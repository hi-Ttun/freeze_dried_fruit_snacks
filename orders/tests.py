from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from shop.models import Category, Lot, Product, Variant

from .models import Order, Payment
from .services import CheckoutError, place_order, shipping_fee_for

CUSTOMER = {
    "name": "Nguyễn Văn A",
    "phone": "0901234567",
    "email": "a@example.com",
    "address": "1 Lê Lợi, Quận 1, TP.HCM",
    "zone": Order.Zone.URBAN,
    "note": "",
}


def make_lot(variant, code, days, qty):
    today = timezone.localdate()
    return Lot.objects.create(
        variant=variant, code=code, produced_on=today, expires_on=today + timedelta(days=days), quantity_in=qty
    )


class OrderTestBase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Trái cây sấy", slug="trai-cay-say")
        product = Product.objects.create(category=category, name="Xoài sấy", slug="xoai-say")
        self.variant = Variant.objects.create(product=product, label="50g", weight_g=50, price=100000, sku="TEST-50")
        self.near = make_lot(self.variant, "L-NEAR", 10, 5)  # dưới hạn tối thiểu, không bán
        self.early = make_lot(self.variant, "L-EARLY", 45, 5)
        self.late = make_lot(self.variant, "L-LATE", 200, 5)

    def reload(self, *lots):
        for lot in lots:
            lot.refresh_from_db()


class FefoTests(OrderTestBase):
    def test_allocates_earliest_sellable_lot_first(self):
        order = place_order(items=[(self.variant.id, 7)], customer=CUSTOMER, payment_method="cod")
        self.reload(self.near, self.early, self.late)
        self.assertEqual(self.early.quantity_left, 0)
        self.assertEqual(self.late.quantity_left, 3)
        self.assertEqual(self.near.quantity_left, 5)  # lô cận hạn không bị bán
        self.assertEqual(order.subtotal, 700000)
        self.assertEqual(order.shipping_fee, 0)  # đạt ngưỡng miễn phí vận chuyển

    def test_insufficient_stock_raises_and_keeps_inventory(self):
        with self.assertRaises(CheckoutError):
            place_order(items=[(self.variant.id, 11)], customer=CUSTOMER, payment_method="cod")
        self.reload(self.early, self.late)
        self.assertEqual((self.early.quantity_left, self.late.quantity_left), (5, 5))
        self.assertEqual(Order.objects.count(), 0)

    def test_empty_cart_raises(self):
        with self.assertRaises(CheckoutError):
            place_order(items=[], customer=CUSTOMER, payment_method="cod")

    def test_shipping_fee_rules(self):
        self.assertEqual(shipping_fee_for(Order.Zone.URBAN, 100000), 22000)
        self.assertEqual(shipping_fee_for(Order.Zone.OTHER, 100000), 35000)
        self.assertEqual(shipping_fee_for(Order.Zone.OTHER, 500000), 0)


class OrderLifecycleTests(OrderTestBase):
    def make_order(self, quantity=7, method="cod"):
        return place_order(items=[(self.variant.id, quantity)], customer=CUSTOMER, payment_method=method)

    def test_invalid_transition_rejected(self):
        order = self.make_order()
        with self.assertRaises(ValueError):
            order.change_status(Order.Status.DELIVERED)

    def test_cancel_restocks_original_lots(self):
        order = self.make_order()
        order.change_status(Order.Status.CANCELLED)
        self.reload(self.early, self.late)
        self.assertEqual((self.early.quantity_left, self.late.quantity_left), (5, 5))
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CANCELLED)
        self.assertEqual(order.payment.status, Payment.Status.FAILED)

    def test_cod_order_full_flow_marks_payment_paid_on_delivery(self):
        order = self.make_order()
        for status in ("confirmed", "packing", "shipping", "delivered", "completed"):
            order.change_status(status)
        order.refresh_from_db()
        self.assertEqual(order.payment.status, Payment.Status.PAID)
        self.assertIsNotNone(order.shipment.shipped_at)
        self.assertIsNotNone(order.shipment.delivered_at)
        self.assertEqual(order.history.count(), 6)

    def test_bank_order_marks_paid_when_status_paid(self):
        order = self.make_order(method="bank")
        order.change_status("confirmed")
        order.change_status("paid")
        order.refresh_from_db()
        self.assertEqual(order.payment.status, Payment.Status.PAID)
        self.assertIsNotNone(order.payment.paid_at)

    def test_cannot_cancel_after_shipping(self):
        order = self.make_order()
        for status in ("confirmed", "packing", "shipping"):
            order.change_status(status)
        with self.assertRaises(ValueError):
            order.change_status(Order.Status.CANCELLED)


