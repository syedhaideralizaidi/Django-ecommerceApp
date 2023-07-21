from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(digital = True)


class OrderManager(models.Manager):
    def get_timerange_orders(self, r1, r2):
        return super().get_queryset().filter(date_ordered__range=(r1, r2))

    def get_complete_orders(self):
        return super().get_queryset().filter(complete=True)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gender="FEMALE")
