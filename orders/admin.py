from django.contrib import admin, messages

from .models import Order, OrderItem, Payment, Shipment, StatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    fields = ("product_name", "variant_label", "unit_price", "quantity", "lots")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description="Lô xuất kho")
    def lots(self, obj):
        return ", ".join(f"{a.lot.code} x{a.quantity}" for a in obj.allocations.select_related("lot"))


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    max_num = 1
    can_delete = False
    fields = ("method", "status", "amount", "paid_at", "reference")
    readonly_fields = ("method", "status", "amount", "paid_at")


class ShipmentInline(admin.StackedInline):
    model = Shipment
    extra = 1
    max_num = 1
    can_delete = False
    fields = ("carrier", "tracking_code", "shipped_at", "delivered_at")
    readonly_fields = ("shipped_at", "delivered_at")


class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    can_delete = False
    fields = ("created_at", "from_status", "to_status", "note", "by")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False


def _status_action(target, label):
    def action(modeladmin, request, queryset):
        done = failed = 0
        for order in queryset:
            try:
                order.change_status(target, by=request.user)
                done += 1
            except ValueError:
                failed += 1
        if done:
            modeladmin.message_user(request, f"Đã chuyển {done} đơn sang '{label}'.", messages.SUCCESS)
        if failed:
            modeladmin.message_user(
                request, f"{failed} đơn không thể chuyển sang '{label}' vì trạng thái hiện tại không cho phép.", messages.WARNING
            )

    action.__name__ = f"to_{target}"
    return admin.action(permissions=["change"], description=f"Chuyển sang: {label}")(action)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("code", "customer_name", "phone", "total", "status", "payment_status", "created_at")
    list_filter = ("status", "zone")
    search_fields = ("code", "customer_name", "phone", "email")
    list_select_related = ("payment",)
    inlines = [OrderItemInline, PaymentInline, ShipmentInline, StatusHistoryInline]
    readonly_fields = (
        "code", "status", "user", "customer_name", "phone", "email", "zone",
        "subtotal", "shipping_fee", "total", "created_at", "updated_at",
    )
    fieldsets = (
        ("Đơn hàng", {"fields": ("code", "status", "user", "created_at")}),
        ("Khách hàng", {"fields": ("customer_name", "phone", "email", "address", "zone", "note")}),
        ("Giá trị", {"fields": ("subtotal", "shipping_fee", "total")}),
    )
    actions = [
        _status_action(Order.Status.CONFIRMED.value, Order.Status.CONFIRMED.label),
        _status_action(Order.Status.PAID.value, Order.Status.PAID.label),
        _status_action(Order.Status.PACKING.value, Order.Status.PACKING.label),
        _status_action(Order.Status.SHIPPING.value, Order.Status.SHIPPING.label),
        _status_action(Order.Status.DELIVERED.value, Order.Status.DELIVERED.label),
        _status_action(Order.Status.COMPLETED.value, Order.Status.COMPLETED.label),
        _status_action(Order.Status.CANCELLED.value, Order.Status.CANCELLED.label),
        _status_action(Order.Status.RETURNED.value, Order.Status.RETURNED.label),
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.display(description="Thanh toán")
    def payment_status(self, obj):
        payment = getattr(obj, "payment", None)
        return payment.get_status_display() if payment else "-"
