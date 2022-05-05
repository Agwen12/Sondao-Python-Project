from django.urls import path
from .views import home, get_name

urlpatterns = [
    path("", home, name="home"),
    path("form", get_name, name="get_name"),
]