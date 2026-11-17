from django import template

register = template.Library()


@register.filter
def vnd(value):
    """125000 -> 125.000₫"""
    try:
        number = int(value)
    except (TypeError, ValueError):
        return ""
    return f"{number:,}".replace(",", ".") + "₫"
