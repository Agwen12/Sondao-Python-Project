from dataclasses import dataclass, field
from Person import Testator, Person
from RelationTypes import RelationTypes
import networkx as nx


# TODO DO GUI!
@dataclass
class Tree:
    root: Testator
    next_node_num: int = 0
    graph: nx.Graph = field(default_factory=lambda: nx.Graph())

    def __post_init__(self):
        # ADD ROOT FOR GRAPH
        self.graph.add_node(self.next_node_num)
        #TODO add infos for nodes (PERSON OR SPECIFIC INFO FROM PERSON)
        self.next_node_num += 1

    def draw(self):  # TODO write drawing
        pass

    def add(self, parent_node: Person, relation: RelationTypes):  # TODO add new nodes
        pass
