import random
import numpy as np
import csv
import itertools as iter
import node_gen as n
# Author: Henry
# Node represents a connected device in the internet, ex: router
class Node:
    
    def __init__(self,ID_Num,x_pos = 0,y_pos = 0):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.deg = 0
        self.target = []   # stores the nodes that are connected to this node 
        self.connected = 0 # If connected is set to 1 means this node is in the graph, else it is out of the graph.
        self.ID = ID_Num # The node's ID
    
    # Calculates distance between two nodes
    # get_distance is written is cython
    def distance(self,other_Node):
        return n.get_distance(self.x_pos,other_Node.x_pos,self.y_pos,other_Node.y_pos)
        
    # Set the target node's connected flag to true, recursively called.
    # A node being connected means that it is directly or indirectly connected to 
    # the layer_1 nodes.
    def net(self):
        for node in self.target:
            if node.connected == 0:
                node.connected = 1
                node.net()

# Author: Henry
# The class for storing configurations.
# Set with some default values
class Data:
    def __init__(self):
        self.Layer_Num = 2
        self.output_Path = "./"
        self.graph_Name = "Default"
        self.con_Para = {}
        self.con_Para['1,1'] = 75
        self.con_Para['1,2'] = 6
        self.con_Para['2,2'] = 10
        self.deg_Para = {}
        for i in range(1,self.Layer_Num + 1):
            self.deg_Para[str(i) + ',' + str(i)] = 1
            if (i != self.Layer_Num):
                self.deg_Para[str(i) + ',' + str(i + 1)] = 1
        self.con_Dispara = {}
        for i in range(1,self.Layer_Num + 1):
            self.con_Dispara[str(i) + ',' + str(i)] = 1
            if (i != self.Layer_Num):
                self.con_Dispara[str(i) + ',' + str(i + 1)] = 1
        self.gen_Dispara = {}
        for i in range(2,self.Layer_Num + 1):
            self.gen_Dispara[str(i)] = 1.5
        self.node_Gen_Para = 100
        self.layer_Node_Num = [-1] * (self.Layer_Num + 1)
        for i in range(1,self.Layer_Num + 1):
            self.layer_Node_Num[i] = 20*(5*i - 4)
        ### storing the node connections as a dictionary
        self.connections = {}
        self.connection_Num = {}
        for i in range(1,self.Layer_Num + 1):
            self.connection_Num[str(i) + ',' + str(i)] = 0
            if (i != self.Layer_Num):
                self.connection_Num[str(i) + ',' + str(i + 1)] = 0
        for i in range(1,self.Layer_Num + 1):
            self.connections[str(i) + '-' + str(i) + ',1'] = []
            self.connections[str(i) + '-' + str(i) + ',2'] = []
            if (i != self.Layer_Num):
                self.connections[str(i) + '-' + str(i + 1) + ',1'] = []
                self.connections[str(i) + '-' + str(i + 1) + ',2'] = []
             
# Author: Henry
# Just a class for the function map_Cordinate_Generator(continent_List)
class Region:
    def __init__(self,y1_pos,x1_pos,y2_pos,x2_pos):
    # The four vertex of the region.
        self.x1 = x1_pos
        self.y1 = y1_pos
        self.x2 = x2_pos
        self.y2 = y2_pos
        self.area = abs(x1_pos - x2_pos) * abs(y1_pos - y2_pos)
    Regions = [] # Static, can be seen as a global variable within the class.
    sum = 0 # Static

# Author: Henry
# This function is for generating (x,y) pairs with specific restriction, since
# there is no router on the sea.
# Return (x,y) coordinate pairs that locates on the continents in continent_List
def map_Cordinate_Generator(continent_List):
    if (len(Region.Regions) == 0): # Read the continent_List if it haven't yet.
        for list in continent_List:
            # All region is a rectangle, defined by four vertex.
            region = Region(int(list[0]),int(list[1]),int(list[2]),int(list[3]))
            Region.Regions.append(region)
        
        for region in Region.Regions:
            Region.sum += region.area # Sum up the Region area

    pro = random.randrange(0,Region.sum)
    sum_buf = 0
    # the probability is directly proportional to the continent's area
    for region in Region.Regions:
        if (sum_buf <= pro < sum_buf + region.area):
            x = random.randrange(region.x1,region.x2)
            y = random.randrange(region.y2,region.y1)
            return (x,y)
        sum_buf += region.area

