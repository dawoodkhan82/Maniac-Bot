from django.db import models


class Docstring(models.Model):
    repo_name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=3000)
    blob_url = models.URLField(max_length=1000)
    function_name = models.CharField(max_length=200)
    time_behind = models.DurationField(blank=True, null=True)
    last_doc_commit = models.URLField(max_length=1000, blank=True, null=True)
    code_author = models.CharField(max_length=50, null=True)
    is_stale = models.BooleanField(default=False)
    is_missing = models.BooleanField(default=False)


class Setup(models.Model):
    repo_name = models.CharField(max_length=50)
    random_hash = models.CharField(max_length=200)
