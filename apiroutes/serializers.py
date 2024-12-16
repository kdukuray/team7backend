from rest_framework.serializers import ModelSerializer
from .models import Product, Review

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'