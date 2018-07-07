import csv
import random
import time
import datetime
import networkx as nx
from decimal import Decimal
import project_utility as pu
import os
import node_gen as ng

# Author: Henry
class Manager:
    def __init__(self):
        self.data = pu.Data()
        
    # Set the configuration in the data object.
    def set_Configuration(self, outputPath = "", graphName = "", disPara = [], genDisPara = {},
                          nodeGenPara = -1, layerNodeNum = [], layerNum = -1, conDegPara = {}, conDisPara = {}, conPara = {}):
        if (layerNum != -1):
            if (layerNum < 2):
                raise RuntimeError("Invalid layer Number!")
                
            else:
                self.data.Layer_Num = layerNum
        
        if (nodeGenPara != -1):
            self.node_Gen_Para = nodeGenPara

        if (graphName != ""):
            self.data.graph_Name = graphName

        if (outputPath != ""):
            self.data.output_Path = outputPath
        
        if (len(genDisPara) != 0):
            self.data.gen_Dispara = dict(genDisPara)
        else:
            for i in range(2,self.data.Layer_Num + 1):
                self.data.gen_Dispara[str(i)] = 2

        if (len(conPara) != 0):
            self.data.con_Para = dict(conPara)
        
        if (len(conDegPara) != 0):
            self.data.deg_Para = dict(conDegPara)
        else:
            for i in range(1,self.data.Layer_Num + 1):
                self.data.deg_Para[str(i) + ',' + str(i)] = 1
                if (i != self.data.Layer_Num):
                    self.data.deg_Para[str(i) + ',' + str(i + 1)] = 1

        if (len(conDisPara) != 0):
            self.data.con_Dispara = dict(conDisPara)
        else:
            for i in range(1,self.data.Layer_Num + 1):
                self.data.con_Dispara[str(i) + ',' + str(i)] = 1
                if (i != self.data.Layer_Num):
                    self.data.con_Dispara[str(i) + ',' + str(i + 1)] = 1

        for i in range(1,self.data.Layer_Num + 1):
            self.data.connection_Num[str(i) + ',' + str(i)] = 0
            if (i != self.data.Layer_Num):
                self.data.connection_Num[str(i) + ',' + str(i + 1)] = 0
        for i in range(1,self.data.Layer_Num + 1):
            self.data.connections[str(i) + '-' + str(i) + ',1'] = []
            self.data.connections[str(i) + '-' + str(i) + ',2'] = []
            if (i != self.data.Layer_Num):
                self.data.connections[str(i) + '-' + str(i + 1) + ',1'] = []
                self.data.connections[str(i) + '-' + str(i + 1) + ',2'] = []
        
        if (len(layerNodeNum) != 0):
            if (len(layerNodeNum) > self.data.Layer_Num):
                raise RuntimeError("Invalid layerNodeNum, too many arugment!")
            elif(len(layerNodeNum) < self.data.Layer_Num):
                raise RuntimeError("Invalid layerNodeNum, missing arugment!")
            else:
                if(layerNodeNum[0] > 48):
                    raise RuntimeError("layer one can only have upto 48 nodes!")
                buflist = list(layerNodeNum)
                buflist.insert(0,-1)
                self.data.layer_Node_Num = list(buflist)
      
        
    ### TODOs
    def print_Configuration(self):
        print("\nConfigurations")
        print("Layer_Num",self.data.Layer_Num)
        print("output_Path",self.data.output_Path)
        print("graph_Name",self.data.graph_Name)
        print("con_Para",sorted(self.data.con_Para.items()))
        print("deg_Para",sorted(self.data.deg_Para.items()))
        print("con_Dispara",sorted(self.data.con_Dispara.items()))
        print("node_Gen_Para",self.data.node_Gen_Para)
        print("gen_Dispara",sorted(self.data.gen_Dispara.items()))
        print("layer_Node_Num",self.data.layer_Node_Num[1:])
    
    # Aurthor: Henry & Pohan
    def generate_Graph(self):
        timeStart = time.time()
        print('Node generation starting...')
        # Variable definition
        layerNode = []
        for i in range(self.data.Layer_Num + 1):
            layerNode.append([])
        ID_count = 0

        # 1.Generate node
        ## 1-1 First Layer
        for i in range(self.data.layer_Node_Num[1]):
            node = pu.Node(ID_Num = ID_count)
            layerNode[1].append(node)
            node.connected = 1 # Layer_1 nodes will always be in the Graph (Layer 1 is the backbone of the internet)
            ID_count += 1

        CSV = csv.reader(open('1layer.csv'),delimiter = ',')
        count = 0
        for row in CSV:
            node = layerNode[1][count]
            count += 1
            node.x_pos = int(row[1])
            node.y_pos = int(row[0])
            if (count == self.data.layer_Node_Num[1]): # Can only have up to 50 layer1_Nodes
                break

        ## 1-2 Generate Second Layer
        ### Read Continent info
        cont_List = []
        CSV = csv.reader(open('continent.csv'),delimiter = ',')
        for row in CSV:
            buf_list = [row[0],row[1],row[2],row[3]] # Reading the continent info, (x1,y1,x2,y2) determines a rectangle.
            cont_List.append(buf_list)

        ### Generate nodes
        for layer in range(2,self.data.Layer_Num + 1):
            previous_layer = layer - 1
            while(len(layerNode[layer]) != self.data.layer_Node_Num[layer]): # Run loop until the required number of nodes is generated
                (x,y) = pu.map_Cordinate_Generator(continent_List = cont_List) # Returns a (x,y) that is in the restricted area
                node = pu.Node(ID_Num = ID_count,x_pos = x, y_pos = y)
                Sum = 0
                for node_p in layerNode[previous_layer]:
                    if(node.distance(node_p) != 0):
                        dis_r = 1/node.distance(node_p)
                    else:
                        dis_r = 1 # Just to avoid bug
                    Sum += dis_r ** self.data.gen_Dispara[str(layer)] # Use the total average distance
                pro = random.uniform(0, 1)
                if (pro < self.data.node_Gen_Para*Sum): # node_Gen_Para controls the speed of generating nodes. Don't set too large values
                    layerNode[layer].append(node)      
                    ID_count += 1
        
        timeEnd = time.time()
        print("Node generation time used: " + str(round(timeEnd - timeStart,2)) + " seconds")
        ### Generate Connection
        n_total = generate_Connection(Data = self.data,layers = layerNode)
        print("Connection generation time used: " + str(round(time.time() - timeEnd,2)) + " seconds")
        ### Calculate dimension
        dim = pu.dimension_calculation(n_total,(3600,1800),5,360.0,5,2)
        dim = round(dim,3)
        print("Graph dimension: " + str(dim))

        timeEnd = time.time()
        print("Total time used: " + str(round(timeEnd - timeStart,2)) + " seconds")