class StorefrontFlowTests(OrderTestBase):
    form_data = {
        "customer_name": "Nguyễn Văn A",
        "phone": "0901 234 567",
        "email": "",
        "address": "1 Lê Lợi, Quận 1, TP.HCM",
        "zone": "urban",
        "payment_method": "cod",
        "note": "",
    }

    def test_cart_checkout_and_access_control(self):
        self.client.post(reverse("cart_add", args=[self.variant.id]), {"quantity": "2"})
        self.assertEqual(self.client.get(reverse("cart")).status_code, 200)
        response = self.client.post(reverse("checkout"), self.form_data)
        order = Order.objects.get()
        self.assertRedirects(response, f"{reverse('order_detail', args=[order.code])}?placed=1")
        self.assertEqual(order.total, 222000)  # 2 x 100.000 + phí vận chuyển nội thành
        self.assertEqual(order.phone, "0901234567")

        # Người khác không xem được đơn nếu không có mã và số điện thoại
        stranger = Client()
        self.assertEqual(stranger.get(reverse("order_detail", args=[order.code])).status_code, 404)
        # Tra cứu đúng mã + số điện thoại thì xem được
        found = stranger.post(reverse("order_lookup"), {"code": order.code.lower(), "phone": "0901234567"})
        self.assertRedirects(found, reverse("order_detail", args=[order.code]))
        # Tra cứu sai số điện thoại thì không thấy
        wrong = Client().post(reverse("order_lookup"), {"code": order.code, "phone": "0911111111"})
        self.assertContains(wrong, "Không tìm thấy đơn hàng")

    def test_checkout_with_empty_cart_redirects(self):
        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("product_list"))

    def test_invalid_phone_rejected(self):
        self.client.post(reverse("cart_add", args=[self.variant.id]), {"quantity": "1"})
        data = dict(self.form_data, phone="123")
        response = self.client.post(reverse("checkout"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)

    def test_dashboard_requires_staff(self):
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)


class PayOSTests(OrderTestBase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_payos_checkout_and_ipn_flow(self):
        order = place_order(items=[(self.variant.id, 2)], customer=CUSTOMER, payment_method="bank")
        self.assertEqual(order.payment.method, "bank")
        self.assertEqual(order.payment.status, Payment.Status.PENDING)
        self.assertIsNotNone(order.payment.payos_order_code)

        # 1. API kiểm tra trạng thái thanh toán realtime ban đầu
        status_res = self.client.get(reverse("order_payment_status", args=[order.code]))
        self.assertEqual(status_res.status_code, 200)
        self.assertFalse(status_res.json()["is_paid"])

        # 2. Giả lập webhook IPN từ PayOS gửi về server
        ipn_payload = {
            "code": "00",
            "desc": "success",
            "data": {
                "orderCode": order.payment.payos_order_code,
                "amount": order.total,
                "description": f"NutriSnack {order.code}",
                "accountNumber": "123456789",
                "reference": "PAYOS_REF_9999",
                "transactionDateTime": "2026-11-12 17:00:00",
                "currency": "VND",
                "paymentLinkId": "plink_test_123",
                "code": "00",
                "desc": "success",
            },
            "signature": "test_signature",
        }
        import json
        ipn_res = self.client.post(
            reverse("payos_ipn"),
            data=json.dumps(ipn_payload),
            content_type="application/json",
        )
        self.assertEqual(ipn_res.status_code, 200)
        self.assertEqual(ipn_res.json()["code"], "00")

        # Đơn hàng và thanh toán đã tự động chuyển sang PAID
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)
        self.assertEqual(order.payment.status, Payment.Status.PAID)
        self.assertEqual(order.payment.reference, "PAYOS_REF_9999")

        # 3. Client polling API nhận được trạng thái mới theo realtime
        status_res_after = self.client.get(reverse("order_payment_status", args=[order.code]))
        self.assertTrue(status_res_after.json()["is_paid"])
        self.assertEqual(status_res_after.json()["status_display"], "Đã thanh toán")

    def test_payos_simulate_payment_endpoint(self):
        order = place_order(items=[(self.variant.id, 1)], customer=CUSTOMER, payment_method="bank")
        sim_res = self.client.post(reverse("payos_simulate_payment", args=[order.code]))
        self.assertEqual(sim_res.status_code, 200)
        self.assertTrue(sim_res.json()["success"])

        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)
        self.assertEqual(order.payment.status, Payment.Status.PAID)

