from datetime import timedelta
from urllib.parse import quote, urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, IntegerField, Sum
from django.db.models.functions import TruncDate
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from shop.models import Lot, Variant

from .cart import Cart
from .forms import CheckoutForm, OrderLookupForm
from .models import Order, OrderItem, Payment
from .payos_service import (
    create_payos_payment_link,
    is_payos_configured,
    process_payos_success,
    verify_payos_webhook,
)
from .services import CheckoutError, place_order


def _parse_qty(raw, default=1):
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return max(-1, min(value, settings.CART_MAX_QTY))


def _safe_next(request, default):
    target = request.POST.get("next", "")
    if target and url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return target
    return reverse(default)


def _remember_order(request, code):
    codes = list(request.session.get("order_codes", []))
    if code not in codes:
        codes.append(code)
    request.session["order_codes"] = codes


def cart_detail(request):
    lines = Cart(request).lines()
    subtotal = sum(line["line_total"] for line in lines)
    context = {
        "lines": lines,
        "subtotal": subtotal,
        "has_problem": any(line["short"] for line in lines),
        "free_ship_threshold": settings.FREE_SHIPPING_THRESHOLD,
        "remaining_free": max(0, settings.FREE_SHIPPING_THRESHOLD - subtotal),
    }
    return render(request, "orders/cart.html", context)


@require_POST
def cart_add(request, variant_id):
    variant = get_object_or_404(Variant, pk=variant_id, is_active=True, product__is_active=True)
    quantity = max(1, _parse_qty(request.POST.get("quantity"), default=1))
    Cart(request).add(variant.id, quantity)
    messages.success(request, f"Đã thêm {variant.product.name} ({variant.label}) vào giỏ hàng.")
    return redirect(_safe_next(request, "cart"))


@require_POST
def cart_update(request, variant_id):
    quantity = _parse_qty(request.POST.get("quantity"), default=1)
    Cart(request).set(variant_id, quantity)
    return redirect("cart")


@require_POST
def cart_remove(request, variant_id):
    Cart(request).remove(variant_id)
    return redirect("cart")


def checkout(request):
    cart = Cart(request)
    lines = cart.lines()
    if not lines:
        messages.info(request, "Giỏ hàng đang trống. Hãy chọn sản phẩm trước khi thanh toán.")
        return redirect("product_list")

    subtotal = sum(line["line_total"] for line in lines)
    initial = {"payment_method": Payment.Method.COD, "zone": Order.Zone.URBAN}
    if request.user.is_authenticated:
        initial["customer_name"] = request.user.get_full_name() or request.user.username
        initial["email"] = request.user.email
    form = CheckoutForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        customer = {
            "name": data["customer_name"],
            "phone": data["phone"],
            "email": data["email"],
            "address": data["address"],
            "zone": data["zone"],
            "note": data["note"],
        }
        try:
            order = place_order(
                items=[(line["variant"].id, line["quantity"]) for line in lines],
                customer=customer,
                payment_method=data["payment_method"],
                user=request.user if request.user.is_authenticated else None,
            )
        except CheckoutError as exc:
            messages.error(request, str(exc))
            return redirect("cart")
        cart.clear()
        _remember_order(request, order.code)
        return redirect(f"{reverse('order_detail', args=[order.code])}?placed=1")

    context = {
        "form": form,
        "lines": lines,
        "subtotal": subtotal,
        "fee_urban": settings.SHIPPING_FEE_URBAN,
        "fee_other": settings.SHIPPING_FEE_OTHER,
        "free_ship_threshold": settings.FREE_SHIPPING_THRESHOLD,
    }
    return render(request, "orders/checkout.html", context)


def _bank_info(order):
    payment = getattr(order, "payment", None)
    if not payment or payment.method != Payment.Method.BANK or payment.status != Payment.Status.PENDING:
        return None
    if not (settings.BANK_ACCOUNT and settings.BANK_NAME):
        return None
    qr_url = ""
    if settings.VIETQR_BANK_ID:
        query = urlencode({"amount": order.total, "addInfo": order.code, "accountName": settings.BANK_HOLDER})
        qr_url = f"https://img.vietqr.io/image/{settings.VIETQR_BANK_ID}-{settings.BANK_ACCOUNT}-compact2.png?{query}"
    return {
        "bank": settings.BANK_NAME,
        "account": settings.BANK_ACCOUNT,
        "holder": settings.BANK_HOLDER,
        "qr_url": qr_url,
    }


