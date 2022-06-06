from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Person, Relation
from pyvis.network import Network
from django.views.generic.base import TemplateView

from .forms import PersonForm
from .models import Person

import networkx as nx
import pyvis.network
import datetime


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PersonForm()
        return context


def person_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PersonForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.surname = form.cleaned_data['surname']
            post.save()
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PersonForm()

    return render(request, '/', {'form': form})


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
        # print(relation)
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
