from sys import exception
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from apify_client import ApifyClient
from os import environ
from .helpers import construct_run_input, generate_sentiment_analysis, dump_into_json, generate_product_analysis
from rest_framework.response import Response
from rest_framework import status
from requests import get
from .serializers import ProductSerializer, ReviewSerializer, AnalysisSerializer
from .models import Review, Product, Analysis
import json
#

@api_view(['GET'])
def dump_into_json_route(request):
    all_reviews = Review.objects.all()
    all_reviews_serialized = ReviewSerializer(all_reviews, many=True)

    all_products = Product.objects.all()
    all_products_serialized = ProductSerializer(all_products, many=True)

    all_analysis = Analysis.objects.all()
    all_analysis_serialized = AnalysisSerializer(all_analysis, many=True)

    payload = {"reviews": all_reviews_serialized.data,
               "products": all_products_serialized.data,
               "analysis": all_analysis_serialized.data}

    with open("db.json", "w") as db:
        db.write(json.dumps(payload))

    with open("reviews.json", "w") as review_file:
        review_file.write(json.dumps({"reviews": all_reviews_serialized.data}))

    with open("product.json", "w") as product_file:
        product_file.write(json.dumps({"products": all_products_serialized.data}))

    with open("analysis.json", "w") as analysis_file:
        analysis_file.write(json.dumps({"analysis": all_analysis_serialized.data}))

    return Response({}, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_product_analysis(request):
    try:
        product_url = request.GET.get('product_url')
        all_reviews_for_product = Review.objects.filter(associated_product_url=product_url)

        star_reviews_1 = 0
        star_reviews_2 = 0
        star_reviews_3 = 0
        star_reviews_4 = 0
        star_reviews_5 = 0
        review_country = all_reviews_for_product[0].country


        # loop through all reviews and get the number of 1, 2, 3, 4 and 5 start ratings
        total_rating = 0
        for review in all_reviews_for_product:
            total_rating += review.score
            if review.score == 1:
                star_reviews_1 += 1
            elif review.score == 2:
                star_reviews_2 += 1
            elif review.score == 3:
                star_reviews_3 += 1
            elif review.score == 4:
                star_reviews_4 += 1
            elif review.score == 5:
                star_reviews_5 += 1


        average_rating = 0
        if len(all_reviews_for_product) > 0:
            average_rating = total_rating / len(all_reviews_for_product)
        sentiment_analysis = generate_sentiment_analysis([x.content for x in all_reviews_for_product])
        # review_keywords = extract_key_words([x.content for x in all_reviews_for_product])
        payload = {
            "review_country": review_country,
            "star_reviews_1": star_reviews_1,
            "star_reviews_2": star_reviews_2,
            "star_reviews_3": star_reviews_3,
            "star_reviews_4": star_reviews_4,
            "star_reviews_5": star_reviews_5,
            "average_rating": average_rating,
            "sentiment_analysis": sentiment_analysis,
        }



        return Response({"analysis": payload}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_reviews_for_product(request):
    product_url = request.GET.get('product_url')
    all_reviews = Review.objects.filter(associated_product_url=product_url)
    return Response({"reviews": ReviewSerializer(all_reviews, many=True).data},
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def get_products_that_have_reviews(request):
    all_products = Product.objects.all()
    return Response({"products": ProductSerializer(all_products, many=True).data},
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def scrape_new_reviews_for_product(request):
    # get relative information from the url
    product_url = request.GET.get('product_url')
    product_name = request.GET.get('product_name')
    review_count = request.GET.get('review_count')

    # initialize the apify client
    api_key = environ.get('APIFY_API_KEY')
    apify_client = ApifyClient(api_key)

    # The apify client takes a payload of a very specific format
    # The logic to create this payload has been abstracted into another function
    run_input = construct_run_input([product_url], int(review_count))


    # This runs the specific scrapper that we need to use
    # this should be uncommented later. Right now, I want to test it on the data that I already have
    run = apify_client.actor("R8WeJwLuzLZ6g4Bkk").call(run_input=run_input)
    resp = apify_client.dataset(run["defaultDatasetId"]).iterate_items()


    # Portion of code to be deleted
    # resp = get("https://api.apify.com/v2/datasets/tbWfTQXAiNzhtUweB/items?token=apify_api_cH1VXiOzACW1yTd6oHRcD8FxPzgbim2iaRwu")
    # resp = resp.json()

    # Create the product and save it in the products database
    try:
        associated_product = Product.objects.get(product_url=product_url)
    except Exception as e:
        associated_product = Product(
            product_name=product_name,
            product_url=product_url,
        )
        associated_product.save()




    # load the response into a list of dictionaries
    all_reviews_data_parsed = resp
    # For each response, make a database entry and save it
    for review_data in all_reviews_data_parsed:
        new_review = Review(
            review_url = review_data.get("reviewUrl", "n/a"),
            score = review_data.get("ratingScore", 0),
            country = review_data.get("country", "n/a"),
            content = (review_data.get("reviewTitle", "n/a") + ":" + review_data.get("reviewDescription", "n/a")),
            date_posted = review_data.get("date", "n/a"),
            associated_product_url = product_url,
            product_name = product_name,
            product_id = associated_product.pk,
        )
        new_review.save()
    generate_product_analysis(product_url, product_name)
    dump_into_json()




    return Response(resp, status=status.HTTP_200_OK)

@api_view(['GET'])
def changes(request):
    # # get all products and add a brand name to them
    # for product in Product.objects.all():
    #     if "Iphone" in product.product_name:
    #         product.product_name = product.product_name.replace("Iphone", "iPhone")
    #     product.save()
    #
    # for review in Review.objects.all():
    #     if "Iphone" in review.product_name:
    #         review.product_name = review.product_name.replace("Iphone", "iPhone")
    #     review.save()
    #
    #
    # for analysis in Analysis.objects.all():
    #     if "Iphone" in analysis.product_name:
    #         analysis.product_name = analysis.product_name.replace("Iphone", "iPhone")
    #     analysis.save()

    #


    for product in Product.objects.all():
        if "Apple" in product.product_name:
            product.brand_name = "Apple"
        elif "Samsung" in product.product_name:
            product.brand_name = "Samsung"
        product.save()
    # # get all reviews and add a brand name to them
    for review in Review.objects.all():
        if "Apple" in review.product_name:
            review.brand_name = "Apple"
        elif "Samsung" in review.product_name:
            review.brand_name = "Samsung"
        review.save()

    # # get all analysis and add a brand name to them
    for analysis in Analysis.objects.all():
        if "Apple" in analysis.product_name:
            analysis.brand_name = "Apple"
        elif "Samsung" in analysis.product_name:
            analysis.brand_name = "Samsung"

        analysis.save()


    return Response({}, status=status.HTTP_200_OK)