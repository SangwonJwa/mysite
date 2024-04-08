from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello world.")

def some_url(requst):
    return HttpResponse("Some url을 구현해 봤습니다.")

# Create your views here.
