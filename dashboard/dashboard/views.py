from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
import os
import uuid

HASH_TO_REPO_JSON = 'dashboard/HASH_TO_REPO.json'

@csrf_exempt
def setup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        repo_name = data["repo_name"]
        uid = uuid.uuid4()
        random_hash = uid.hex

        with open(HASH_TO_REPO_JSON, 'r+') as f:
            dictionary = json.load(f)
            dictionary[random_hash] = repo_name
            f.seek(0)
            json.dump(dictionary, f, indent=4)
            f.truncate()
    return HttpResponse(f'{repo_name}/{random_hash}')