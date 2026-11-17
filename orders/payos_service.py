import hmac
import hashlib
import json
import logging
import secrets
import time
from typing import Optional, Tuple

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from .models import Order, Payment

logger = logging.getLogger(__name__)


def is_payos_configured() -> bool:
    return bool(
        getattr(settings, "PAYOS_CLIENT_ID", "").strip()
        and getattr(settings, "PAYOS_API_KEY", "").strip()
        and getattr(settings, "PAYOS_CHECKSUM_KEY", "").strip()
    )


def get_payos_client():
    if not is_payos_configured():
        return None
    try:
        from payos import PayOS
        return PayOS(
            client_id=settings.PAYOS_CLIENT_ID.strip(),
            api_key=settings.PAYOS_API_KEY.strip(),
            checksum_key=settings.PAYOS_CHECKSUM_KEY.strip(),
        )
    except Exception as exc:
        logger.error(f"Lỗi khởi tạo PayOS client: {exc}")
        return None


def generate_payos_order_code(order: Order) -> int:
    """Tạo mã số nguyên duy nhất cho PayOS (PayOS yêu cầu orderCode kiểu số nguyên)."""
    # Kết hợp order.id và 4 số ngẫu nhiên để tránh trùng khi tạo lại link thanh toán
    salt = secrets.randbelow(9000) + 1000
    return int(f"{order.id}{salt}")


def create_payos_payment_link(order: Order, request=None) -> Tuple[Optional[str], Optional[str]]:
    """
    Tạo link thanh toán PayOS cho đơn hàng.
    Trả về tuple (checkout_url, error_message).
    """
    payment = getattr(order, "payment", None)
    if not payment:
        return None, "Đơn hàng chưa có thông tin thanh toán."

    order_code = payment.payos_order_code or generate_payos_order_code(order)
    payment.payos_order_code = order_code

    if not is_payos_configured():
        # Chưa cấu hình API Key: Lưu mã order_code để sẵn sàng giả lập kiểm thử
        payment.save(update_fields=["payos_order_code"])
        return None, "Chưa cấu hình API Key PayOS trong file .env (PAYOS_CLIENT_ID, PAYOS_API_KEY, PAYOS_CHECKSUM_KEY)."

    try:
        from payos.types.v2.payment_requests.payment_requests import CreatePaymentLinkRequest, ItemData

        client = get_payos_client()
        if not client:
            return None, "Không thể kết nối với PayOS."

        # Xây dựng Return URL và Cancel URL
        if request:
            return_url = request.build_absolute_uri(reverse("payos_return"))
            cancel_url = request.build_absolute_uri(reverse("payos_cancel"))
        else:
            return_url = f"http://127.0.0.1:8000{reverse('payos_return')}"
            cancel_url = f"http://127.0.0.1:8000{reverse('payos_cancel')}"

        # Danh sách sản phẩm rút gọn
        items = [
            ItemData(
                name=f"{item.product_name} ({item.variant_label})"[:50],
                quantity=item.quantity,
                price=int(item.unit_price),
            )
            for item in order.items.all()
        ]

        desc = f"NutriSnack {order.code}"[:25]
        buyer_name = order.customer_name[:100]
        buyer_phone = order.phone[:20]
        buyer_email = order.email[:100] if order.email else None
        buyer_address = order.address[:200]

        link_request = CreatePaymentLinkRequest(
            order_code=order_code,
            amount=int(order.total),
            description=desc,
            cancel_url=cancel_url,
            return_url=return_url,
            items=items if items else None,
            buyer_name=buyer_name,
            buyer_phone=buyer_phone,
            buyer_email=buyer_email,
            buyer_address=buyer_address,
        )

        response = client.payment_requests.create(link_request)

        payment.checkout_url = response.checkout_url or ""
        payment.qr_code = response.qr_code or ""
        payment.save(update_fields=["payos_order_code", "checkout_url", "qr_code"])

        return response.checkout_url, None

    except Exception as exc:
        logger.exception(f"Lỗi tạo link PayOS cho đơn {order.code}: {exc}")
        return None, str(exc)


def verify_payos_webhook(raw_body: bytes) -> Tuple[Optional[dict], Optional[str]]:
    """
    Xác thực chữ ký HMAC-SHA256 của Webhook IPN gửi từ PayOS.
    Trả về tuple (data_dict, error_message).
    """
    client = get_payos_client()
    if not client:
        # Nếu chưa cấu hình PayOS trong môi trường dev, parse payload cơ bản để test
        try:
            payload = json.loads(raw_body.decode("utf-8"))
            return payload.get("data"), None
        except Exception as exc:
            return None, f"JSON không hợp lệ: {exc}"

    try:
        webhook_data = client.webhooks.verify(raw_body)
        return webhook_data.model_dump(), None
    except Exception as exc:
        logger.warning(f"Chữ ký PayOS webhook không hợp lệ: {exc}")
        return None, f"Chữ ký không hợp lệ: {exc}"


def process_payos_success(order_code: int, reference: str = "", amount: Optional[int] = None) -> Optional[Order]:
    """
    Xử lý cập nhật đơn hàng sau khi nhận tín hiệu thanh toán thành công từ Webhook IPN.
    """
    with transaction.atomic():
        payment = (
            Payment.objects.select_for_update()
            .select_related("order")
            .filter(payos_order_code=order_code)
            .first()
        )
        if not payment:
            # Thử tìm theo order.id trong trường hợp order_code trùng order.id
            payment = (
                Payment.objects.select_for_update()
                .select_related("order")
                .filter(order_id=order_code)
                .first()
            )

        if not payment:
            logger.warning(f"Không tìm thấy Payment tương ứng với payos_order_code={order_code}")
            return None

        order = payment.order
        if payment.status == Payment.Status.PAID:
            logger.info(f"Đơn {order.code} đã được thanh toán trước đó.")
            return order

        # Cập nhật trạng thái đơn hàng: pending -> confirmed -> paid
        if order.status == Order.Status.PENDING:
            order.change_status(Order.Status.CONFIRMED, note="Hệ thống tự động xác nhận qua PayOS IPN")
        if order.status == Order.Status.CONFIRMED:
            note_text = f"Cổng PayOS xác nhận thanh toán thành công. Mã GD: {reference or 'N/A'}"
            order.change_status(Order.Status.PAID, note=note_text)

        payment.mark_paid(reference=reference or f"PAYOS-{order_code}")
        logger.info(f"Đơn {order.code} đã được cập nhật PAID thành công qua IPN.")
        return order

