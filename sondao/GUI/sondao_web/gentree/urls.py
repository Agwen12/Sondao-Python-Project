from django.urls import path
from .views import Index, PersonDeleteView, RelationDeleteView, DocumentDeleteView

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path('<pk>/delete_person/', PersonDeleteView.as_view(), name='person-delete'),
    path('<pk>/delete_relation/', RelationDeleteView.as_view(), name='relation-delete'),
    path('<pk>/delete_document/', DocumentDeleteView.as_view(), name='document-delete'),

]