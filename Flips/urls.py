from . import views
from django.urls import path

urlpatterns = [
    path('/new', views.new_flip, name="new-flip"),
    path('/<str:pk>', views.execute_flip, name="execute-flip")
]
