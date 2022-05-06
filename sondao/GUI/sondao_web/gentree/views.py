import networkx as nx
import pyvis.network
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from .models import Person, Relation
from pyvis.network import Network
from sondao.logic.RelationTypes import RelationTypes




def home(request):
    menager = Person.objects
    items = menager.all()
    graph = nx.Graph()
    for item in items.values():
        graph.add_node(item['id'],
                       label=(item['name']+ " "+ item['surname']),
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



    nt = Network()
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
