from django.contrib import messages

from .models import CouponCode


def get_discounted_amount(price,code,request)->int:
    razorpay_conversion_factor = 100
    if code:
        coupon_code = CouponCode.objects.filter(code=code)
        if coupon_code.exists():
            discount = coupon_code.last().discount
            messages.success(request,f"Successfully applied a discount of {discount}%")
            discounted_amount = price - ((price*discount)/100)
            return discounted_amount * razorpay_conversion_factor
        messages.error(request,f"Oops, looks like this coupon code is no longer valid!")
    return price * razorpay_conversion_factor