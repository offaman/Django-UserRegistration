from django.contrib import admin
from accounts.models import Account, authTokenModel


admin.site.register(Account)
admin.site.register(authTokenModel)