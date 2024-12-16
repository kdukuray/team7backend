from django.db import models

class Review(models.Model):
    review_url = models.CharField(max_length=255)
    score = models.IntegerField()
    country = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.CharField(max_length=255)
    associated_product_url = models.CharField(max_length=255)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_url = models.CharField(max_length=255)





    # self.review_url: str = review_url
    # self.score: int = score
    # self.country: str = country
    # self.content: str = content
    # # This should be changed
    # self.date_posted: str = date_posted
