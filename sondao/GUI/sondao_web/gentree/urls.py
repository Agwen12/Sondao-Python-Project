from django.urls import path
from .views import home, PersonAddView, Index

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path('add_person/', PersonAddView.as_view(), name='add_person'),
]