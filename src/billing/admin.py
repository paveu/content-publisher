from django.contrib import admin
from .models import Membership, Transaction, UserMerchantId, TransactionPayu


class TransactionPayuAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    list_display = ('user', 'order_id', 'extorder_id', 'timestamp','transaction_status', 'customer_ip')


class TransactionBraintreeAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'transaction_id', 'timestamp', 'transaction_status')


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_start', 'date_end')
  
class UserMerchantIdAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer_id', 'subscription_id', 'plan_id', 'merchant_name')
   
# Register your models here.
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Transaction, TransactionBraintreeAdmin)
admin.site.register(TransactionPayu, TransactionPayuAdmin)
admin.site.register(UserMerchantId, UserMerchantIdAdmin)
