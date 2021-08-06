[TOC]
# Prerequest
## Install networkx, mcl and cython
```
pip3 install networkx
pip3 install markov_clustering
pip3 install cython
```
or download or fork [https://github.com/GuyAllard/markov_clustering](https://)
## Clone the project
Download or fork the project [https://github.com/henrylaih41/Internet_topology_generator](https://github.com/henrylaih41/Internet_topology_generator)


# Network Topology Generator
## Introduction
This program can generate a network topology graph of which the configuration can be set by the users. 
The user needs import the manager.py first; then, the user needs construct a class called manager which includes the network generating function and set configuration function.

Before introducing the functions of manager, we realize the parameters and the generating rules of the node and the link  of the network topolofy.
## Parameters
### SetConfiguration
#### 1.layerNum
Each node in the topology is classied  by the layer they located.
Note that the layerNum must be greater than 1. 
#### 2.layerNodeNum
The **layerNodeNum** parameter is  a list object storing the number of nodes in each layer.
#### 3.nodeGenPara & genDisPara
Both nodeGenPara and genDisPara are list objects.
The rule of generating nodes is calculating the $\dfrac {1}{N}\sum ^{N}_{n=0}\dfrac {1}{d^{\alpha }}$, where $\alpha$ is **genDisPara**, between the random generating node in layer n and the entire N nodes in layer n-1.
If $p(random)<kp$, where $p=\dfrac {1}{N}\sum ^{N}_{n=0}\dfrac {1}{d^{\alpha }}$ and k is **nodeGenPara**, the node can exist at that posistion.

Note that the nodeGenPara is for accelerating the node generating process. nodeGenPara should increase as the node number increase.
#### 4.conPara & conDegPara & conDisPara
The probability of having connection between two nodes is $k\dfrac {w^{\alpha }}{d^{\beta }}$ where $\alpha$ is **ConDegPra**, w is degree, $\beta$ is **ConDisPra**, d is distance, and k is **conPara**.

conPara, conDegPara, and conDisPara are all directionary of which key is [layern,layern+1].

Note that the node in layer n can only has connections between the nodes in n-1, n, and n+1 layers.

### Clustering
#### 1.cluster_rate
To assign AS number to each node in the topology, we use markov clustering to divide the topology into different ASes.
There is only one variable in markov clustering, **cluster_rate**.
The larger the cluster_rate, the more the number of AS, i.e. the smaller the AS.
Recommend value: 1.1 ~ 1.9

## Functions
Now, we can introduce the functions in class manager.
### 1.manager.set_Configuration (outputPath, graphName, layerNum, layerNodeNum, genDisPara, nodeGenPara, conDegPara, conDisPara, conPara)
The input of set_Configuration function are the parameters introduced before and the output path and the graphname.
### 2.manager.generate_Graph(self)
If the user does not set the configuration in advance, the configuration of topology generated is the default value.
### 3.manager.print_Configuration(self)
print("Configurations:......")

## Output CSV Format
Sample
```
# Created at 2018-07-07 21:36:13
# Connection parameters.
# Layer1-1:150 Layer1-2:230 Layer2-2:350 Layer2-3:60
# Layer3-3:60 Layer3-4:10 Layer4-4:16
# Connection Num.
# Layer1-1:19 Layer1-2:24 Layer2-2:10 Layer2-3:32
# Layer3-3:11 Layer3-4:9 Layer4-4:1
# Lowest level starting ID, total router number
20,77
# NodeID, x_pos, y_pos, degree
0,12129,3110,8
...
# Links
0,1
...
```

# Routing Table Setup
## Introduction
Since we know all information about the graph, we can find the shortest path between two nodes by link state algorithm.
In this project, we use Dijkstra's algorithm which  is a famous link state algorithm.
To see how Dijkstra's algorithm runs, refer to [https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm](https://)

## IntraAS
To construct the routing table for interAS path, the source and destination are at the same AS, we use OSPF algorithm.
In this project, we do not divide an AS into multiple areas.
To implement OSPF, we first use Dijkstra's algorithm to find the shortest path from a node to all the other nodes in the same AS.
Then, we reocrd the next hop to the corrosponding destination to construct the intraAS routing table, i.e. G.nodes[i].['IntraTable'] is dictionary {dest: next node id}

## InterAS
We divide the BGP protocol into eBGP and iBGP.
To complete eBGP, we constrcut the AS_PATH to each gateway.
The way to construct AS_PATH:
1. Construct a gateway-level graph
2. For each node, it can find the shortest path for all the other AS, this is modified AS_PATH which stored the gateway id instead of AS number along the path

Then, we record the next gateway id to the corrosponding AS number to construct the interAS routing table, i.e. G.nodes[i].['InterTable'] is a dictionary {ASnumber: next gateway node id}

Notice that, according to the policy of BGP,  we connected all the gateways inside a AS (at function getgateway so you will not see the this in the connection csv).

For nongateway nodes, we use hot-potato algorithm instead of iBGP. 
In hot-potato algorithm, each nonegateway nodes send the packet of which destination is outside the AS to the closest gateway(minimum intraAS cost).
After finding the closest gateway, we record the next hop to construct the default gateway, i.e. G.nodes[i].['DefaultGateway'] is the the next node id to the cloest (shortest path length) gateway for the node[i]


## How to use the TableSetup function
1. Construct the toplogy by manager.py which is introduced in the section **Network Topology Generator**; then, there will a csv file be created.
2. Run the TableSetup in TableSetup.py. 
```
TableSetup(G,filename,cluster_rate)
```  
   G: a empty networkx graph object
   filename: the filename of the topology you just created,    cluster_rate: introduced in the clustering section and recommend value is 1.1 ~ 1.9.
   Then, you can reach the routing table stored in the atrribute of nodes.
   
## Summary
For nonegateway nodes, they contain **IntraTable** and **DefaultGateway** which can be attained by 
```
G.nodes[i].['IntraTable']
G.nodes[i].['DefaultGateway']
```
For gateways, they contain  **IntraTable** and **InterTable** which can be attained by 
```
G.nodes[i].['IntraTable']
G.nodes[i].['InterTable']
```

# Sample code
The sample code is located in src/Example.py, you can run the code simply by the following command, its takes around 15s to run
```
python3 Example.py
```
```python=
import manager as m
import networkx as nx
import project_utility as p
import mcl as mcl
import matplotlib.pyplot as plt
import TableSetup as t

# generating a graph (output is a csv file)
def generate_graph_example():
    g = m.Manager()
    g.set_Configuration(layerNum = 4,layerNodeNum = [20,50,100,100], outputPath = "../connection_data/", 
    conPara = {"1,1": 150,"1,2": 230,"2,2": 350,"2,3": 60,"3,3":60,"3,4":10,"4,4":16},
    conDisPara= {"1,1": 1.5,"1,2": 1.5,"2,2": 1.5,"2,3": 1.5,"3,3":1.5,"3,4":1.5,"4,4":1.5},
    graphName = "example")
    g.generate_Graph()
    print("Success")

# draw the graph from example.csv()
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
     
# The network topology and its routing table, intraAS and interAS, have been created.
# If want to access the routing table,
# For gateways,
G.nodes[i].['IntraTable']
G.nodes[i].['InterTable']
# For nongateway node,
G.nodes[i].['IntraTable']
G.nodes[i].['DefaultGateway']
```
