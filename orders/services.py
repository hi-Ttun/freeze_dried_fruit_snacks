import secrets

from django.conf import settings
from django.db import transaction
from django.db.models import F

from shop.models import Lot, Variant

from .models import (
    Order,
    OrderItem,
    OrderItemAllocation,
    Payment,
    StatusHistory,
    generate_order_code,
)


class CheckoutError(Exception):
    """Lỗi nghiệp vụ khi đặt hàng (hiển thị được cho khách)."""


def shipping_fee_for(zone, subtotal):
    if subtotal >= settings.FREE_SHIPPING_THRESHOLD:
        return 0
    if zone == Order.Zone.URBAN:
        return settings.SHIPPING_FEE_URBAN
    return settings.SHIPPING_FEE_OTHER


def _allocate(variant, quantity):
    """FEFO: lấy từ lô có hạn dùng gần nhất (còn đủ hạn tối thiểu) trước."""
    remaining = quantity
    allocations = []
    lots = Lot.objects.select_for_update().sellable().filter(variant=variant).order_by("expires_on", "id")
    for lot in lots:
        take = min(lot.quantity_left, remaining)
        allocations.append((lot, take))
        remaining -= take
        if remaining == 0:
            break
    if remaining > 0:
        raise CheckoutError(f"{variant.product.name} ({variant.label}) không đủ hàng. Vui lòng giảm số lượng.")
    return allocations


def _unique_code():
    for _ in range(10):
        code = generate_order_code()
        if not Order.objects.filter(code=code).exists():
            return code
    raise CheckoutError("Không thể tạo mã đơn hàng, vui lòng thử lại.")


@transaction.atomic
def place_order(*, items, customer, payment_method, user=None):
    """Tạo đơn hàng trong một transaction và trừ kho theo lô.

    items: danh sách (variant_id, số lượng)
    customer: dict gồm name, phone, email, address, zone, note
    """
    wanted = {}
    for variant_id, quantity in items:
        quantity = int(quantity)
        if quantity > 0:
            wanted[int(variant_id)] = wanted.get(int(variant_id), 0) + quantity
    if not wanted:
        raise CheckoutError("Giỏ hàng đang trống.")

    variants = {
        v.id: v
        for v in Variant.objects.select_related("product").filter(
            id__in=wanted.keys(), is_active=True, product__is_active=True
        )
    }
    if len(variants) != len(wanted):
        raise CheckoutError("Có sản phẩm không còn được bán. Vui lòng kiểm tra lại giỏ hàng.")

    plan = []
    subtotal = 0
    for variant_id in sorted(wanted):  # khóa theo thứ tự cố định để tránh deadlock
        variant = variants[variant_id]
        quantity = wanted[variant_id]
        plan.append((variant, quantity, _allocate(variant, quantity)))
        subtotal += variant.price * quantity

    zone = customer.get("zone", Order.Zone.URBAN)
    fee = shipping_fee_for(zone, subtotal)
    order = Order.objects.create(
        code=_unique_code(),
        user=user,
        customer_name=customer["name"],
        phone=customer["phone"],
        email=customer.get("email", ""),
        address=customer["address"],
        zone=zone,
        note=customer.get("note", ""),
        subtotal=subtotal,
        shipping_fee=fee,
        total=subtotal + fee,
    )
    for variant, quantity, allocations in plan:
        item = OrderItem.objects.create(
            order=order,
            variant=variant,
            product_name=variant.product.name,
            variant_label=variant.label,
            unit_price=variant.price,
            quantity=quantity,
        )
        for lot, take in allocations:
            OrderItemAllocation.objects.create(item=item, lot=lot, quantity=take)
            Lot.objects.filter(pk=lot.pk).update(quantity_left=F("quantity_left") - take)

    payos_code = int(f"{order.id}{secrets.randbelow(9000) + 100}")
    Payment.objects.create(order=order, method=payment_method, amount=order.total, payos_order_code=payos_code)
    StatusHistory.objects.create(order=order, from_status="", to_status=order.status, note="Khách đặt hàng")
    return order
