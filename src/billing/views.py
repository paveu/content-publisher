import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404
from django.utils import timezone

# Create your views here.
from .models import Transaction, Membership, UserMerchantId
from .signals import membership_dates_update

import braintree

# it's in sandbox mode if you want to turn it into prodiciton change this line
braintree.Configuration.configure(braintree.Environment.Sandbox, 
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

# it defines how often it charges customers. Recurring billing for subscription
PLAN_ID = "monthly_plan"

@login_required
def cancel_subscription(request):
    """
    It canceles subscription based on saved sub_ui in django.merchant model
    """
    sub_id = request.user.usermerchantid.subscription_id
    if sub_id:
        result = braintree.Subscription.cancel(sub_id)
        if result.is_success:
            request.user.usermerchantid.subscription_id = None
            request.user.usermerchantid.save()
            messages.success(request, "Your account has been successfully cancelled")
        else:
            messages.error(request, "There was an error with your account, please contact us")
    else:
        messages.success(request, "You do not have an active subscription")
    return redirect("billing_history")


@login_required
def upgrade(request):
    """
    It upgrades regular user account into premium one. It is done based
    on transaction information.
    """
    if request.user.is_authenticated():
        try:
            # get the UserMerchantId object where braintree 'customer id' is stored
            # UserMerchantId object is created in accounts/models.py in new_user_receiver()
            merchant_obj = UserMerchantId.objects.get(user=request.user)
        except:
            messages.error(request, "There was an error with your account. Please contact us.")
            return redirect("contact_us")
    
        # get braintree 'customer_id' stored in merchant_obj
        merchant_customer_id = merchant_obj.customer_id
        
        # client_taken is needed for javascript frontend.
        # it's gonna be rendered into JS code based on 'merchant_customer_id'.
        # client token is useful to identify customer already existed in database
        client_token = braintree.ClientToken.generate({
                                                       "customer_id": merchant_customer_id
                                                    })
        if request.method == "POST":
            # 'nonce' is a unique token of credit card generated after filling in
            # braintree java script payment form
            nonce = request.POST.get("payment_method_nonce", None)
            if nonce is None:
                messages.error(request, "An error occured, please try again filling in braintree form")
                return redirect("account_upgrade")
            else:
                # create a payment method for the new subscription
                # we need it because we have few payment methods: credit card or paypal
                payment_method_result = braintree.PaymentMethod.create({
                    "customer_id": merchant_customer_id,
                    "payment_method_nonce": nonce,
                    "options": {
                                "make_default": True
                    }
                })
                if not payment_method_result.is_success:
                    messages.error(request, "An error occured: %s" % payment_method_result.message)
                    return redirect("account_upgrade")
                
                # payment method token which turns out to be a default one
                the_token = payment_method_result.payment_method.token
                
                # current_sub_id and current_plan_id will be used to check
                # whether a merchant has an active subscription, if it's not 
                # active then we gonna charge his Credit Card or Paypal
                # if it is active then nothing happens.
                # To check this out we need merchant play_id and sub_uid
                current_sub_id = merchant_obj.subscription_id
                current_plan_id = merchant_obj.plan_id
                
                did_create_sub = False
                did_update_sub = False
                # trans_success = False
                # trans_timestamp = None

                try:
                    # find current subscription and get its status
                    current_subscription = braintree.Subscription.find(current_sub_id)
                    sub_status = current_subscription.status
                except:
                    current_subscription = None
                    sub_status = None
                
                # if there is an active subscription then update braintree subscription
                # and take its status
                if current_subscription and sub_status == "Active":
                    update_sub = braintree.Subscription.update(current_sub_id, {
                            "payment_method_token": the_token,
                    })
                    did_update_sub = True
                # if subscription expired then charge him/her again based on 
                # payment token and PLAN_ID(monthly).
                else:
                    create_sub = braintree.Subscription.create({
                            "payment_method_token": the_token,
                            "plan_id": PLAN_ID
                    })
                    did_create_sub = True

                if did_create_sub or did_update_sub:
                    membership_instance, created = Membership.objects.get_or_create(user=request.user)

                if did_update_sub and not did_create_sub:
                    messages.success(request, "Your plan has been updated")
                    # membership_dates_update signal is used to update membership
                    # premium account with start time
                    membership_dates_update.send(membership_instance,
                                                 new_date_start=timezone.now())
                    return redirect("account_upgrade")
                elif did_create_sub and not did_update_sub:
                    merchant_obj.subscription_id = create_sub.subscription.id
                    merchant_obj.plan_id = PLAN_ID
                    merchant_obj.save()
                    
                    # get most recent transaction bound to subscription
                    bt_tran = create_sub.subscription.transactions[0]
                    # create a new transaction instance in project Transaction model
                    new_tran, created = get_or_create_model_transaction(request.user, bt_tran)
                    trans_success = False
                    trans_timestamp = None
                    
                    if created:
                        trans_timestamp = new_tran.timestamp
                        trans_success = new_tran.success

                    membership_dates_update.send(membership_instance,
                                                 new_date_start=trans_timestamp)
                    messages.success(request, "Welcome to our service")
                    return redirect("billing_history")
                else:
                    messages.error(request, "An error occured, please try again.")
                    return redirect("account_upgrade")

    context = {"client_token": client_token}
    return render(request, "billing/upgrade.html", context)


def get_or_create_model_transaction(user, braintree_transaction):
    """
    It gets already created Transaction instance or creates a new one
    based on braintree subscription
    """
    trans_id = braintree_transaction.id
    try:
        trans = Transaction.objects.get(user=user, transaction_id=trans_id)
        created = False
    except:
        created = True
        # 'payment_instrument_type' is a way how we made transaction either paypal or credit card
        payment_type = braintree_transaction.payment_instrument_type
        amount = braintree_transaction.amount

        # PaymentInstrumentType prints out what type of payment was issued
        if payment_type == braintree.PaymentInstrumentType.PayPalAccount:
            trans = Transaction.objects.create_new(user, trans_id, amount, "Paypal")

        elif payment_type == braintree.PaymentInstrumentType.CreditCard:
            credit_card_details = braintree_transaction.credit_card_details
            card_type = credit_card_details.card_type
            last_4 = credit_card_details.last_4
            trans = Transaction.objects.create_new(user,
                                                   trans_id,
                                                   amount,
                                                   card_type,
                                                   last_four=last_4)
        else:
            created = False
            trans = None
    return trans, created


def update_transaction(user):
    """
    The main reason to have this function is to have synchronzied transaction
    between braintree.transacations and django.transaction model
    
    It checks whether billing_history() function has up-to-dated history.
    If it's not up to dated if it doesn't have all transactions stored in
    django transaction model then interate through braintree.transaction and take
    those missing transaction and save it to django.transaction model.
    """
    # bt_transactions object returns generator
    bt_transactions = braintree.Transaction.search(
                braintree.TransactionSearch.customer_id == user.usermerchantid.customer_id)
    try:
        django_transactions = user.transaction_set.all()
    except:
        django_transactions = None
        
    if bt_transactions is not None and django_transactions is not None:
        if bt_transactions.maximum_size <= django_transactions.count():
            pass
        else:
            for bt_tran in bt_transactions.items:
                new_tran, created = get_or_create_model_transaction(user, bt_tran)


@login_required
def billing_history(request):
    """
    It prints out all successful transactions associated with particular user
    """
    update_transaction(request.user)
    history = Transaction.objects.filter(user=request.user).filter(success=True)
    return render(request, "billing/history.html", {"queryset": history})
