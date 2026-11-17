import secrets

from django.conf import settings
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

from shop.models import Lot

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_order_code():
    suffix = "".join(secrets.choice(CODE_ALPHABET) for _ in range(5))
    return f"NS{timezone.localdate():%y%m%d}{suffix}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Chờ xác nhận"
        CONFIRMED = "confirmed", "Đã xác nhận"
        PAID = "paid", "Đã thanh toán"
        PACKING = "packing", "Đang đóng gói"
        SHIPPING = "shipping", "Đang giao"
        DELIVERED = "delivered", "Đã giao"
        COMPLETED = "completed", "Hoàn tất"
        CANCELLED = "cancelled", "Đã hủy"
        RETURNED = "returned", "Hoàn trả"

    class Zone(models.TextChoices):
        URBAN = "urban", "Nội thành TP.HCM / Hà Nội"
        OTHER = "other", "Tỉnh thành khác"

    # Vòng đời đơn hàng: chỉ cho phép các bước chuyển hợp lệ.
    TRANSITIONS = {
        "pending": ["confirmed", "paid", "cancelled"],
        "confirmed": ["paid", "packing", "cancelled"],
        "paid": ["packing", "cancelled"],
        "packing": ["shipping", "cancelled"],
        "shipping": ["delivered", "returned"],
        "delivered": ["completed", "returned"],
        "completed": [],
        "cancelled": [],
        "returned": [],
    }

    code = models.CharField("Mã đơn", max_length=20, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders", verbose_name="Tài khoản"
    )
    customer_name = models.CharField("Người nhận", max_length=120)
    phone = models.CharField("Số điện thoại", max_length=20)
    email = models.EmailField("Email", blank=True)
    address = models.TextField("Địa chỉ giao hàng")
    zone = models.CharField("Khu vực", max_length=10, choices=Zone.choices, default=Zone.URBAN)
    note = models.CharField("Ghi chú", max_length=255, blank=True)
    subtotal = models.PositiveIntegerField("Tiền hàng", default=0)
    shipping_fee = models.PositiveIntegerField("Phí vận chuyển", default=0)
    total = models.PositiveIntegerField("Tổng thanh toán", default=0)
    status = models.CharField("Trạng thái", max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField("Ngày đặt", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"

    def __str__(self):
        return self.code

    @property
    def allowed_next(self):
        return self.TRANSITIONS.get(self.status, [])

    def can_move_to(self, new_status):
        return new_status in self.allowed_next

    def change_status(self, new_status, by=None, note=""):
        """Đổi trạng thái hợp lệ, ghi lịch sử và xử lý hệ quả (kho, thanh toán, vận chuyển)."""
        new_status = str(new_status)
        if not self.can_move_to(new_status):
            raise ValueError(f"Không thể chuyển đơn {self.code} từ '{self.status}' sang '{new_status}'.")
        with transaction.atomic():
            old_status = self.status
            if new_status == self.Status.CANCELLED:
                self.restock()
            self.status = new_status
            self.save(update_fields=["status", "updated_at"])
            StatusHistory.objects.create(
                order=self,
                from_status=old_status,
                to_status=new_status,
                note=note,
                by=by if getattr(by, "is_authenticated", False) else None,
            )
            self._apply_side_effects(new_status)

    def restock(self):
        """Trả hàng về đúng các lô đã xuất (chỉ dùng khi hủy trước khi giao)."""
        for item in self.items.all():
            for allocation in item.allocations.all():
                Lot.objects.filter(pk=allocation.lot_id).update(quantity_left=F("quantity_left") + allocation.quantity)

    def _apply_side_effects(self, new_status):
        payment = getattr(self, "payment", None)
        now = timezone.now()
        if new_status == self.Status.PAID and payment:
            payment.mark_paid()
        elif new_status == self.Status.SHIPPING:
            shipment, _ = Shipment.objects.get_or_create(order=self)
            shipment.shipped_at = now
            shipment.save(update_fields=["shipped_at"])
        elif new_status == self.Status.DELIVERED:
            shipment, _ = Shipment.objects.get_or_create(order=self)
            shipment.delivered_at = now
            shipment.save(update_fields=["delivered_at"])
            if payment and payment.method == Payment.Method.COD:
                payment.mark_paid()
        elif new_status in (self.Status.CANCELLED, self.Status.RETURNED) and payment:
            payment.status = Payment.Status.REFUND_DUE if payment.status == Payment.Status.PAID else Payment.Status.FAILED
            payment.save(update_fields=["status"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey("shop.Variant", on_delete=models.PROTECT, related_name="order_items")
    product_name = models.CharField("Sản phẩm", max_length=200)
    variant_label = models.CharField("Quy cách", max_length=50)
    unit_price = models.PositiveIntegerField("Đơn giá")
    quantity = models.PositiveIntegerField("Số lượng")

    class Meta:
        verbose_name = "Sản phẩm trong đơn"
        verbose_name_plural = "Sản phẩm trong đơn"

    def __str__(self):
        return f"{self.product_name} ({self.variant_label}) x{self.quantity}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity


class OrderItemAllocation(models.Model):
    """Dòng hàng được xuất từ lô nào, bao nhiêu (phục vụ FEFO và truy xuất nguồn gốc)."""

    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="allocations")
    lot = models.ForeignKey("shop.Lot", on_delete=models.PROTECT, related_name="allocations")
    quantity = models.PositiveIntegerField()


class Payment(models.Model):
    class Method(models.TextChoices):
        COD = "cod", "Thanh toán khi nhận hàng (COD)"
        BANK = "bank", "Chuyển khoản ngân hàng (VietQR)"

    class Status(models.TextChoices):
        PENDING = "pending", "Chờ thanh toán"
        PAID = "paid", "Đã thanh toán"
        FAILED = "failed", "Không thành công"
        REFUND_DUE = "refund_due", "Cần hoàn tiền"

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField("Phương thức", max_length=10, choices=Method.choices)
    status = models.CharField("Trạng thái", max_length=12, choices=Status.choices, default=Status.PENDING)
    amount = models.PositiveIntegerField("Số tiền")
    paid_at = models.DateTimeField("Thời điểm thanh toán", null=True, blank=True)
    reference = models.CharField("Mã giao dịch / ghi chú đối soát", max_length=100, blank=True)
    payos_order_code = models.BigIntegerField("Mã đơn PayOS", null=True, blank=True, unique=True)
    checkout_url = models.URLField("Link thanh toán PayOS", blank=True, max_length=500)
    qr_code = models.TextField("Mã VietQR", blank=True)

    class Meta:
        verbose_name = "Thanh toán"
        verbose_name_plural = "Thanh toán"

    def mark_paid(self, reference=""):
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        if reference:
            self.reference = reference
        self.save(update_fields=["status", "paid_at", "reference"])


class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipment")
    carrier = models.CharField("Đơn vị vận chuyển", max_length=80, blank=True)
    tracking_code = models.CharField("Mã vận đơn", max_length=80, blank=True)
    shipped_at = models.DateTimeField("Bắt đầu giao", null=True, blank=True)
    delivered_at = models.DateTimeField("Giao thành công", null=True, blank=True)

    class Meta:
        verbose_name = "Vận chuyển"
        verbose_name_plural = "Vận chuyển"


class StatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    from_status = models.CharField(max_length=12, blank=True)
    to_status = models.CharField(max_length=12, choices=Order.Status.choices)
    note = models.CharField(max_length=255, blank=True)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name = "Lịch sử trạng thái"
        verbose_name_plural = "Lịch sử trạng thái"
