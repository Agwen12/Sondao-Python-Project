from django.http import HttpResponse, HttpResponseRedirect
from pyvis.network import Network
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import DeleteView
from sondao.logic.Person import Person as LPerson, Testator
from sondao.logic.PersonalInfo import PersonalInfo, RelativesInfo
from sondao.logic.RelationTypes import RelationTypes
from django.views.decorators.clickjacking import xframe_options_sameorigin
from sondao.logic.Algorithm import Algorithm
from .forms import PersonForm, RelationFrom, DocumentForm
from .models import Person, Relation, Document
import networkx as nx
import os


class GeneralDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    success_url = "/"

    class Meta:
        abstract = True


class PersonDeleteView(GeneralDeleteView):
    model = Person


class RelationDeleteView(GeneralDeleteView):
    model = Relation


class DocumentDeleteView(GeneralDeleteView):
    model = Document


class Index(TemplateView):
    template_name = "index.html"

    @staticmethod
    def post(request):
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

class GraphView(View):
    @xframe_options_sameorigin
    def get(self, request):
        persons_from_database = Person.objects.all()
        graph = nx.Graph()
        graph_data = dict(graph.nodes.data())
        persons, relation_dict, testator_id = list(), dict(), None
        for person_object in persons_from_database.values():
            if person_object['is_testator']:
                personal_info = PersonalInfo(
                    name=person_object['name'], surname=person_object['surname'], PESEL=person_object['pesel'],
                    phone_number=person_object['phone_number'], home_address=person_object['home_address'],
                    birthday=person_object['birthday'], proxy=person_object['proxy'],
                    receive_confirmation_place=person_object['receive_confirmation_place']
                )
                testator_id = person_object['id']
                person = Testator(personal_info=personal_info, internal_id=person_object['id'])
            else:
                personal_info = RelativesInfo(
                    name=person_object['name'], surname=person_object['surname'], PESEL=person_object['pesel'],
                    phone_number=person_object['phone_number'], home_address=person_object['home_address'],
                    birthday=person_object['birthday'], proxy=person_object['proxy'],
                    receive_confirmation_place=person_object['receive_confirmation_place'],
                    want_inherit=person_object['want_inherit'],
                    supposed_death_notification=person_object['supposed_death_notification']
                )
                person = LPerson(personal_info=personal_info, internal_id=person_object['id'])

            graph.add_node(person_object['id'],
                           label=f"{person_object['name']} {person_object['surname']}",
                           physics=False,
                           shape="box",
                           person=len(persons),
                           level=2 if person_object['is_testator'] else None,
                           color='yellow' if person_object['is_testator'] else None,
                           )
            persons.append(person)
        relations = Relation.objects.order_by('first_relative').all()
        for relation in relations.values():
            print(relation)
            relation = RelationTypes.from_string(relation['relation'])
            person_id = graph_data[relation['first_relative_id']]['person']
            sc_person_id = graph_data[relation['second_relative_id']]['person']
            if relation == RelationTypes.SPOUSE:
                persons[person_id].add_relative(persons[sc_person_id], relation)
            else:
                persons[sc_person_id].add_relative(persons[person_id], relation)
            relation_dict[(relation['first_relative_id'], relation['second_relative_id'])] = relation
            relation_dict[(relation['second_relative_id']), relation['first_relative_id']] = relation.opposite()
            graph.add_edge(relation['first_relative_id'],
                           relation['second_relative_id'],
                           label=str(relation))

        bfs_edges_result = list(nx.bfs_edges(graph, testator_id))
        for edge_info in bfs_edges_result:
            level = graph_data[edge_info[0]]['level']
            match relation_dict[edge_info]:
                case RelationTypes.CHILD | RelationTypes.FULL_ADOPTED_CHILD | RelationTypes.PARTIAL_ADOPTED_CHILD:
                    level -= 1
                case RelationTypes.EX_SPOUSE | RelationTypes.SIBLING | RelationTypes.SPOUSE:
                    level = level
                case RelationTypes.PARENT:
                    level += 1

            graph_data[edge_info[1]]['level'] = level

        algorithm = Algorithm(graph, persons, relation_dict, testator_id)
        algorithm.find_heir()

        nt = Network(600, 1700)
        nt.set_template(os.path.join(os.getcwd(), 'gentree', 'templates', 'pyvis_template.html'))
        nt.from_nx(graph)
        nt.set_options("""
            var options = {
              "edges": {
                "to": {
                    "enabled": true,
                    "type": "arrow"
                  },
                "color": {
                  "inherit": false
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

        return HttpResponse(nt.generate_html())
