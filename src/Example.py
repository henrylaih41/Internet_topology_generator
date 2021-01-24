import manager as m
import networkx as nx
import project_utility as p
import mcl as mcl
import matplotlib.pyplot as plt
import TableSetup as t
# generating a graph (output is a csv file)
def generate_graph_example():
    g = m.Manager()
    g.set_Configuration(layerNum = 4,layerNodeNum = [48,50,100,100], outputPath = "../connection_data/",
    conPara = {"1,1": 150,"1,2": 230,"2,2": 350,"2,3": 60,"3,3":60,"3,4":10,"4,4":16},
    conDisPara= {"1,1": 1.5,"1,2": 1.5,"2,2": 1.5,"2,3": 1.5,"3,3":1.5,"3,4":1.5,"4,4":1.5},
    graphName = "example")
    g.generate_Graph()
    print("Success")

# draw the graph from example.csv
def draw_graph_from_csv_example():
    # Get the final graph using TableSetup()
    G = nx.Graph()
    t.TableSetup(G,"../connection_data/example.csv",1.2)
    # Can only support 7 AS, add more color if there is more AS.
    colors = ['r','g','b','y','black','pink','gray']
    color_map = ['black'] * len(G)
    for n in G.nodes():
        color_map[n] = colors[G.nodes[n]['AS_N']]
    nx.draw_networkx(G,node_size = 10,width = 0.2,node_color = color_map,font_size = 5)
    plt.show()

if __name__ == "__main__":
     generate_graph_example()
     draw_graph_from_csv_example()
