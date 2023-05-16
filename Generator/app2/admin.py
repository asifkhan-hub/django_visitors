from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Customer,
    Visitor,
)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Password_Name', 'Password']

@admin.register(Visitor)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [ 'ip_address', 'timestamp','visited_page','notification_sent']