def _payos_info(order):
    payment = getattr(order, "payment", None)
    if not payment or payment.method != "payos":
        return None
    qr_url = ""
    if payment.qr_code:
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={quote(payment.qr_code)}"
    elif settings.VIETQR_BANK_ID and settings.BANK_ACCOUNT:
        query = urlencode({"amount": order.total, "addInfo": f"DH {order.code}", "accountName": settings.BANK_HOLDER})
        qr_url = f"https://img.vietqr.io/image/{settings.VIETQR_BANK_ID}-{settings.BANK_ACCOUNT}-compact2.png?{query}"
    return {
        "checkout_url": payment.checkout_url,
        "order_code": payment.payos_order_code,
        "qr_url": qr_url,
        "is_configured": is_payos_configured(),
        "is_pending": payment.status == Payment.Status.PENDING,
        "is_paid": payment.status == Payment.Status.PAID,
    }


def order_detail(request, code):
    order = get_object_or_404(
        Order.objects.select_related("payment", "shipment").prefetch_related("items__allocations__lot", "history"),
        code=code,
    )
    allowed = (
        request.user.is_staff
        or (request.user.is_authenticated and order.user_id == request.user.id)
        or code in request.session.get("order_codes", [])
    )
    if not allowed:
        raise Http404()
    context = {
        "order": order,
        "history": order.history.all(),
        "bank": _bank_info(order),
        "payos": _payos_info(order),
        "placed": request.GET.get("placed") == "1",
    }
    return render(request, "orders/order_detail.html", context)


@csrf_exempt
@require_POST
def payos_ipn(request):
    """
    Webhook endpoint nhận thông báo thanh toán (IPN) từ cổng PayOS theo thời gian thực.
    PayOS sẽ gửi HTTP POST kèm payload JSON và chữ ký số HMAC-SHA256.
    """
    data, err = verify_payos_webhook(request.body)
    if err:
        return JsonResponse({"code": "01", "message": f"Webhook verification failed: {err}"}, status=400)

    if not data:
        return JsonResponse({"code": "01", "message": "No data in webhook payload"}, status=400)

    order_code = data.get("orderCode") or data.get("order_code")
    reference = data.get("reference") or data.get("paymentLinkId") or ""
    amount = data.get("amount")

    if not order_code:
        return JsonResponse({"code": "01", "message": "Missing orderCode"}, status=400)

    try:
        order = process_payos_success(int(order_code), reference=str(reference), amount=amount)
        if order:
            return JsonResponse({"code": "00", "message": "Success", "order_code": order.code})
        return JsonResponse({"code": "02", "message": "Order not found or already paid"})
    except Exception as exc:
        return JsonResponse({"code": "99", "message": str(exc)}, status=500)


def order_payment_status(request, code):
    """API nhẹ hỗ trợ client polling kiểm tra trạng thái thanh toán Realtime."""
    order = get_object_or_404(Order.objects.select_related("payment"), code=code)
    payment = getattr(order, "payment", None)
    return JsonResponse({
        "code": order.code,
        "status": order.status,
        "status_display": order.get_status_display(),
        "payment_status": payment.status if payment else None,
        "payment_status_display": payment.get_status_display() if payment else None,
        "is_paid": bool(payment and payment.status == Payment.Status.PAID),
    })


def payos_return(request):
    """Xử lý khi khách hoàn tất thanh toán trên PayOS và được chuyển hướng về website."""
    order_code = request.GET.get("orderCode")
    status = request.GET.get("status")
    if order_code:
        try:
            payment = Payment.objects.select_related("order").filter(payos_order_code=int(order_code)).first()
            if payment:
                if status == "PAID" or request.GET.get("code") == "00":
                    process_payos_success(int(order_code), reference="PAYOS-RETURN")
                    messages.success(request, "Thanh toán đơn hàng thành công qua cổng PayOS!")
                return redirect("order_detail", code=payment.order.code)
        except Exception:
            pass
    return redirect("my_orders")


