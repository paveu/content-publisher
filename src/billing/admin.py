from django.contrib import admin
from .models import Membership, Transaction, UserMerchantId, TransactionPayu

class TransactionPayuAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    
# Register your models here.
admin.site.register(Membership)
admin.site.register(Transaction)
admin.site.register(TransactionPayu, TransactionPayuAdmin)
admin.site.register(UserMerchantId)
