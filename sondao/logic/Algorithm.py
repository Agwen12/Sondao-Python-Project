import networkx as nx
from typing import List, Dict, Optional
# from sondao.GUI.sondao_web.gentree.models import Person, Relation
from sondao.logic.RelationTypes import RelationTypes
from sondao.logic.Person import Person


class Algorithm:
    def __init__(self, tree: nx.Graph, persons: List[Person], relation_dict: dict, testator_id: int):
        self.tree = tree
        self.persons = persons
        self.relation_dict = relation_dict
        self.testator_id = testator_id
        self.testator = self.get_person_obj(testator_id)
        self.inheritees = []

    def find_heir(self):
        """

        :return:
        """

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
            self.distibute_wealth(0.75, self.testator.children)
        else:
            self.distibute_wealth(1, self.testator.children, self.testator.spouse)

        print(list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}", self.inheritees)))

    def distibute_wealth(self, wealth: float, *args):

        the_truth = []
        inheritees = [person for sublist in args for person in sublist]
        # print(list(map(lambda x: f"{x.personal_info.name} {x.personal_info.surname}",  inheritees)))
        # print(list(map(lambda x: x.personal_info.can_inherit(),  inheritees)))
        if wealth == 0:
            print("[INFO] There is no more whealth to inherit")
            return True, wealth
        if len(inheritees) == 0:
            print("[INFO] No more inheritees and some wealth left")
            return False, wealth
        local_wealth = wealth
        equal_part = wealth / len(inheritees)
        for inheritee in inheritees:
            # print(inheritee.personal_info.name, inheritee.personal_info.surname)
            if inheritee.personal_info.can_inherit():
                # local_wealth -= equal_part
                # print(f"[INFO] {inheritee.personal_info.name} {inheritee.personal_info.surname} has inherited {equal_part} of money $$$$$")
                self.inheritees.append(inheritee)
                self.set_color(inheritee, "green")
            else:
                self.set_color(inheritee, "red")
                self.distibute_wealth(equal_part, inheritee.children)


    def get_person_obj(self, node) -> Optional[Person]:
        # level = dict(graph.nodes.data())[rel[0]]['level']
        # sc_person_id = dict(graph.nodes.data())[relation['second_relative_id']]['person']
        if node in dict(self.tree.nodes.data()):
            return self.persons[dict(self.tree.nodes.data())[node]['person']]

    def set_color(self, person: Person, color: str):
        dict(self.tree.nodes.data())[person.internal_id]['color'] = color