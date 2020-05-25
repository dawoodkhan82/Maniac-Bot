from django.contrib import admin

from .models import Docstring
from .models import Setup

admin.site.register(Docstring)
admin.site.register(Setup)