# Aurthor: Henry & Pohan
# generates the connection between nodes, according to the configurations.
# Connections will only exist in the same layer or bewteen upper and lower layes.
# Ex: 1-2, 2-2, 2-3
def generate_Connection(Data,layers):
   
   # Variables
    print("Connection generation starting...")
    # Layer 1-1
    for i in range(1,len(layers[1])):
        dis = layers[1][0].distance(layers[1][i]) 
        closest = 0
        minDis = 0
        for j in range(i - 1):
            if j == 0:
                minDis = layers[1][j].distance(layers[1][i])
            dis = layers[1][j].distance(layers[1][i]) 
            if minDis > dis:
                minDis = dis
                closest = j   

        layers[1][closest].deg += 1
        layers[1][i].deg += 1
        Data.connections['1-1,1'].append(layers[1][closest])
        Data.connections['1-1,2'].append(layers[1][i])
        for j in range(i-1):
            if (j != closest):
                pro = random.uniform(0, 1)
                if dis == 0:
                    dis = 1
                if pro < Data.con_Para['1,1']*(layers[1][j].deg**Data.deg_Para['1,1'])/(dis**Data.con_Dispara['1,1']): # This is where you need to read, see how the parameter affects the connection.
                    layers[1][i].deg += 1
                    layers[1][j].deg += 1
                    Data.connections['1-1,1'].append(layers[1][i])
                    Data.connections['1-1,2'].append(layers[1][j])
                 
    
    for layer in range(1,Data.Layer_Num):
        ### Connection between layer_i and layer_i+1
        key1 = str(layer) + ',' + str(layer + 1)
        key2 = str(layer + 1) + ',' + str(layer + 1)
        for node_i in layers[layer]:
            for node_j in layers[layer + 1]:
                dis = node_i.distance(node_j)
                pro = random.uniform(0, 1)
                if dis == 0:
                    dis = 1
                if pro < (Data.con_Para[key1]*(node_i.deg**Data.deg_Para[key1])/(dis**Data.con_Dispara[key1])):
                    node_i.deg += 1
                    node_j.deg += 1
                    node_i.target.append(node_j), node_j.target.append(node_i)
                    Data.connections[str(layer) + '-' + str(layer + 1) + ',1'].append(node_i)
                    Data.connections[str(layer) + '-' + str(layer + 1) + ',2'].append(node_j)
                    if (node_i.connected == 1):
                        node_j.connected = 1
                 
        ### Connection between layer_i+1 and layer_i+1
        for i in range(len(layers[layer + 1])):
            for j in range(i + 1,len(layers[layer + 1])):
                node_i = layers[layer + 1][i]
                node_j = layers[layer + 1][j]
                dis = node_i.distance(node_j) 
                if dis == 0:
                    dis = 1
                pro = random.uniform(0, 1)
                if (pro < Data.con_Para[key2]*(node_j.deg**Data.deg_Para[key2])/(dis**Data.con_Dispara[key2])):
                    node_j.deg += 1
                    node_i.deg += 1
                    node_i.target.append(node_j), node_j.target.append(node_i)
                    Data.connections[str(layer + 1) + '-' + str(layer + 1) + ',1'].append(node_i)
                    Data.connections[str(layer + 1) + '-' + str(layer + 1) + ',2'].append(node_j)
                    if (node_i.connected == 1 and node_j.connected == 0):
                        node_j.connected = 1
                        node_j.net()
                    if (node_j.connected == 1 and node_i.connected == 0):
                        node_i.connected = 1
                        node_i.net()

    # Removing isolated nodes
    # Delete the nodes that aren't in the graph
    n_total = []
    for layer in layers:
        n_total += layer
    pu.delete_unconnected_new_mapping(n_total)
    node_count = 0
    for node in n_total:
        if(node.ID != -10):
            node_count += 1

    # Writing connection data to csv
    file = open(Data.output_Path + str(Data.graph_Name) + ".csv",'w')
    s_connect = ""

    # Writing Links
    key = str(1) + '-' + str(1)
    for i in range(len(Data.connections[key + ',1'])):
        if (Data.connections[key + ',1'][i].ID != -10): # if the first node is in graph, the second one must be too.
            s_connect += str(Data.connections[key + ',1'][i].ID) + ',' + str(Data.connections[key + ',2'][i].ID) + '\n'
    for i in range(1,Data.Layer_Num):
        key = str(i) + '-' + str(i+1)
        for j in range(len(Data.connections[key + ',1'])):
            if (Data.connections[key + ',1'][j].ID != -10):
                s_connect += str(Data.connections[key + ',1'][j].ID) + ',' + str(Data.connections[key + ',2'][j].ID) + '\n'
                Data.connection_Num[str(i) + ',' + str(i+1)] += 1
        key = str(i+1) + '-' + str(i+1)
        for j in range(len(Data.connections[key + ',1'])):
            if (Data.connections[key + ',1'][j].ID != -10):
                s_connect += str(Data.connections[key + ',1'][j].ID) + ',' + str(Data.connections[key + ',2'][j].ID) + '\n'
                Data.connection_Num[str(i+1) + ',' + str(i+1)] += 1

    # Writing Parameters
    count = 0
    s = "# Created at " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\n'
    file.write(s)
    s = "# Connection parameters." + "\n# Layer1-1:" + str(Data.con_Para['1,1'])
    count += 1
    for layer in range(1,Data.Layer_Num):
        s += " Layer" + str(layer) + '-' + str(layer + 1) + ':'  + str(Data.con_Para[str(layer) + ',' + str(layer + 1)])
        count += 1
        if (count >= 3):
            count = 0
            s += '\n' + "#"
        s += " Layer" + str(layer + 1) + '-' + str(layer + 1) + ':'  + str(Data.con_Para[str(layer + 1) + ',' + str(layer + 1)])
        count += 1
    file.write(s)
    count = 0
    s = '\n' + "# Connection Num." + "\n# Layer1-1:" + str(len(Data.connections['1-1,1']))  
    for layer in range(1,Data.Layer_Num):
        s += (" Layer" + str(layer) + '-' + str(layer + 1) + ':' + str(Data.connection_Num[str(layer) + ',' + str(layer + 1)]))
        count += 1
        if (count >= 3):
            count = 0
            s += '\n' + "#"
        s += (" Layer" + str(layer + 1) + '-' + str(layer + 1) + ':' + str(Data.connection_Num[str(layer + 1) + ',' + str(layer + 1)]))
        count += 1
    file.write(s)
    s = '\n' + "# Lowest level starting ID, total router number\n"
    file.write(s)
    s = str(len(layers[1])) + ',' + str(node_count) + '\n'
    file.write(s)
    s = "# NodeID, x_pos, y_pos, degree\n"
    # Writing Node info
    for layer in layers:
        for node in layer:
            if (node.ID != -10):
                s += str(node.ID) + ',' + str(node.x_pos) + ',' + str(node.y_pos) + ',' + str(node.deg) + '\n'
    file.write(s)
    # Writing Links
    s = "# links\n"
    file.write(s)
    s_connect += "c"
    file.write(s_connect)
    return n_total