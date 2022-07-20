from django.contrib import admin
from .models import *
# Register your models here.


class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "price", "completed")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "image")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product_price", "table_number", "table_completed")

    def table_number(self, obj):
        return obj.table.table_number

    def table_completed(self, obj):
        return obj.table.completed

    def product_name(self, obj):
        return obj.product.name

    def product_price(self, obj):
        return obj.product.price

admin.site.register(Table, TableAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)

