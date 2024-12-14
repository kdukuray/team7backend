from django.urls import path
from .views import get_reviews_for_product

urlpatterns = [
    path("get-reviews-for-product/", get_reviews_for_product, name="get_reviews_for_product"),
]