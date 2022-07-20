from ast import Delete
from cgitb import lookup
from importlib.resources import read_text
from django.forms import model_to_dict
from django.shortcuts import render
from psycopg2 import Timestamp
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import generics
from .serializers import *
from userManagement.authClasses import *
from .models import Table, Order, Product
from datetime import datetime
import time
from django.db.models import Sum
# Create your views here.

class TableViewsetNotCompleted(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    authentication_classes = [JWTCookieUserAuthentication, ]
    serializer_class = TableSerializer
    lookup_field = "table_number"
    queryset = Table.objects.filter(completed=False).order_by("table_number")

    
class TodayTableInfo(viewsets.ViewSet, generics.ListAPIView):
    authentication_classes = [JWTCookieUserAuthentication, ]
    serializer_class = TableSerializer
    queryset = Table.objects.filter(completed=True, timestamp__gte=time.mktime(datetime.utcnow().date().timetuple()))

    def list(self, request, *args, **kwargs):
        # print(time.mktime(datetime.utcnow().date().timetuple()))
        tables = self.get_queryset()
        return Response({
            "total_tables": tables.count(),
            "total_revenue": self.queryset.aggregate(Sum("price"))["price__sum"],
            "tip_amount": self.queryset.aggregate(Sum("tip_amount"))["tip_amount__sum"],
            "tables": TableSerializer(tables, many=True).data,
            })


class ProductView(viewsets.ModelViewSet, generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            name = self.request.query_params["name"]
            if name:
                return Product.objects.filter(name__icontains=name)
        except:
            pass
        return None

class OrderViewset(APIView):
    http_method_names = ['post', 'delete']
    

    def post(self, request, *args, **kwargs):
        data = request.data
        table_number = data["table_number"]
        product_id = data["product_id"]
        try:
            table = Table.objects.get(table_number=table_number, completed=False)
        except Exception as e:
            print(e)
            return Response({"errors": "The chosen table does not exist", "e": str(e)})

        try:
            new_order = Order.objects.create(table=table, product_id=product_id)
        except Exception as e:
            print(e)
            return Response({"errors": "Bad product id (most likely)", "e": str(e)})
        
        
        return Response({"success": "Order has been added", "table": TableSerializer(Table.objects.get(id=table.id)).data})

    def delete(self, request, *args, **kwargs):
        data = request.data
        order_id = data["order_id"]

        try:
            order = Order.objects.get(id=order_id)
        except Exception as e:
            print(e)
            return Response({"error": "No order with the given ID"})

        table_number = order.table.table_number
        order.delete()
        
        table = Table.objects.get(table_number=table_number, completed=False)

        return Response({"success": "Order has been deleted", "table": TableSerializer(table).data})

class EndTable(APIView):
    http_method_names = ['post']

    def post(self, request):
        data = request.data
        try:
            table = Table.objects.get(table_number=int(data["table_number"]), completed=False)
        except Exception as e:
            print(e)
            return Response({"errors": "Not completed table with this ID doesn't exist", "e": str(e)})
        table.end_the_table(float(data["paid_with"]))
        return Response(model_to_dict(table))