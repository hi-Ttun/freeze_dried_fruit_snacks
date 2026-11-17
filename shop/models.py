from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Category(models.Model):
    name = models.CharField("Tên danh mục", max_length=120)
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField("Thứ tự", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Danh mục")
    name = models.CharField("Tên sản phẩm", max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField("Mô tả ngắn", max_length=255, blank=True)
    description = models.TextField("Mô tả chi tiết", blank=True)
    ingredients = models.CharField("Thành phần", max_length=255, blank=True)
    nutrition = models.TextField("Giá trị dinh dưỡng", blank=True)
    origin = models.CharField("Xuất xứ", max_length=200, blank=True)
    certificates = models.CharField("Chứng nhận / kiểm nghiệm", max_length=255, blank=True)
    image = models.ImageField("Ảnh", upload_to="products/", blank=True)
    is_active = models.BooleanField("Đang bán", default=True)
    is_featured = models.BooleanField("Nổi bật", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    def __str__(self):
        return self.name

    @property
    def tile_color(self):
        """Màu nền ổn định cho từng sản phẩm khi chưa có ảnh."""
        hue = sum(ord(c) for c in self.slug) % 360
        return f"hsl({hue} 55% 86%)"


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", verbose_name="Sản phẩm")
    label = models.CharField("Quy cách", max_length=50, help_text="Ví dụ: 50g, hộp 200g")
    weight_g = models.PositiveIntegerField("Khối lượng (g)")
    price = models.PositiveIntegerField("Giá (VNĐ)")
    sku = models.CharField("Mã SKU", max_length=40, unique=True)
    is_active = models.BooleanField("Đang bán", default=True)

    class Meta:
        ordering = ["product", "weight_g"]
        verbose_name = "Quy cách"
        verbose_name_plural = "Quy cách"

    def __str__(self):
        return f"{self.product.name} ({self.label})"

    @property
    def stock(self):
        """Tồn kho có thể bán: chỉ tính lô còn đủ hạn dùng tối thiểu."""
        total = self.lots.sellable().aggregate(t=Sum("quantity_left"))["t"]
        return total or 0

    @property
    def next_lot(self):
        """Lô sẽ được xuất trước (FEFO): hạn dùng gần nhất trong các lô còn bán được."""
        return self.lots.sellable().order_by("expires_on", "id").first()


class LotQuerySet(models.QuerySet):
    def sellable(self):
        cutoff = timezone.localdate() + timedelta(days=settings.MIN_SHELF_DAYS)
        return self.filter(quantity_left__gt=0, expires_on__gte=cutoff)


class Lot(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT, related_name="lots", verbose_name="Quy cách")
    code = models.CharField("Mã lô", max_length=40, unique=True)
    produced_on = models.DateField("Ngày sản xuất")
    expires_on = models.DateField("Hạn sử dụng")
    quantity_in = models.PositiveIntegerField("Số lượng nhập")
    quantity_left = models.PositiveIntegerField("Số lượng còn", default=0, help_text="Để 0 khi tạo mới, hệ thống sẽ lấy bằng số lượng nhập")
    source_note = models.CharField("Nguồn gốc lô (vùng trồng / nhà cung cấp)", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = LotQuerySet.as_manager()

    class Meta:
        ordering = ["expires_on", "id"]
        verbose_name = "Lô hàng"
        verbose_name_plural = "Lô hàng"

    def __str__(self):
        return f"{self.code} ({self.variant})"

    def clean(self):
        if self.expires_on and self.produced_on and self.expires_on <= self.produced_on:
            raise ValidationError("Hạn sử dụng phải sau ngày sản xuất.")
        if self.quantity_left and self.quantity_left > self.quantity_in:
            raise ValidationError("Số lượng còn không được lớn hơn số lượng nhập.")

    def save(self, *args, **kwargs):
        if self._state.adding and not self.quantity_left:
            self.quantity_left = self.quantity_in
        super().save(*args, **kwargs)

    @property
    def days_left(self):
        return (self.expires_on - timezone.localdate()).days
