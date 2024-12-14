from django.shortcuts import render
from rest_framework.decorators import api_view
from apify_client import ApifyClient
from os import environ
from .helperfunctions import construct_run_input
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def get_reviews_for_product(request):
    # first we initialize the apify client with the apify api key
    # I stored the api key in an environment variable
    # Will share it with you separately over discord
    # make sure to put the api_key in an environment variable with the same name
    api_key = environ.get('APIFY_API_KEY')
    client = ApifyClient(api_key)

    if request.method == 'POST':
        product_url = request.data['product_url']
        reviews_count = int(request.data['reviews_count'])


        # This is the payload that the client needs to run
        # I abstracted its logic into another module called helper functons
        run_input = construct_run_input([product_url], reviews_count)

        # do not change this actor id
        # It is needed to run the specific amazon review scrapper that we need
        run = client.actor("R8WeJwLuzLZ6g4Bkk").call(run_input=run_input)


        # these were for testing purposes
        # Fetch and print Actor results from the run's dataset (if there are any)
        # for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        #     print(item)
        #
        #     # client.dataset(run["defaultDatasetId"])

        return Response({"product_reviews": client.dataset(run["defaultDatasetId"]).iterate_items()},
                        status=status.HTTP_200_OK)


