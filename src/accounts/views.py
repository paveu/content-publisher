from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from billing.models import Transaction, TransactionPayu
from notifications.models import Notification

from .models import MyUser
from .forms import LoginForm, RegisterForm
# Create your views here.


@login_required
def account_home(request):
    notifications = Notification.objects.get_recent_for_user(request.user)
    braintreeHistory = Transaction.objects.get_recent_for_user(request.user, 3)
    payuHistory = TransactionPayu.objects.get_recent_for_user(request.user, 3)
    
    return render(request, "account/account_home.html", {"braintreeHistory": braintreeHistory, 
                                                    "payuHistory": payuHistory,
                                                    "notifications": notifications
    })


# def auth_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/')


# def auth_login(request):
#     form = LoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         # returns already created user in db or None
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect('/')

#     context = {"form": form,
#               }
#     return render(request, "accounts/account_login.html", context)


# def auth_register(request):
#     form = RegisterForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data['username']
#         email = form.cleaned_data['email']
#         password = form.cleaned_data['password2']

#         # MyUser.objects.create_user(username=username, email=email, password=password)
#         new_user = MyUser()
#         new_user.username = username
#         new_user.email = email
#         new_user.set_password(password)
#         new_user.save()

#     action_url = reverse("register")
#     context = {"form": form,
#               }
#     return render(request, "accounts/account_register.html", context)

