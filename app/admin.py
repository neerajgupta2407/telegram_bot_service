from django.contrib import admin

from .models import ABC, State, District, TelegramUser
# Register your models here.

admin.site.register(ABC)
admin.site.register(State)
admin.site.register(District)
admin.site.register(TelegramUser)