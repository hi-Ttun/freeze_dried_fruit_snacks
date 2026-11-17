from django.conf import settings

from shop.models import Variant

SESSION_KEY = "cart"


class Cart:
    """Giỏ hàng lưu trong session: {"<variant_id>": số lượng}."""

    def __init__(self, request):
        self.session = request.session
        self.data = dict(self.session.get(SESSION_KEY, {}))

    def _save(self):
        self.session[SESSION_KEY] = self.data
        self.session.modified = True

    @property
    def count(self):
        return sum(self.data.values())

    def add(self, variant_id, quantity=1):
        key = str(variant_id)
        self.data[key] = min(self.data.get(key, 0) + quantity, settings.CART_MAX_QTY)
        self._save()

    def set(self, variant_id, quantity):
        key = str(variant_id)
        if quantity <= 0:
            self.data.pop(key, None)
        else:
            self.data[key] = min(quantity, settings.CART_MAX_QTY)
        self._save()

    def remove(self, variant_id):
        self.data.pop(str(variant_id), None)
        self._save()

    def clear(self):
        self.data = {}
        self._save()

    def lines(self):
        ids = [int(k) for k in self.data]
        variants = Variant.objects.filter(id__in=ids, is_active=True, product__is_active=True).select_related("product")
        by_id = {v.id: v for v in variants}
        lines = []
        for key, quantity in self.data.items():
            variant = by_id.get(int(key))
            if variant is None:
                continue
            stock = variant.stock
            lines.append(
                {
                    "variant": variant,
                    "quantity": quantity,
                    "unit_price": variant.price,
                    "line_total": variant.price * quantity,
                    "stock": stock,
                    "short": quantity > stock,
                }
            )
        return lines
