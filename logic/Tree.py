from dataclasses import dataclass, field
from datetime import date
from Person import Testator
import networkx as nx
from pyvis.network import Network

#TODO SEE WHATS MORE
@dataclass
class Tree:
    root: Testator
    next_node_num: int = 0
    graph: nx.Graph = field(default_factory=lambda: nx.Graph())

    def __post_init__(self): #TODO problably use .add() method
        # ADD ROOT FOR GRAPH
        self.graph.add_node(self.next_node_num)
        self.next_node_num += 1




    def draw(self): #TODO write drawing
        pass


    def add(self): #TODO add new nodes
        pass