import datetime
import random

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from .signals import membership_dates_update
from .utils import update_braintree_membership
# Create your models here.


def user_logged_in_receiver(sender, user, **kwargs):
    """
    It updates project membership account with braintree membership end time
    It will be run whenever user logs in.
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
    date_start = models.DateTimeField(default=timezone.now,
                                      verbose_name='Start Date')
    date_end = models.DateTimeField(default=timezone.now,
                                    verbose_name='End Date')

    def __unicode__(self):
        return str(self.user.username)

    def update_status(self):
        """
        Checking whether user is a member or not
        """
        # if end date is greater or equal with current date then
        # mark user as member 
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
        
    class Meta:
        verbose_name_plural = "Memberships"
        
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
    """
    It actually updates membership time for particular account when
    new transaction is made. So this signal method is bound to transactions
    """
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
    Custumized version of creatig new object for Transaction model
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
    
    # customerIp
    # merchantPosId
    objects = TransactionManager()

    def __unicode__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'braintree_payment'
        verbose_name_plural = 'braintree_payments'


class TransactionPayuManager(models.Manager):
    """
    Custumized version of creatig new object for TransactionPayuManager model
    """
    def all_for_user(self, user):
        return super(TransactionPayuManager, self).filter(user=user)

    def get_recent_for_user(self, user, num):
        return super(TransactionPayuManager, self).filter(user=user)[:num]

STATUS_CHOICES = (
    ('NEW', 'New'),
    ('PENDING', 'Pending'),
    ('WAITING_FOR_CONFIRMATION', 'Waiting for confirmation'),
    ('COMPLETED', 'Completed'),
    ('CANCELED', 'Canceled'),
    ('REJECTED', 'Rejected'),
)

class TransactionPayu(models.Model):
    """
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # payu order id coming from payu payment system
    order_id = models.CharField(max_length=255)
    # our own internal order id
    extorder_id = models.CharField(max_length=120, null=True, blank=True)
    # total cost for a product
    amount = models.CharField(max_length=8, null=True, blank=True)
    # created time
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    transaction_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='NEW')
    # products = JSONField('products', default='', blank=True)
    pos_id = models.CharField(max_length=255, null=True, blank=True)
    customer_ip = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # notes = models.TextField('notes', null=True, blank=True)

    objects = TransactionPayuManager()
    
    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'payu_payment'
        verbose_name_plural = 'payu_payments'

    def __unicode__(self):
        return self.order_id

class UserMerchantId(models.Model):
    """
    It stores information about braintree customer on this site.
    it keeps braintree_id plan_id and subscription_id. All
    these information are coming from Braintree
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # braintree customer id
    customer_id = models.CharField(max_length=120)
    # braintree subscription_id taken from braintree subscription
    subscription_id = models.CharField(max_length=120, null=True, blank=True)
    # braintree monthly plan
    plan_id = models.CharField(max_length=120, null=True, blank=True)
    # braintree merchant name
    merchant_name = models.CharField(max_length=120, default="Braintree")
    # payu add pos id
    # pos_id = models.CharField('PayU POS ID', max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.customer_id

    class Meta:
        verbose_name = 'UserMerchantId'
        verbose_name_plural = 'UserMerchantIds'