from django.urls import path

from . import views

urlpatterns = [
    path('<str:repo_name>/', views.index, name='index'),
    path('<str:repo_name>/commit/', views.commit, name='commit')
]