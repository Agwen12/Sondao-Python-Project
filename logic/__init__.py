import pyvis.network
from pyvis.network import Network
import networkx as nx

nt = Network(height=1000, width=2000, font_color="black", bgcolor='white', heading='Treeeeee')
g = nx.Graph()
g.add_node(1, label="Feliks B", shape="box", level=1, physics=False)
g.add_node(2, label="Franciszek B", shape="box", level=0)
g.add_node(3, label="Bernadyka B", shape="box", level=0)
g.add_node(4, label="Zofia B", shape="box", level=1, physics=False)
g.add_node(5, label="Franciszek B", shape="box", level=1)
g.add_node(6, label="Zenon B", shape="box", level=1)
g.add_node(7, label="Zenon D", shape="box", level=1)

g.add_edge(2, 1)
g.add_edge(3, 1)
g.add_edge(4, 1)
g.add_edge(5, 1)
g.add_edge(6, 1)
g.add_edge(7, 1)

nt.from_nx(g)
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
      "nodeSpacing": 60,
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
nt.show("nx.html")
