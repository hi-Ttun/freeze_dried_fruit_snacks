from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Lot, Product, Variant


class ShopPagesTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Trái cây sấy", slug="trai-cay-say")
        self.product = Product.objects.create(
            category=category, name="Xoài sấy thăng hoa", slug="xoai-say", short_description="Giòn ngọt", is_featured=True
        )
        self.variant = Variant.objects.create(product=self.product, label="30g", weight_g=30, price=55000, sku="T-30")
        today = timezone.localdate()
        self.lot = Lot.objects.create(
            variant=self.variant, code="T-30-L1", produced_on=today, expires_on=today + timedelta(days=200), quantity_in=10
        )

    def test_lot_quantity_left_defaults_to_quantity_in(self):
        self.assertEqual(self.lot.quantity_left, 10)

    def test_home_lists_featured_product(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Xoài sấy thăng hoa")

    def test_product_list_search(self):
        self.assertContains(self.client.get(reverse("product_list"), {"q": "Xoài"}), "Xoài sấy thăng hoa")
        self.assertNotContains(self.client.get(reverse("product_list"), {"q": "khongco"}), "Xoài sấy thăng hoa")

    def test_product_detail(self):
        response = self.client.get(reverse("product_detail", args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "55.000₫")
        self.assertContains(response, "T-30-L1")

    def test_inactive_product_is_404(self):
        self.product.is_active = False
        self.product.save()
        self.assertEqual(self.client.get(reverse("product_detail", args=[self.product.slug])).status_code, 404)

    def test_trace_found_and_not_found(self):
        self.assertContains(self.client.get(reverse("trace"), {"code": "t-30-l1"}), "T-30-L1")
        self.assertContains(self.client.get(reverse("trace"), {"code": "SAI"}), "Không tìm thấy lô")

    def test_variant_stock_ignores_lots_with_short_shelf_life(self):
        today = timezone.localdate()
        Lot.objects.create(variant=self.variant, code="SHORT", produced_on=today, expires_on=today + timedelta(days=5), quantity_in=50)
        self.assertEqual(self.variant.stock, 10)

    def test_chat_message_ai_response(self):
        response = self.client.post(
            reverse("chat_message"),
            data='{"message": "Sầu riêng sấy có ngọt không?"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reply", data)
        self.assertFalse(data.get("is_handoff", True))

    def test_chat_message_triggers_human_handoff(self):
        response = self.client.post(
            reverse("chat_message"),
            data='{"message": "Cho tôi gặp nhân viên tư vấn trực tiếp"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("is_handoff", False))
        self.assertIn("handoff_info", data)

    def test_chat_lead_submission(self):
        from .models import ConsultationLead
        response = self.client.post(
            reverse("chat_lead"),
            data='{"phone": "0912345678", "customer_name": "Nguyen Van A", "note": "Hỏi giá sỉ 100 hộp"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        lead = ConsultationLead.objects.filter(phone="0912345678").first()
        self.assertIsNotNone(lead)
        self.assertEqual(lead.customer_name, "Nguyen Van A")

