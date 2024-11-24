from . import views
from django.urls import path

urlpatterns = [
    path('/new', views.new_flip),
]
