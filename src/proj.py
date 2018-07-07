import manager as m
import networkx as nx
import project_utility as p
import mcl as mcl
import matplotlib.pyplot as plt
G = nx.Graph()
p.buildG(G,"connection_100_v2.csv")
mcl.graph_clustering(graph = G,cluster_rate=1.5)
p.get_gateway(G)
print(G.nodes(data=True))
print(G.graph)
colors = ['r','g','b','y','black','pink','gray']
color_map = ['black'] * len(G)
for n in G.nodes():
    color_map[n] = colors[G.node[n]['AS_N']]
nx.draw_networkx(G,node_size = 10,width = 0.2,node_color = color_map,font_size = 5)
plt.show()
"""
g = m.Manager()
g.set_Configuration(layerNum = 4,layerNodeNum = [20,50,125,360], outputPath = "../connection_data/", 
conPara = {"1,1": 150,"1,2": 230,"2,2": 350,"2,3": 60,"3,3":60,"3,4":10,"4,4":16},
conDisPara= {"1,1": 1.5,"1,2": 1.5,"2,2": 1.5,"2,3": 1.5,"3,3":1.5,"3,4":1.5,"4,4":1.5},
graphName = "2018-6-20-100nodes")
g.generate_Graph()
g.print_Configuration()
print("Success")
"""