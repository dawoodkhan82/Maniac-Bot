from django.shortcuts import render
from django.http import HttpResponse
from .models import Docstring
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


def index(request, repo_name):
    try:
        stale = Docstring.objects.filter(is_stale=True)
    except ObjectDoesNotExist:
        stale = False
    try:
        missing = Docstring.objects.filter(is_missing=True)
    except ObjectDoesNotExist:
        missing = False
    try:
        passed = Docstring.objects.filter(is_stale=False, is_missing=False)
    except ObjectDoesNotExist:
        passed = False

    stale_fns = []
    if stale:
        for obj in stale:
            stale_fns.append([getattr(obj, "file_path"),
                              getattr(obj, "function_name"),
                              str(getattr(obj, "time_behind")),
                              getattr(obj, "last_doc_commit"),
                              getattr(obj, "code_author")])

    missing_fns = []
    if missing:
        for obj in missing:
            missing_fns.append([getattr(obj, "file_path"),
                                getattr(obj, "function_name"),
                                " ",
                                " ",
                                getattr(obj, "code_author")])
    passed_fns = []
    if passed:
        for obj in passed:
            passed_fns.append([getattr(obj, "file_path"),
                              getattr(obj, "function_name"),
                               " ",
                               " ",
                              getattr(obj, "code_author")])

    context = {'stale_fns': stale_fns, "missing_fns": missing_fns,
               "passed_fns": passed_fns, "repo_name": repo_name}

    return render(request, 'maniac/index.html', context)


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
            is_stale = data[key]["is_stale"]
            is_missing = data[key]["is_missing"]
            if is_stale and not is_missing:
                # TODO(aliabd): fix this
                t = datetime.strptime(time_behind, "%d day, %H:%M:%S")
                time_behind = timedelta(days=t.day, hours=t.hour, minutes=t.minute,
                                  seconds=t.second)

                last_doc_commit = data[key]["last_doc_commit"]
            else:
                time_behind = None
                last_doc_commit = None
            code_author = data[key]["code_author"]


            d = Docstring(file_path=file_path, function_name=function_name,
                          time_behind=time_behind,
                          last_doc_commit=last_doc_commit,
                          code_author=code_author,
                          is_stale=is_stale, is_missing=is_missing)
            d.save()
    return HttpResponse("Success!")
