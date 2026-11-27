from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from .models import Category, ConsultationLead, Lot, Product, Variant

admin.site.site_header = "NutriSnack - Quản trị"
admin.site.site_title = "NutriSnack"
admin.site.index_title = "Quản lý cửa hàng"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "is_featured", "created_at")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [VariantInline]


class ExpiryFilter(admin.SimpleListFilter):
    title = "hạn dùng"
    parameter_name = "han"

    def lookups(self, request, model_admin):
        return (
            ("expired", "Đã hết hạn"),
            ("soon", "Còn tối đa 60 ngày"),
            ("ok", "Còn hơn 60 ngày"),
        )

    def queryset(self, request, queryset):
        today = timezone.localdate()
        soon = today + timedelta(days=60)
        if self.value() == "expired":
            return queryset.filter(expires_on__lt=today)
        if self.value() == "soon":
            return queryset.filter(expires_on__gte=today, expires_on__lte=soon)
        if self.value() == "ok":
            return queryset.filter(expires_on__gt=soon)
        return queryset


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "label", "weight_g", "price", "stock", "is_active")
    list_editable = ("price", "is_active")
    list_filter = ("product__category", "is_active")
    search_fields = ("sku", "product__name", "label")


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ("code", "variant", "produced_on", "expires_on", "days_left_display", "quantity_in", "quantity_left")
    list_editable = ("quantity_left",)
    list_filter = (ExpiryFilter, "variant__product")
    search_fields = ("code", "variant__product__name")
    list_select_related = ("variant__product",)
    ordering = ("expires_on",)

    @admin.display(description="Còn (ngày)", ordering="expires_on")
    def days_left_display(self, obj):
        return obj.days_left


@admin.register(ConsultationLead)
class ConsultationLeadAdmin(admin.ModelAdmin):
    list_display = ("phone", "customer_name", "status", "created_at", "short_note")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("phone", "customer_name", "note")
    readonly_fields = ("created_at",)

    @admin.display(description="Lời nhắn / Nhu cầu")
    def short_note(self, obj):
        return (obj.note[:60] + "...") if len(obj.note) > 60 else obj.note

