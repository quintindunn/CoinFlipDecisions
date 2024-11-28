from . import views
from django.urls import path
urlpatterns = [
    path('new', views.new_flip, name="new-flip"),
    path("ratings/rate/", views.rate, name="rate"),
    path("updates/", views.update_visibility, name="update-visibility"),
    path('myflips', views.my_flips, name="my-flips"),
    path('<str:pk>', views.execute_flip, name="execute-flip"),
]

