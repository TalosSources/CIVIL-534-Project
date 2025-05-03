import json
import networkx as nx
import matplotlib.pyplot as plt

json_file = open("world3-03_variables.json")
w3_vars = json.loads(json_file.read())
json_file.close()

G = nx.DiGraph()
for name, val in w3_vars.items():
    G.add_node(name, var_type=val["type"])
    if val["dependencies"] is not None:
        G.add_edges_from([(dep, name) for dep in val["dependencies"]])
