from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("san-pham/", views.product_list, name="product_list"),
    path("san-pham/<slug:slug>/", views.product_detail, name="product_detail"),
    path("truy-xuat/", views.trace, name="trace"),
    path("gioi-thieu/", TemplateView.as_view(template_name="shop/about.html"), name="about"),
    path("chinh-sach/doi-tra/", TemplateView.as_view(template_name="shop/policy_returns.html"), name="policy_returns"),
    path("chinh-sach/bao-mat/", TemplateView.as_view(template_name="shop/policy_privacy.html"), name="policy_privacy"),
    path("chinh-sach/dieu-khoan/", TemplateView.as_view(template_name="shop/policy_terms.html"), name="policy_terms"),
    # Chatbot AI & Human Handoff API
    path("api/chat/", views.chat_message, name="chat_message"),
    path("api/chat/lead/", views.chat_lead, name="chat_lead"),
]
