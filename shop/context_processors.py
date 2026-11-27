from django.conf import settings
from shop.models import Category, ConsultationLead


def site(request):
    new_leads_count = 0
    if hasattr(request, "user") and request.user.is_authenticated and request.user.is_staff:
        try:
            new_leads_count = ConsultationLead.objects.filter(status=ConsultationLead.Status.NEW).count()
        except Exception:
            new_leads_count = 0

    return {
        "SITE_CONTACT_EMAIL": settings.SITE_CONTACT_EMAIL,
        "ADMIN_EMAIL": getattr(settings, "ADMIN_EMAIL", settings.SITE_CONTACT_EMAIL),
        "SITE_HOTLINE": settings.SITE_HOTLINE,
        "SITE_ZALO": getattr(settings, "SITE_ZALO", "https://zalo.me/0827721974"),
        "nav_categories": Category.objects.all(),
        "new_leads_count": new_leads_count,
    }
