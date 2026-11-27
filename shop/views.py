import json
import os
from datetime import timedelta

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Min, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .ai_chatbot import get_chat_response
from .models import Category, ConsultationLead, Lot, Product

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


@csrf_exempt
@require_POST
def chat_message(request):
    """Tiếp nhận câu hỏi từ Chatbot AI và phản hồi thông tin."""
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        data = request.POST

    message = data.get("message", "").strip()
    history = data.get("history", [])

    response_data = get_chat_response(message, history=history)
    return JsonResponse(response_data)


@csrf_exempt
@require_POST
def chat_lead(request):
    """Lưu thông tin yêu cầu tư vấn viên gọi lại (Human Handoff Lead)."""
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        data = request.POST

    phone = data.get("phone", "").strip()
    name = data.get("customer_name", "").strip()
    note = data.get("note", "").strip()

    if not phone or len(phone) < 9:
        return JsonResponse({"success": False, "message": "Vui lòng nhập số điện thoại hợp lệ (từ 10 chữ số)."}, status=400)

    lead = ConsultationLead.objects.create(
        customer_name=name,
        phone=phone,
        note=note or "Yêu cầu tư vấn trực tiếp từ Chatbot AI",
        status=ConsultationLead.Status.NEW
    )

    # 1. Ghi log nổi bật ra màn hình console máy chủ
    print(f"\n{'='*60}\n🔔 [LEAD MỚI] KHÁCH HÀNG YÊU CẦU TƯ VẤN TRỰC TIẾP!\n📞 SĐT: {phone}\n👤 Tên: {name or 'Khách vãng lai'}\n📝 Nhu cầu: {lead.note}\n⏰ Thời gian: {timezone.localtime(lead.created_at):%d/%m/%Y %H:%M:%S}\n{'='*60}\n")

    # 2. Gửi Email thông báo tự động đến Admin
    try:
        from django.core.mail import send_mail
        admin_email = getattr(settings, "ADMIN_EMAIL", "") or getattr(settings, "SITE_CONTACT_EMAIL", "")
        if admin_email:
            send_mail(
                subject=f"[NutriSnack] 🔔 Có khách hàng yêu cầu tư vấn mới: {phone}",
                message=(
                    f"Có khách hàng vừa để lại số điện thoại yêu cầu tư vấn trên website!\n\n"
                    f"• Số điện thoại: {phone}\n"
                    f"• Họ tên: {name or 'Khách vãng lai'}\n"
                    f"• Nhu cầu: {lead.note}\n"
                    f"• Thời gian: {timezone.localtime(lead.created_at):%d/%m/%Y %H:%M}\n\n"
                    f"Vui lòng đăng nhập trang quản trị để liên hệ và xử lý:\n"
                    f"http://127.0.0.1:8000/admin/shop/consultationlead/\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, "DEFAULT_FROM_EMAIL") else None,
                recipient_list=[admin_email],
                fail_silently=True,
            )
    except Exception as e:
        pass

    # 3. Gửi tin nhắn qua Telegram Bot (nếu có cấu hình)
    tg_token = getattr(settings, "TELEGRAM_BOT_TOKEN", "") or os.environ.get("TELEGRAM_BOT_TOKEN", "")
    tg_chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "") or os.environ.get("TELEGRAM_CHAT_ID", "")
    if tg_token and tg_chat_id:
        try:
            import requests
            tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
            tg_text = (
                f"🔔 *[NutriSnack] KHÁCH YÊU CẦU TƯ VẤN MỚI!*\n\n"
                f"📞 *SĐT:* `{phone}`\n"
                f"👤 *Khách:* {name or 'Khách vãng lai'}\n"
                f"📝 *Nội dung:* {lead.note}\n"
                f"⏰ *Lúc:* {timezone.localtime(lead.created_at):%d/%m/%Y %H:%M}\n\n"
                f"👉 [Mở trang quản trị](http://127.0.0.1:8000/admin/shop/consultationlead/)"
            )
            requests.post(tg_url, json={"chat_id": tg_chat_id, "text": tg_text, "parse_mode": "Markdown"}, timeout=3)
        except Exception:
            pass

    return JsonResponse({
        "success": True,
        "message": f"Dạ NutriSnack đã ghi nhận số điện thoại {phone}! Chuyên viên tư vấn sẽ liên hệ lại ngay trong ít phút ạ."
    })


