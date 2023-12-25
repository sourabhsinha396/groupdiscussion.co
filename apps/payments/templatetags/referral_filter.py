from django import template

from ..models import Credit


register = template.Library()

@register.filter(name='user_referral_credit')
def user_referral_credit(user):
    return sum(credit.amount for credit in user.credits.all())