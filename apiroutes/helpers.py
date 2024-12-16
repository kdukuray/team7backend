from typing import Dict, List
from openai import OpenAI
from os import environ
import json
from .models import Review, Product, Analysis
from .serializers import ReviewSerializer, ProductSerializer, AnalysisSerializer

def generate_sentiment_analysis(all_reviews: List [str]):
    all_reviews_concatenated = "-".join(all_reviews)
    system_prompt = ("You are a sentiment analyzer that receives a string of hyphen seperated reviews for a product."
                     " Analyze the reviews and respond with a short but detailed paragraph explaining the"
                     " overall sentiment of consumers towards the product ")

    open_ai_api_client = OpenAI(api_key=environ.get("OPENAI_API_KEY"))
    api_response = open_ai_api_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": all_reviews_concatenated}
        ]
    )

    return api_response.choices[0].message.content

# def extract_key_words(all_reviews: List [str]):
#     all_reviews_concatenated = "-".join(all_reviews)
#     system_prompt = ("You are a keyword extractor. Given a list of hyphen seperated reviews for a product"
#                      "Extract the keywords that people are using to describe the product. The response should"
#                      "be a list of comma separated key words. Example: "
#                      "'great, perfect condition', bad quality, ...")
#
#     open_ai_api_client = OpenAI(api_key=environ.get("OPENAI_API_KEY"))
#     api_response = open_ai_api_client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": all_reviews_concatenated}
#         ]
#     )
#
#     return api_response.choices[0].message.content


def construct_run_input(product_urls: List[str], reviews_count: int) -> Dict:

    run_input = {
    "productUrls": [{ "url": product_url } for product_url in product_urls],
    "maxReviews": reviews_count,
    "sort": "helpful",
    "includeGdprSensitive": False,
    "filterByRatings": ["allStars"],
    "reviewsUseProductVariantFilter": False,
    "reviewsEnqueueProductVariants": False,
    "proxyCountry": "AUTO_SELECT_PROXY_COUNTRY",
    "scrapeProductDetails": False,
    "reviewsAlwaysSaveCategoryData": False,
    "scrapeQuickProductReviews": True,
    }

    return run_input


def dump_into_json():
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



def generate_product_analysis(product_url, product_name):
    try:
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

        try:
            associated_product = Product.objects.get(product_url=product_url)
        except Exception as e:
            associated_product = Product(
                product_name=product_name,
                product_url=product_url,
            )
            associated_product.save()

        new_analysis = Analysis(
            associated_product_url=product_url,
            review_country=review_country,
            one_star_rating=star_reviews_1,
            two_star_rating=star_reviews_2,
            three_star_rating=star_reviews_3,
            four_star_rating=star_reviews_4,
            five_star_rating=star_reviews_5,
            sentiment_analysis=sentiment_analysis,
            average_rating=average_rating,
            product_name=product_name,
            product_id = associated_product.pk,
        )
        new_analysis.save()

    except Exception as e:
        pass