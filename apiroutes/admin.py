from django.contrib import admin
from .models import Review, Product, Analysis
from .helpers import generate_product_analysis


class ProductAdmin(admin.ModelAdmin):
    actions = ["generate_product_analysis_"]

    def generate_product_analysis_(self, request, queryset):
        for product in queryset:
            generate_product_analysis(product.product_url)


    short_description = "Generate product analysis"



admin.site.register(Review)
admin.site.register(Product, ProductAdmin)
admin.site.register(Analysis)