from . import views
from django.urls import path

urlpatterns = [
    path('/new', views.new_flip),
    path('/<str:pk>', views.execute_flip)
]
