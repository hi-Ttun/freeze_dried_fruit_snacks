from django.urls import path

from . import views

urlpatterns = [
    path("gio-hang/", views.cart_detail, name="cart"),
    path("gio-hang/them/<int:variant_id>/", views.cart_add, name="cart_add"),
    path("gio-hang/cap-nhat/<int:variant_id>/", views.cart_update, name="cart_update"),
    path("gio-hang/xoa/<int:variant_id>/", views.cart_remove, name="cart_remove"),
    path("thanh-toan/", views.checkout, name="checkout"),
    path("thanh-toan/payos/ipn/", views.payos_ipn, name="payos_ipn"),
    path("thanh-toan/payos/ket-qua/", views.payos_return, name="payos_return"),
    path("thanh-toan/payos/huy/", views.payos_cancel, name="payos_cancel"),
    path("thanh-toan/payos/simulate/<str:code>/", views.payos_simulate_payment, name="payos_simulate_payment"),
    path("don-hang/", views.my_orders, name="my_orders"),
    path("don-hang/tra-cuu/", views.order_lookup, name="order_lookup"),
    path("don-hang/<str:code>/", views.order_detail, name="order_detail"),
    path("don-hang/<str:code>/payment-status/", views.order_payment_status, name="order_payment_status"),
    path("quan-tri/bao-cao/", views.dashboard, name="dashboard"),
]
