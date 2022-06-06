from django.urls import path
from .views import home, person_form

urlpatterns = [
    path("", home, name="home"),
    path("form", person_form, name="person_form"),
]