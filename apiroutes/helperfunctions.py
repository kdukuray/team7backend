from typing import Dict, List
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