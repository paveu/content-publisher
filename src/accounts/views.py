from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from billing.models import Transaction, TransactionPayu
from notifications.models import Notification
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import MyUser
# Create your views here.


@login_required
def account_dashboard(request):
    notifications = Notification.objects.get_recent_for_user(request.user)
    braintreeHistory = Transaction.objects.get_recent_for_user(request.user, 5)
    payuHistory = TransactionPayu.objects.get_recent_for_user(request.user, 5)
    
    return render(request, "account/account_dashboard.html", {
        "braintreeHistory": braintreeHistory,
        "payuHistory": payuHistory,
        "notifications": notifications,
    })

#TODO
@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_(request, user, **kwargs):
    # user signed up now send email
    # send email part - do your self
    print("new user")

