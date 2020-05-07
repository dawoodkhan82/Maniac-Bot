from django.shortcuts import render
from django.http import HttpResponse
from .models import Docstring
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta


def index(request, repo_name):
    return HttpResponse("Hello, world. You're at the maniac dashboard "
                        f"for {repo_name}.")

@csrf_exempt
def commit(request, repo_name):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        print("data: ", data)
        for key in data.keys():
            print("key", key)
            file_path = data[key]["file_path"]
            function_name = key
            time_behind = data[key]["time_behind"]

            #TODO(aliabd): fix this
            t = datetime.strptime(time_behind, "%d day, %H:%M:%S")
            time_behind = timedelta(days=t.day, hours=t.hour, minutes=t.minute,
                              seconds=t.second)

            last_doc_commit = data[key]["last_doc_commit"]
            code_author = data[key]["code_author"]
            is_stale = data[key]["is_stale"]
            is_missing = data[key]["is_missing"]

            d = Docstring(file_path=file_path, function_name=function_name,
                          time_behind=time_behind,
                          last_doc_commit=last_doc_commit,
                          code_author=code_author,
                          is_stale=is_stale, is_missing=is_missing)
            d.save()
    return HttpResponse("Success!")
