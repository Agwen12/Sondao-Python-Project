import networkx as nx
from typing import List, Dict, Optional
# from sondao.GUI.sondao_web.gentree.models import Person, Relation
from sondao.logic.RelationTypes import RelationTypes
from sondao.logic.Person import Person
import functools as ft


class Algorithm:
    def __init__(self, tree: nx.Graph, persons: List[Person], relation_dict: dict, testator_id: int):
        self.tree = tree
        self.persons = persons
        self.relation_dict = relation_dict
        self.testator_id = testator_id
        self.testator = self.get_person_obj(testator_id)
        self.inheritees = []

    def find_heir(self):
        print("CHILDREN", list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}",
                                   self.testator.children)))
        print("PARENTS", list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}",
                                  self.testator.parents)))
        print("SIBLINGS", list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}",
                                   self.testator.siblings)))
        print("SPOUSE", list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}",
                                 self.testator.spouse)))

        # print("INFO", dict(self.tree.nodes.data()))
        if len(self.testator.spouse) + len(self.testator.children) > 4:
            print("MALZONEK DOSTAJE 1/4 majatku", self.testator.spouse[0].personal_info.name)
            self.set_color(self.testator.spouse[0], 'green')
            self.inheritees.append(self.distibute_wealth(0.75, self.testator.children))
        else:
            self.distibute_wealth(1, self.testator.children, self.testator.spouse)

        print(self.inheritees)


    def distibute_wealth(self, wealth: float, *args):

        the_truth = []
        inheritees = [person for sublist in args for person in sublist]
        if wealth == 0:
            print("[INFO] There is no more whealth to inherit")
            return None
        if len(inheritees) == 0:
            print("[INFO] No more inheritees and some wealth left")
            return None
        equal_part = wealth / len(inheritees)
        for inheritee in inheritees:
            # print(inheritee.personal_info.name, inheritee.personal_info.surname)
            if inheritee.personal_info.can_inherit():

                # print(f"[INFO] {inheritee.personal_info.name} {inheritee.personal_info.surname} has inherited {equal_part} of money $$$$$")
                the_truth.append((inheritee.personal_info.name, inheritee.personal_info.surname))
                self.set_color(inheritee, "green")
            else:
                self.set_color(inheritee, "red")
                res = self.distibute_wealth(equal_part, inheritee.children)
                if res is not None:
                    the_truth.append(res)

        return wealth, the_truth if len(the_truth) > 0 else None

    def money_money(self):
        """"""

    def get_person_obj(self, node) -> Optional[Person]:
        # level = dict(graph.nodes.data())[rel[0]]['level']
        # sc_person_id = dict(graph.nodes.data())[relation['second_relative_id']]['person']
        if node in dict(self.tree.nodes.data()):
            return self.persons[dict(self.tree.nodes.data())[node]['person']]

    def set_color(self, person: Person, color: str):
        dict(self.tree.nodes.data())[person.internal_id]['color'] = color