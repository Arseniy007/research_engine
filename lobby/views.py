from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from quoting.data_cleaning import clean_author_data
from utils.messages import display_error_message


def lobby_view(request):




    return JsonResponse({"message": "ok"})



