from django.contrib import admin
from .models import Order, Item, Price, Currency


admin.site.register(Currency)
admin.site.register(Price)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item 
    readonly_fields = ('stripe_id', )


class ItemInlineAdmin(admin.TabularInline):
    model = Item
    fields = ("name", "price")
    classes = ('extrapretty')
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order 
    