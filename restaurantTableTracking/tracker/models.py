from distutils.command.upload import upload
from hashlib import blake2b
from msilib.schema import tables
from pyexpat import model
from secrets import choice
from traceback import print_exc
from unittest import defaultTestLoader
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete
import time


class TableOptions(models.IntegerChoices):
    CORNER_TV = 0, "Corner tv"
    IN_1 = 1, "Inside 1"
    IN_2 = 2, "Inside 2"
    IN_3 = 3, "Inside 3"
    IN_4 = 4, "Inside 4"
    IN_5 = 5, "Inside 5"
    BAR_1 = 6, "Bar 1"
    BAR_2 = 7, "Bar 2"
    BAR_3 = 8, "Bar 3"
    FRONT_DOOR = 9, "Front door table"
    OUT_1 = 10, "Out 1 (first one on the left)"
    OUT_2 = 11, "Out 2"
    OUT_3 = 12, "Out 3"
    OUT_4 = 13, "Out 4"
    OUT_5 = 14, "Out 5 (first one on the right)"
    NO_TABLE = 15, "Without a table"

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=120, blank=False)
    price = models.FloatField(null=False)
    image = models.ImageField(upload_to="menu_thumbnails", null=False, default="menu_thumbnails/no_thumbnail.png")

    def __str__(self):
        return self.name

class Table(models.Model):
    table_number = models.IntegerField(null=False, default=TableOptions.NO_TABLE, choices=TableOptions.choices)
    completed = models.BooleanField(default=False)
    price = models.FloatField(null=False, default=0)
    timestamp = models.FloatField(null=True, blank=True)
    tip_amount = models.FloatField(default=0)

    def end_the_table(self, payed_amount):
        self.completed = True
        self.tip_amount = payed_amount - self.price
        self.timestamp = time.time()
        self.save()
        Table.objects.create(table_number=self.table_number)

    

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.FloatField(null=True, blank=True)


def timestamp_order_update_price(sender, instance, created, *args, **kwargs):
    if created:
        the_table = Table.objects.get(id=instance.table.id, completed=False)
        the_table.price += instance.product.price
        the_table.save()
        instance.timestamp = time.time()
        instance.save()

def remove_order_from_the_table(sender, instance, *args, **kwargs):
    the_table = Table.objects.get(id=instance.table.id)
    if not the_table.completed:
        the_table.price -= instance.product.price
    the_table.save()

def timestamp_table(sender, instance, created, *args, **kwargs):
    if created:
        instance.timestamp = time.time()
        instance.save()

post_save.connect(timestamp_order_update_price, sender=Order)
post_save.connect(timestamp_table, sender=Table)
pre_delete.connect(remove_order_from_the_table, sender=Order)
