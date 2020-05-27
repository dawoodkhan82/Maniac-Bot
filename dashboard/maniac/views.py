from django.shortcuts import render
from django.http import HttpResponse
from .models import Docstring, Setup
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

import os
import uuid
HASH_TO_REPO_JSON = 'dashboard/dashboard/HASH_TO_REPO.json'


@csrf_exempt
def setup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        repo_name = data["repo_name"]
        uid = uuid.uuid4()
        random_hash = uid.hex

        obj, created = Setup.objects.update_or_create(
            repo_name=repo_name,
            defaults={'random_hash': random_hash},
        )
    return HttpResponse(f'{repo_name}/{random_hash}')


def about(request):
    return render(request, 'maniac/about.html')


def handler404(request, exception, *args, **argv):
    # return HttpResponse("Uh-oh")
    return render(request, 'maniac/404.html', status=404)


def index(request, repo_name, random_hash):
    try:
        setup_obj = Setup.objects.filter(repo_name=repo_name)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if random_hash != getattr(setup_obj[0], "random_hash"):
        return HttpResponse(status=404)

    try:
        stale = Docstring.objects.filter(repo_name=repo_name,
                                         is_stale=True,
                                         is_missing=False)
    except ObjectDoesNotExist:
        stale = False
    try:
        missing = Docstring.objects.filter(repo_name=repo_name,
                                           is_missing=True)
    except ObjectDoesNotExist:
        missing = False
    try:
        passed = Docstring.objects.filter(repo_name=repo_name,
                                          is_stale=False,
                                          is_missing=False)
    except ObjectDoesNotExist:
        passed = False

    num_fns = 0
    num_stale = 0
    stale_fns = []
    if stale:
        for obj in stale:
            stale_fns.append([[getattr(obj, "file_path"),
                              getattr(obj, "blob_url")],
                              getattr(obj, "function_name"),
                              str(getattr(obj, "time_behind")),
                              getattr(obj, "last_doc_commit"),
                              getattr(obj, "code_author")])
            num_stale += 1
            num_fns += 1

    num_missing = 0
    missing_fns = []
    if missing:
        for obj in missing:
            missing_fns.append([[getattr(obj, "file_path"),
                                getattr(obj, "blob_url")],
                                getattr(obj, "function_name"),
                                " ",
                                " ",
                                getattr(obj, "code_author")])
            num_missing += 1
            num_fns += 1

    num_passed = 0
    passed_fns = []
    if passed:
        for obj in passed:
            passed_fns.append([[getattr(obj, "file_path"),
                               getattr(obj, "blob_url")],
                               getattr(obj, "function_name"),
                               " ",
                               " ",
                              getattr(obj, "code_author")])
            num_passed += 1
            num_fns += 1

    doc_coverage = 100 * (num_passed + num_stale) / (num_passed +
                                                     num_stale +
                                                     num_missing)
    doc_fresh = 100 * num_passed / (num_passed + num_stale +
                                    num_missing)

    context = {'stale_fns': stale_fns, "missing_fns": missing_fns,
               "passed_fns": passed_fns, "repo_name": repo_name,
               "doc_coverage": str(round(doc_coverage)) + '%',
               "doc_fresh": str(round(doc_fresh)) + '%',
               "num_fns": str(num_fns)}

    return render(request, 'maniac/index.html', context)


@csrf_exempt
def commit(request, repo_name, random_hash):
    try:
        setup_obj = Setup.objects.filter(repo_name=repo_name)
    except ObjectDoesNotExist:
        return HttpResponse("Sorry! This link is invalid!", status=404)
    if random_hash != getattr(setup_obj[0], "random_hash"):
        return HttpResponse("Sorry! This link is invalid!", status=404)

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
            blob_url = data[key]["blob_url"]
            if is_stale and not is_missing:
                # TODO(aliabd): fix this
                try:
                    t = datetime.strptime(time_behind, "%d day, %H:%M:%S")
                except ValueError:
                    t = datetime.strptime(time_behind, "%d days, %H:%M:%S")
                time_behind = timedelta(days=t.day, hours=t.hour, minutes=t.minute,
                                  seconds=t.second)

                last_doc_commit = "https://github.com/dawoodkhan82/" \
                                  "Maniac-Bot-Test/commit/" + \
                                  data[key]["last_doc_commit"]
            else:
                time_behind = None
                last_doc_commit = None
            code_author = data[key]["code_author"]

            obj, created = Docstring.objects.update_or_create(
                function_name=function_name,
                defaults={"repo_name": repo_name,
                          "file_path": file_path,
                          "blob_url": blob_url,
                          "function_name": function_name,
                          "time_behind": time_behind,
                          "last_doc_commit": last_doc_commit,
                          "code_author": code_author,
                          "is_stale": is_stale, "is_missing": is_missing},
            )

    return HttpResponse("Success!")

@csrf_exempt
def coverage(request, repo_name, random_hash):
    try:
        setup_obj = Setup.objects.filter(repo_name=repo_name)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    if random_hash != getattr(setup_obj[0], "random_hash"):
        return HttpResponse(status=404)

    try:
        stale = Docstring.objects.filter(repo_name=repo_name,
                                         is_stale=True,
                                         is_missing=False)
    except ObjectDoesNotExist:
        stale = False
    try:
        missing = Docstring.objects.filter(repo_name=repo_name,
                                           is_missing=True)
    except ObjectDoesNotExist:
        missing = False
    try:
        passed = Docstring.objects.filter(repo_name=repo_name,
                                          is_stale=False,
                                          is_missing=False)
    except ObjectDoesNotExist:
        passed = False

    print("STALE: ", stale)
    print("MISSING: ", missing)
    print("PASSED: ", passed)

    num_stale = 0
    if stale:
        for obj in stale:
            num_stale += 1
    num_missing = 0
    if missing:
        for obj in missing:
            num_missing += 1
    num_passed = 0
    if passed:
        for obj in passed:
            num_passed += 1

    print(num_stale)
    print(num_missing)
    print(num_passed)
    doc_coverage = 100 * (num_passed + num_stale) / (num_passed +
                                                    num_stale +
                                               num_missing)
    doc_fresh = 100 * num_passed / (num_passed + num_stale +
                                       num_missing)

    context = {'documentation_coverage': str(round(doc_coverage)) + '%',
               'documentation_freshness': str(round(doc_fresh)) + '%'}
    return HttpResponse(json.dumps(context))

