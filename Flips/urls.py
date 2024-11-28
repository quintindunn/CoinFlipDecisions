from . import views
from django.urls import path
urlpatterns = [
    path('new', views.new_flip, name="new-flip"),
    path('myflips', views.my_flips, name="my-flips"),
    path('<str:pk>', views.execute_flip, name="execute-flip"),
]

