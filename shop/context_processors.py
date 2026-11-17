from django.conf import settings
from shop.models import Category


def site(request):
    return {
        "SITE_CONTACT_EMAIL": settings.SITE_CONTACT_EMAIL,
        "ADMIN_EMAIL": getattr(settings, "ADMIN_EMAIL", settings.SITE_CONTACT_EMAIL),
        "SITE_HOTLINE": settings.SITE_HOTLINE,
        "nav_categories": Category.objects.all(),
    }
