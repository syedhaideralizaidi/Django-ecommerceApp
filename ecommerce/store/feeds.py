import os

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy , reverse
from .models import Product

class LatestProduct(Feed):
    title = 'Helloo, Welcome to Products of Haider!! Happy Surfing :)'
    link = reverse_lazy('product_list')
    description = 'New Product'
    description_template = os.path.join(settings.BASE_DIR, "templates/store/rss_feed.html")
    #description_template = reverse('product_list')


    def items(self):
        return Product.products.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.price

    def item_link(self, item):
        return item.get_absolute_url()
