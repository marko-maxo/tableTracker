from rest_framework import serializers
from .models import Table, Order, Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "image", "price", "name"]
    def get_image(self, member):
        return member.image.url

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "timestamp", "product_name", "price"]

    def get_product_name(self, member):
        return member.product.name

    def get_price(self, member):
        return member.product.price


class TableSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = "__all__"
        extra_fields = ["orders"]
    
    def get_orders(self, member):
        orders = Order.objects.filter(table_id=member.id)
        if orders:
            return OrderSerializer(orders, many=True).data
        else:
            return False