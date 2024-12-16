from rest_framework.serializers import ModelSerializer
from .models import Product, Review, Analysis

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class AnalysisSerializer(ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'