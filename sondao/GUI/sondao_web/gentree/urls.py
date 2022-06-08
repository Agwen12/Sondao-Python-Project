from django.urls import path
from .views import Index, PersonDeleteView, RelationDeleteView, DocumentDeleteView, GraphView, DocumentUpdateView, \
    PersonUpdateView, RelationUpdateView

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path('<pk>/delete_person/', PersonDeleteView.as_view(), name='person-delete'),
    path('<pk>/delete_relation/', RelationDeleteView.as_view(), name='relation-delete'),
    path('<pk>/delete_document/', DocumentDeleteView.as_view(), name='document-delete'),
    path('<pk>/update_person/', PersonUpdateView.as_view(), name='person-update'),
    path('<pk>/update_relation/', RelationUpdateView.as_view(), name='relation-update'),
    path('<pk>/update_document/', DocumentUpdateView.as_view(), name='document-update'),
    path('graph', GraphView.as_view(), name='graph'),
]
