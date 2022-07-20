from django.urls import path
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"table", TableViewsetNotCompleted, basename="tableView")
router.register(r"today_info", TodayTableInfo, basename="todayInfo")
router.register(r"product", ProductView, basename="productView")

urlpatterns = [
    path("order/", OrderViewset.as_view(), name="orderView"),
    path("end/", EndTable.as_view(), name="end"),
] + router.urls
