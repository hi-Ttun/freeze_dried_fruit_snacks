import re

from django import forms

from .models import Order, Payment


def normalize_phone(raw):
    digits = re.sub(r"[^\d+]", "", raw or "")
    if digits.startswith("+84"):
        digits = "0" + digits[3:]
    elif digits.startswith("84") and len(digits) == 11:
        digits = "0" + digits[2:]
    return digits


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(label="Họ và tên người nhận", max_length=120)
    phone = forms.CharField(label="Số điện thoại", max_length=20)
    email = forms.EmailField(label="Email (để nhận thông tin đơn hàng)", required=False)
    address = forms.CharField(label="Địa chỉ giao hàng", widget=forms.Textarea(attrs={"rows": 3}))
    zone = forms.ChoiceField(label="Khu vực giao hàng", choices=Order.Zone.choices)
    payment_method = forms.ChoiceField(label="Phương thức thanh toán", choices=Payment.Method.choices, widget=forms.RadioSelect)
    note = forms.CharField(label="Ghi chú cho cửa hàng", max_length=255, required=False)

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data["phone"])
        if not re.fullmatch(r"0\d{9,10}", phone):
            raise forms.ValidationError("Số điện thoại chưa đúng. Ví dụ: 0901234567.")
        return phone


class OrderLookupForm(forms.Form):
    code = forms.CharField(label="Mã đơn hàng", max_length=20)
    phone = forms.CharField(label="Số điện thoại đặt hàng", max_length=20)

    def clean_code(self):
        return self.cleaned_data["code"].strip().upper()

    def clean_phone(self):
        return normalize_phone(self.cleaned_data["phone"])
