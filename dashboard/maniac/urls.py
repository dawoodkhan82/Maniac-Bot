from django.urls import path

from . import views

urlpatterns = [
    path('<str:repo_name>/<str:random_hash>/', views.index, name='index'),
    path('<str:repo_name>/<str:random_hash>/commit/', views.commit,
         name='commit'),
    path('<str:repo_name>/<str:random_hash>/coverage/', views.coverage,
         name='coverage'),
    path('setup/', views.setup)

]