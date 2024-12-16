from django.urls import path
from .views import (get_reviews_for_product, scrape_new_reviews_for_product,
                    get_products_that_have_reviews, get_product_analysis, dump_into_json, dump_into_json_route)

urlpatterns = [
    path("scrape-new-reviews-for-product/", scrape_new_reviews_for_product, name="scrape_reviews_for_product"),
    path("get-reviews-for-product/", get_reviews_for_product, name="get_reviews_for_product"),
    path("get-products-that-have-reviews/", get_products_that_have_reviews, name="get_reviews_for_product"),
    path("get-product-analysis/", get_product_analysis, name="get_product_analysis"),
    path("dump-into-json/", dump_into_json_route, name="dump_into_json"),
]