# Author: Pohan
# Because of some unconnected nodes, we need to remove them from the graph.
# we do this by changing the ID mapping, setting the unconnected node's ID to -10
# then reorder the rest of the nodes.
def delete_unconnected_new_mapping( node_array ): # Input is an array of nodes
    node_mapping = []
    length = len(node_array)
    for j in range(length):
        node_mapping.append(j)
    for i in range(length):
        if node_array[i].connected == 0:
            node_mapping[i] = -10 # Set the iD to -10 if the node is not in the graph.
            for j in range(i+1,length):
                node_mapping[j] = node_mapping[j] -1
    for i in range(length):
        node_array[i].ID = node_mapping[i]

# Author: Andrew
def dimension_calculation(image, image_size,unit, initial_box_size, number_of_linear_regression, scale):
    # image would be a list of object(node)
    # suggest setting initial_box_soze to be 1/100 of image_size, unit = 1
    # unit is the unit for transforming the image from point format to pixel format
    b = initial_box_size
    q = number_of_linear_regression
    (m,n) = image_size
    
    # Build successive box sizes, 1/10 smaller
    sizes = b/(scale**np.arange(0,q,1))
    
    # Extract the positions of image
    image_pos = []
    for i in image:
        image_pos.append([i.x_pos/10 + 1800,i.y_pos/10 + 900])
    
    # Transform the point graph to pxiel image where 1 means existing point
    (px,py) = (int(m/unit), int(n/unit))
    pixel_image = np.zeros((px+1,py+1))
    for i in image_pos:
        bx = int(i[0]/unit)
        by = int(i[1]/unit)
        pixel_image[(bx,by)] = 1
    # The positions of pixels at where points exist
    points = np.transpose(np.nonzero(pixel_image))*unit
    
    # Count the number of boxes
    def box_count(image,k): # z is the image and k is the box size
        (nx,ny) = (int(m/k), int(n/k))
        boxcount = np.zeros((nx+1,ny+1))
        for i in points:
            ppx = int(i[0]/k)
            ppy = int(i[1]/k)
            boxcount[(ppx,ppy)] = 1
        return np.count_nonzero(boxcount)

    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        counts.append(box_count(image_pos, size))
    # Calculate the dimension with linear regression
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]

# Author: Henry
# Construct the graph from the file_ (.csv)
def buildG(G, file_, delimiter_=','):
    start_reading_links = False
    read_node_num = False
    reader = csv.reader(open(file_), delimiter=delimiter_)
    for line in reader:
        if(line[0] == "# links"):
            start_reading_links = True
            continue
        if(line[0] == "# Lowest level starting ID"):
            read_node_num = True
            continue
        if(line[0] == "c"):
            break
        if(read_node_num):
            for i in range(int(line[1])):
                G.add_node(i)
            read_node_num = False
        if(start_reading_links):
            if len(line) > 2:
                if float(line[2]) != 0.0:
                    #line format: u,v,w
                    G.add_edge(int(line[0]),int(line[1]),weight=float(line[2]))
            elif len(line) == 2:
                #line format: u,v
                G.add_edge(int(line[0]),int(line[1]),weight=1.0)

# Author: Henry
# gets the gateway router in different AS, must run mcl.graph_clustering first.
def get_gateway(G):
    G.graph['gateWayList'] = {}
    for i in range(G.graph['Total_AS']):
        G.graph['gateWayList'][str(i)] = set()
    for e in G.edges():
        if(G.node[e[0]]['AS_N'] != G.node[e[1]]['AS_N']):
            G.add_node(e[0],isGateway = True)
            G.add_node(e[1],isGateway = True)
            G.graph['gateWayList'][str(G.node[e[0]]['AS_N'])].add(e[0])
            G.graph['gateWayList'][str(G.node[e[1]]['AS_N'])].add(e[1])
        else:
            if((G.node[e[0]].get('isGateway')) == None):
                G.add_node(e[0],isGateway = False)
            if((G.node[e[1]].get('isGateway')) == None):
                G.add_node(e[1],isGateway = False)
    connect_interAS_gateway(G)
# Author: Henry
# connects all the gateWay in the Same AS.
# According to BGP, InterAS gateways should be fully connected.
def connect_interAS_gateway(G):
    for AS_Num in G.graph['gateWayList']:
        for pairs in iter.combinations(G.graph['gateWayList'][AS_Num],2):
            G.add_edge(pairs[0],pairs[1])
