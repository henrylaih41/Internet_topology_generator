import markov_clustering as mc
import networkx as nx
import csv
from cmty import buildG
import sys
import matplotlib.pyplot as plt

def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <input graph>\n" % (argv[0],))
        return 1
    graph_fn = argv[1]
    G = nx.Graph()  #let's create the graph first
    buildG(G, graph_fn, ',')
    n_Matrix = nx.to_scipy_sparse_matrix(G)
    result = mc.run_mcl(n_Matrix,inflation=1.1)
    clusters = mc.get_clusters(result)
    print(clusters)
    print("Number of clusters: " + str(len(clusters)))
    for c in clusters:
        print(len(c))
    mc.draw_graph(n_Matrix, clusters,
    node_size=10, with_labels=False, edge_color="black",width=0.2)
    plt.show()
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))
