import osmnx as ox

G = ox.graph_from_place('Beijing, China', which_result=2, network_type='drive')
G_proj = ox.project_graph(G)
fig, ax = ox.plot_graph(G_proj)