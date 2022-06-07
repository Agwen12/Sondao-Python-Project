from django.http import HttpResponse, HttpResponseRedirect
from pyvis.network import Network
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from .forms import PersonForm, RelationFrom, DocumentForm
from .models import Person, Relation, Document
import networkx as nx


class GeneralDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    success_url = "/"


class PersonDeleteView(GeneralDeleteView):
    model = Person


class RelationDeleteView(GeneralDeleteView):
    model = Relation


class DocumentDeleteView(GeneralDeleteView):
    model = Document


class Index(TemplateView):
    template_name = "index.html"

    def post(self, request):
        forms = (form(request.POST) for form in [PersonForm, RelationFrom, DocumentForm])

        for form in forms:
            if form.is_valid():
                form.save()
                break

        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_form'] = PersonForm()
        context['person_objects'] = Person.objects.all()
        context['relation_form'] = RelationFrom()
        context['relation_objects'] = Relation.objects.all()
        context['document_form'] = DocumentForm()
        context['document_objects'] = Document.objects.all()
        return context


def home(request):
    menager = Person.objects
    items = menager.all()
    graph = nx.Graph()
    for item in items.values():
        graph.add_node(item['id'],
                       label=(item['name'] + " " + item['surname']),
                       physics=False,
                       shape="box")

    # p = Relation(first_relative_id=1, second_relative_id=2, relation=RelationTypes.CHILD)
    # p.save()
    relations = Relation.objects.order_by('first_relative').all()
    for relation in relations.values():
        graph.add_edge(relation['first_relative_id'],
                       relation['second_relative_id'],
                       label=str(relation['relation']))

    nt = Network(600, 1700)
    nt.set_template("gentree\\templates\\template.html")
    nt.from_nx(graph)
    nt.set_options("""var options = {
      "edges": {
        "to": {
            "enabled": true,
            "type": "arrow"
          },
        "color": {
          "inherit": true
        },
        "smooth": false
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "levelSeparation": 200,
          "nodeSpacing": 100,
          "direction": "UD",
          "sortMethod": "directed"
        }
      },
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0
        },
        "minVelocity": 0.75,
        "solver": "hierarchicalRepulsion"
      }
    }""")
    out = nt.generate_html()
    return HttpResponse(out)
