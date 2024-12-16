from typing import Dict, List
from openai import OpenAI
from os import environ
import json

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

def extract_key_words(all_reviews: List [str]):
    all_reviews_concatenated = "-".join(all_reviews)
    system_prompt = ("You are a keyword extractor. Given a list of hyphen seperated reviews for a product"
                     "Extract the keywords that people are using to describe the product. The response should"
                     "be a list of comma separated key words. Example: "
                     "'great, perfect condition', bad quality, ...")

    open_ai_api_client = OpenAI(api_key=environ.get("OPENAI_API_KEY"))
    api_response = open_ai_api_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": all_reviews_concatenated}
        ]
    )

    return api_response.choices[0].message.content


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