def payos_cancel(request):
    """Xử lý khi khách bấm hủy thanh toán trên cổng PayOS."""
    order_code = request.GET.get("orderCode")
    if order_code:
        try:
            payment = Payment.objects.select_related("order").filter(payos_order_code=int(order_code)).first()
            if payment:
                messages.info(request, "Giao dịch thanh toán PayOS đã bị hủy.")
                return redirect("order_detail", code=payment.order.code)
        except Exception:
            pass
    return redirect("cart")


@require_POST
def payos_simulate_payment(request, code):
    """
    Giả lập Webhook IPN PayOS cho mục đích kiểm thử và demo đồ án.
    Cho phép test realtime ngay cả khi chưa mở ngrok ra ngoài Internet!
    """
    order = get_object_or_404(Order.objects.select_related("payment"), code=code)
    payment = getattr(order, "payment", None)
    if not payment:
        return JsonResponse({"success": False, "message": "Không tìm thấy thanh toán"}, status=404)

    order_code = payment.payos_order_code or order.id
    updated_order = process_payos_success(
        order_code=order_code,
        reference=f"SIMULATED-IPN-{int(timezone.now().timestamp()) % 10000}",
        amount=order.total,
    )
    return JsonResponse({
        "success": True,
        "order_code": order.code,
        "status": updated_order.status if updated_order else order.status,
        "payment_status": updated_order.payment.status if updated_order else payment.status,
    })


def order_lookup(request):
    form = OrderLookupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = Order.objects.filter(code=form.cleaned_data["code"], phone=form.cleaned_data["phone"]).first()
        if order:
            _remember_order(request, order.code)
            return redirect("order_detail", code=order.code)
        messages.error(request, "Không tìm thấy đơn hàng với mã và số điện thoại đã nhập.")
    return render(request, "orders/order_lookup.html", {"form": form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).select_related("payment")
    return render(request, "orders/my_orders.html", {"orders": orders})


@staff_member_required
def dashboard(request):
    today = timezone.localdate()
    start = today - timedelta(days=13)
    excluded = [Order.Status.CANCELLED, Order.Status.RETURNED]
    valid = Order.objects.exclude(status__in=excluded)

    rows = (
        valid.filter(created_at__date__gte=start)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(revenue=Sum("total"), n=Count("id"))
        .order_by("day")
    )
    by_day = {row["day"]: row for row in rows}
    series = []
    for i in range(14):
        day = start + timedelta(days=i)
        row = by_day.get(day)
        series.append({"day": day, "revenue": row["revenue"] if row else 0, "orders": row["n"] if row else 0})
    peak = max((d["revenue"] for d in series), default=0) or 1
    for d in series:
        d["pct"] = round(d["revenue"] * 100 / peak)

    revenue_14d = sum(d["revenue"] for d in series)
    orders_14d = sum(d["orders"] for d in series)
    month_revenue = valid.filter(created_at__date__gte=today.replace(day=1)).aggregate(t=Sum("total"))["t"] or 0

    top_products = (
        OrderItem.objects.exclude(order__status__in=excluded)
        .values("product_name")
        .annotate(qty=Sum("quantity"), revenue=Sum(F("unit_price") * F("quantity"), output_field=IntegerField()))
        .order_by("-qty")[:5]
    )
    labels = dict(Order.Status.choices)
    status_counts = [
        {"label": labels.get(r["status"], r["status"]), "n": r["n"]}
        for r in Order.objects.values("status").annotate(n=Count("id")).order_by("status")
    ]
    expiring = (
        Lot.objects.filter(quantity_left__gt=0, expires_on__lte=today + timedelta(days=60))
        .select_related("variant__product")
        .order_by("expires_on")[:10]
    )
    context = {
        "series": series,
        "revenue_14d": revenue_14d,
        "orders_14d": orders_14d,
        "aov": round(revenue_14d / orders_14d) if orders_14d else 0,
        "month_revenue": month_revenue,
        "pending_count": Order.objects.filter(status=Order.Status.PENDING).count(),
        "top_products": top_products,
        "status_counts": status_counts,
        "expiring": expiring,
    }
    return render(request, "orders/dashboard.html", context)
