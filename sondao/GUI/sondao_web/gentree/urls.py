from django.urls import path
from .views import home, person_form, Index, PersonDeleteView

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path('<pk>/delete/', PersonDeleteView.as_view(), name='person_delete'),
    path('graph', home),
]