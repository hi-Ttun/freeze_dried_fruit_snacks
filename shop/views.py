from datetime import timedelta

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Min, Q, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Lot, Product

SORTS = {
    "new": "-created_at",
    "price_asc": "price_from",
    "price_desc": "-price_from",
    "name": "name",
}


def _products():
    """Sản phẩm đang bán kèm giá thấp nhất và tồn kho còn bán được."""
    cutoff = timezone.localdate() + timedelta(days=settings.MIN_SHELF_DAYS)
    return (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .annotate(
            price_from=Min("variants__price", filter=Q(variants__is_active=True)),
            stock_total=Sum(
                "variants__lots__quantity_left",
                filter=Q(
                    variants__is_active=True,
                    variants__lots__quantity_left__gt=0,
                    variants__lots__expires_on__gte=cutoff,
                ),
            ),
        )
    )


def home(request):
    featured = list(_products().filter(is_featured=True)[:4])
    if not featured:
        featured = list(_products().order_by("-created_at")[:4])
    context = {
        "featured": featured,
        "categories": Category.objects.all(),
        "min_shelf_days": settings.MIN_SHELF_DAYS,
    }
    return render(request, "shop/home.html", context)


def product_list(request):
    qs = _products()
    q = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "new")

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(short_description__icontains=q))
    category = None
    if category_slug:
        category = Category.objects.filter(slug=category_slug).first()
        if category:
            qs = qs.filter(category=category)
    if sort not in SORTS:
        sort = "new"
    qs = qs.order_by(SORTS[sort], "id")

    page = Paginator(qs, 12).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "page": page,
        "categories": Category.objects.all(),
        "category": category,
        "q": q,
        "sort": sort,
        "qs": params.urlencode(),
    }
    return render(request, "shop/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, is_active=True)
    variants = list(product.variants.filter(is_active=True).order_by("weight_g", "price"))
    for variant in variants:
        variant.available = variant.stock
        variant.next_lot_obj = variant.next_lot
    related = _products().filter(category=product.category).exclude(pk=product.pk)[:4]
    context = {
        "product": product,
        "variants": variants,
        "related": related,
        "max_qty": settings.CART_MAX_QTY,
        "min_shelf_days": settings.MIN_SHELF_DAYS,
    }
    return render(request, "shop/product_detail.html", context)


def trace(request):
    """Truy xuất nguồn gốc theo mã lô in trên bao bì."""
    code = request.GET.get("code", "").strip()
    lot = None
    if code:
        lot = Lot.objects.select_related("variant__product").filter(code__iexact=code).first()
    return render(request, "shop/trace.html", {"code": code, "lot": lot})
