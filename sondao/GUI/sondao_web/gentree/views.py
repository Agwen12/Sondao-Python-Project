from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import DeleteView, UpdateView
from django.views.decorators.clickjacking import xframe_options_sameorigin
from sondao.logic.Person import Person as LPerson, Testator
from sondao.logic.PersonalInfo import PersonalInfo, RelativesInfo
from sondao.logic.RelationTypes import RelationTypes
from sondao.logic.Algorithm import Algorithm
from .forms import PersonForm, RelationFrom, DocumentForm
from .models import Person, Relation, Document
from pyvis.network import Network
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


class GeneralUpdateView(UpdateView):
    template_name = 'update_form.html'
    success_url = "/"
    fields = '__all__'

    class Meta:
        abstract = True


class PersonUpdateView(GeneralUpdateView):
    model = Person


class RelationUpdateView(GeneralUpdateView):
    model = Relation


class DocumentUpdateView(GeneralUpdateView):
    model = Document


class Index(TemplateView):
    template_name = "index.html"

    @staticmethod
    def post(request):
        forms = (form(request.POST) for form in (PersonForm, RelationFrom, DocumentForm))

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persons = list()
        self.testator_id = None
        self.graph = nx.Graph()
        self.relation_dict = dict()

    def _create_persons(self):
        persons_from_database = Person.objects.all()
        for item in persons_from_database.values():
            if item['is_testator']:
                personal_info = PersonalInfo(
                    name=item['name'], surname=item['surname'], PESEL=item['pesel'],
                    phone_number=item['phone_number'], home_address=item['home_address'],
                    birthday=item['birthday'], proxy=item['proxy'],
                    receive_confirmation_place=item['receive_confirmation_place']
                )
                self.testator_id = item['id']
                person = Testator(personal_info=personal_info, internal_id=item['id'])
            else:
                personal_info = RelativesInfo(
                    name=item['name'], surname=item['surname'], PESEL=item['pesel'],
                    phone_number=item['phone_number'], home_address=item['home_address'],
                    birthday=item['birthday'], proxy=item['proxy'],
                    receive_confirmation_place=item['receive_confirmation_place'],
                    want_inherit=item['want_inherit'],
                    supposed_death_notification=item['supposed_death_notification']

                )
                person = LPerson(personal_info=personal_info, internal_id=item['id'])

            self.graph.add_node(item['id'], label=f"{item['name']} {item['surname']}", physics=False, shape="box",
                                person=len(self.persons), level=2 if item['is_testator'] else None,
                                color='yellow' if item['is_testator'] else None)
            self.persons.append(person)

    def _create_relation_dict(self):
        relations = Relation.objects.order_by('first_relative').all()
        for relation in relations.values():
            rel = RelationTypes.from_string(relation['relation'])
            person_id = dict(self.graph.nodes.data())[relation['first_relative_id']]['person']
            sc_person_id = dict(self.graph.nodes.data())[relation['second_relative_id']]['person']
            if rel == RelationTypes.SPOUSE:
                self.persons[person_id].add_relative(self.persons[sc_person_id], rel)
            else:
                self.persons[sc_person_id].add_relative(self.persons[person_id], rel)
            self.relation_dict[(relation['first_relative_id'], relation['second_relative_id'])] = rel
            self.relation_dict[(relation['second_relative_id']), relation['first_relative_id']] = rel.opposite()
            self.graph.add_edge(relation['first_relative_id'],
                                relation['second_relative_id'],
                                label=str(rel))

    def _set_levels(self):
        for edge_info in nx.bfs_edges(self.graph, self.testator_id):
            level = dict(self.graph.nodes.data())[edge_info[0]]['level']
            match self.relation_dict[edge_info]:
                case RelationTypes.CHILD | RelationTypes.FULL_ADOPTED_CHILD | RelationTypes.PARTIAL_ADOPTED_CHILD:
                    level -= 1
                case RelationTypes.EX_SPOUSE | RelationTypes.SIBLING | RelationTypes.SPOUSE:
                    level = level
                case RelationTypes.PARENT:
                    level += 1

            dict(self.graph.nodes.data())[edge_info[1]]['level'] = level

    def _find_heirs(self):
        print("BEFORE =============================================================")
        Algorithm(self.graph, self.persons, self.relation_dict, self.testator_id).find_heir()
        print("AFTER =============================================================")

    def _create_html(self):
        nt = Network(600, 1700)
        nt.set_template(
            os.path.join(os.getcwd(), 'gentree', 'templates', 'pyvis_template.html'))
        nt.from_nx(self.graph)
        nt.set_options("""var options = {
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
              "sortMethod": "directed",
              "parentCentralization": true
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
        return nt.generate_html()

    @xframe_options_sameorigin
    def get(self, request):
        self._create_persons()
        self._create_relation_dict()
        self._set_levels()
        self._find_heirs()
        return HttpResponse(self._create_html())
