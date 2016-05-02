import datetime
import requests
from django.conf import settings
from django.utils import timezone

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

from .signals import membership_dates_update


def check_membership_status(subscription_id):
    """
    this function check status of a current subscription and returns its status
    and next billing date
    """
    sub = braintree.Subscription.find(subscription_id)
    if sub.status == "Active":
        status = True
        next_billing_date = sub.next_billing_date
    else:
        status = False
        next_billing_date = None
    # checking in braintree
    return status, next_billing_date


def update_braintree_membership(user):
    """
    Updates premium membership account with new end date. If subscription is
    not active then it marks MyUser.s_member as a False.
    
    This function is run everytime when user is logged in.
    """
    user = user
    membership = user.membership
    now = timezone.now()
    subscription_id = user.usermerchantid.subscription_id
    
    # update premium account end time based on information coming from
    # braintree subscription end time value
    if membership.date_end <= timezone.now() and subscription_id is not None:
        status, next_billing_date = check_membership_status(subscription_id)
        # if subscription is active and customer was charged then calculate
        # new end time
        if status:
            # next_billing_date returns only date which is not datetime obj
            # so convert it to datetime obj
            small_time = datetime.time(0, 0, 0, 1)
            datetime_obj = datetime.datetime.combine(next_billing_date,
                                                     small_time)
            datetime_aware = timezone.make_aware(datetime_obj,
                                                 timezone.get_current_timezone())

            # update premium account(membership) with new start time date
            # update_membership_dates receiver exists in billing/models.py
            membership_dates_update.send(membership,
                                         new_date_start=datetime_aware)
        # if not active, then update status and mark is_member as a False
        else:
            membership.update_status()
    elif subscription_id is None:
        membership.update_status()
    else:
        pass

def get_oauth_token():
    """
    Getting oauth token
    """
    OAUTH_URL = 'https://secure.payu.com/pl/standard/user/oauth/authorize'
    oauth_request_data = {
        'grant_type': 'client_credentials',
        'client_id': settings.PAYU_POS_ID,
        'client_secret': settings.PAYU_MD5_KEY
    }
    try:
        oauth_request = requests.post(OAUTH_URL, data=oauth_request_data)
        response = oauth_request.json()
        return response['access_token']
    except:
        return False