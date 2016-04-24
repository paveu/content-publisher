import datetime
import random

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
# from django.contrib.messages.api import success

from .signals import membership_dates_update
from .utils import update_braintree_membership
# Create your models here.


def user_logged_in_receiver(sender, user, **kwargs):
    """
    """
    try:
        update_braintree_membership(user)
    except:
        pass

user_logged_in.connect(user_logged_in_receiver)


class Membership(models.Model):
    """
    Check whether user has a premium account
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_start = models.DateTimeField(default=timezone.now(),
                                      verbose_name='Start Date')
    date_end = models.DateTimeField(default=timezone.now(),
                                    verbose_name='End Date')

    def __unicode__(self):
        return str(self.user.username)

    def update_status(self):
        if self.date_end >= timezone.now():
            self.user.is_member = True
            self.user.save()
        # if user premium account is expired then mark its membership
        # account as a false
        elif self.date_end < timezone.now():
            self.user.is_member = False
            self.user.save()
        else:
            pass


def update_membership_status(sender, **kwargs):
    """
    Update membership status just after you save changes on the
    Membership model
    """
    created = kwargs['created']
    instance = kwargs['instance']

    if not created:
        instance.update_status()

post_save.connect(update_membership_status, sender=Membership)


def update_membership_dates(sender, new_date_start, **kwargs):
    membership = sender
    current_date_end = membership.date_end

    if current_date_end >= new_date_start:
        # append new_start date plus offset to date end of the instance
        membership.date_end = current_date_end + datetime.timedelta(days=30,
                                                                    hours=10)
        membership.save()
    else:
        # set a new start date and new end date with the same offset
        membership.date_start = new_date_start
        membership.date_end = new_date_start + datetime.timedelta(days=30,
                                                                  hours=10)
        membership.save()
#     membership.update_status()

membership_dates_update.connect(update_membership_dates)


class TransactionManager(models.Manager):
    """
    """
    def create_new(self,
                   user,
                   transaction_id,
                   amount,
                   card_type,
                   success=None,
                   transaction_status=None,
                   last_four=None):
        if not user:
            raise ValueError("Must be a user")

        if not user:
            raise ValueError("Must complete a transaction to add new")
        
        # Create an order id based on our unique ID
        new_order_id = "%s%s%s" % (transaction_id[:2],
                                   random.randint(1, 9),
                                   transaction_id[2:])
        new_trans = self.model(
            user=user,
            transaction_id=transaction_id,
            order_id=new_order_id,
            amount=amount,
            card_type=card_type,
        )
        if success is not None:
            new_trans.success = success
            new_trans.transaction_status = transaction_status
        if last_four is not None:
            new_trans.last_four = last_four

        new_trans.save(using=self._db)
        return new_trans

    def all_for_user(self, user):
        return super(TransactionManager, self).filter(user=user)

    def get_recent_for_user(self, user, num):
        return super(TransactionManager, self).filter(user=user)[:num]


class Transaction(models.Model):
    """
    This model is used to track all transaction that was issued by credit card.
    It keeps sucessfull and failures transactions.
    It's not supposed to store subscription info, it's only to storing transaction history
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # braintree, stripe or payu transaction id that comes from those systems
    transaction_id = models.CharField(max_length=120)
    # we gonna create our own order_id based on transaction_id field
    # it's usefull for not not using internal payment system id but rather ours
    order_id = models.CharField(max_length=120)
    # how much we actually we are charging them(customers) for. It's final amount.
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    # we will store information whether transaction was actually success or not
    success = models.BooleanField(default=True)
    # if fails store transaction status
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    # we make card_type field as a CharField just beacause it can turn to be paypal
    card_type = models.CharField(max_length=120)
    # we do same sas above, if we get paypal then we can't provide any last_four
    # digits
    last_four = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = TransactionManager()

    def __unicode__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']


class UserMerchantId(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    customer_id = models.CharField(max_length=120)
    subscription_id = models.CharField(max_length=120, null=True, blank=True)
    plan_id = models.CharField(max_length=120, null=True, blank=True)
    merchant_name = models.CharField(max_length=120, default="Braintree")

    def __unicode__(self):
        return self.customer_id
