
from django.contrib import admin

from .models import Person, Document, Relation

admin.site.register(Person)
admin.site.register(Document)
admin.site.register(Relation)