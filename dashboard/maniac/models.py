from django.db import models


class Docstring(models.Model):
    file_path = models.CharField(max_length=3000)
    function_name = models.CharField(max_length=200)
    time_behind = models.DurationField(blank=True)
    last_doc_commit = models.URLField(max_length=1000, blank=True)
    code_author = models.CharField(max_length=50)
    is_stale = models.BooleanField(default=False)
    is_missing = models.BooleanField(default=False)
