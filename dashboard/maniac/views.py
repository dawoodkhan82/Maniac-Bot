from django.shortcuts import render
from django.http import HttpResponse


def index(request, repo_name):
    return HttpResponse("Hello, world. You're at the maniac dashboard "
                        f"for {repo_name}.")

# Create your views here.
