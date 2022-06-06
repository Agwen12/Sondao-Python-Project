from django.urls import path
from .views import home, person_form, Index

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("form", person_form, name="person_form"),
]