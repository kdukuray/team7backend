from django.db import models

class Review(models.Model):
    product_name = models.CharField(max_length=255, default='Samsung Galaxy S24 Ultra')
    product_id = models.IntegerField(default=2)
    review_url = models.CharField(max_length=255)
    score = models.IntegerField()
    country = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.CharField(max_length=255)
    associated_product_url = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, default='')


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_url = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, default='')


class Analysis(models.Model):
    product_name = models.CharField(max_length=255, default='Samsung Galaxy S24 Ultra')
    product_id = models.IntegerField(default=2)
    associated_product_url = models.CharField(max_length=255)
    review_country = models.TextField()
    one_star_rating = models.IntegerField()
    two_star_rating = models.IntegerField()
    three_star_rating = models.IntegerField()
    four_star_rating = models.IntegerField()
    five_star_rating = models.IntegerField()
    sentiment_analysis = models.TextField()
    average_rating = models.FloatField()
    brand_name = models.CharField(max_length=255, default='')





    # self.review_url: str = review_url
    # self.score: int = score
    # self.country: str = country
    # self.content: str = content
    # # This should be changed
    # self.date_posted: str = date_posted
