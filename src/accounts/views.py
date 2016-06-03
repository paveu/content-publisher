from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from billing.models import Transaction, TransactionPayu
from notifications.models import Notification

from .models import MyUser
# Create your views here.


@login_required
def account_home(request):
    notifications = Notification.objects.get_recent_for_user(request.user)
    braintreeHistory = Transaction.objects.get_recent_for_user(request.user, 3)
    payuHistory = TransactionPayu.objects.get_recent_for_user(request.user, 3)
    
    return render(request, "account/account_home.html", {
        "braintreeHistory": braintreeHistory,
        "payuHistory": payuHistory,
        "notifications": notifications,
        "FeedbackForm": FeedbackForm
    })


