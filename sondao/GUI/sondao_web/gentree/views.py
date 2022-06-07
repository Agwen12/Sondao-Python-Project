from django.http import HttpResponse, HttpResponseRedirect
from pyvis.network import Network
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from sondao.logic.Person import Person as LPerson
from sondao.logic.PersonalInfo import PersonalInfo, RelativesInfo
from sondao.logic.RelationTypes import RelationTypes as RT

from .forms import PersonForm
from .models import Person
from sondao.logic.Algorithm import Algorithm

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
    persons = []
    relation_dict = dict()
    testator_id = None
    for item in items.values():
        # print(item)
        if item['is_testator']:
            personal_info = PersonalInfo(
                name=item['name'], surname=item['surname'], PESEL=item['pesel'],
                phone_number=item['phone_number'], home_address=item['home_address'],
                birthday=item['birthday'], proxy=item['proxy'],
                receive_confirmation_place=item['receive_confirmation_place']
            )
            testator_id = item['id']
        else:
            personal_info = RelativesInfo(
                name=item['name'], surname=item['surname'], PESEL=item['pesel'],
                phone_number=item['phone_number'], home_address=item['home_address'],
                birthday=item['birthday'], proxy=item['proxy'],
                receive_confirmation_place=item['receive_confirmation_place'],
                want_inherit=item['want_inherit'],
                supposed_death_notification=item['supposed_death_notification']
            )

        person = LPerson(personal_info=personal_info)

        graph.add_node(item['id'],
                       label=f"{item['name']} {item['surname']}",
                       physics=False,
                       shape="box",
                       person=len(persons),
                       level=2 if item['is_testator'] else None,
                       color='yellow' if item['is_testator'] else None
                       )
        persons.append(person)
    relations = Relation.objects.order_by('first_relative').all()
    for relation in relations.values():
        rel = RT.from_string(relation['relation'])
        person_id = dict(graph.nodes.data())[relation['first_relative_id']]['person']
        sc_person_id = dict(graph.nodes.data())[relation['second_relative_id']]['person']
        persons[sc_person_id].add_relative(persons[person_id], rel)
        relation_dict[(relation['first_relative_id'], relation['second_relative_id'])] = rel
        relation_dict[(relation['second_relative_id']), relation['first_relative_id']] = rel.opposite()
        graph.add_edge(relation['first_relative_id'],
                       relation['second_relative_id'],
                       label=str(relation['relation']))

    T = nx.bfs_edges(graph, testator_id)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n")
    for b in graph.nodes.data():
        # print(b)
        print(persons[b[1]['person']].personal_info.name, persons[b[1]['person']].personal_info.surname)
        print("childern", list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}", persons[b[1]['person']].children)))
        print("parents", list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}", persons[b[1]['person']].parents)))
        print("siblings", list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}", persons[b[1]['person']].siblings)))
        print("#====================================================#")

    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n\n")
    a = list(T)
    # print(graph.edges)
    print(relation_dict)
    # print(a)
    for rel in a:
        # print(rel, relation_dict[rel])
        # print("LEVEL ", dict(graph.nodes.data())[rel[0]]['level'])
        level = dict(graph.nodes.data())[rel[0]]['level']
        match relation_dict[rel]:
            case RT.CHILD | RT.FULL_ADOPTED_CHILD | RT.PARTIAL_ADOPTED_CHILD:
                level -= 1
            case RT.EX_SPOUSE | RT.SIBLING | RT.SPOUSE:
                level = level
            case RT.PARENT:
                level += 1

        dict(graph.nodes.data())[rel[1]]['level'] = level

    a = Algorithm()

    a.find_heir()

    nt = Network(600, 1700)
    nt.set_template(
        "D:\\sem4\\PYTHON\\Sondao-Python-Project\\sondao\\GUI\\sondao_web\\gentree\\templates\\template.html")
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
