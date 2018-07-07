# Author: Andrew Liu

import networkx as nx

def IntraAS(G, ASnumber, nodesinthisAS, DictGWs):
	# Input: 
	# G is the input graph 
	# ASnumber is the ASnumber for this AS to find the gateway in this AS
	# nodeinthisAS is a list object containing the node id of all nodes in this AS
	# DictGWs is a dict object like {ASnumber: corrosponding gateways id}
	# Output: 
	# G, a graph object in networkx
	# The nongatwway nodes in G have attribute 'AS number', 'InterTable', and 'DefaultGateway'
	# 'InterTable' and 'DefaultGateway' will be created later
	# The gateway nodes in G have attribute 'AS number', 'InterTable', and 'IntraTable'
	# 'InterTable' will be created later
	# 'IntraTable' will be created by another function InterAS

	gateway = DictGWs[ASnumber]

	for i in nodesinthisAS:
		# Compute the shortest path for node i to the other nodes
		p = {}
		for j in nodesinthisAS:
			if j != i:
				p[j] = nx.shortest_path(G, source = i, target = j)
		
		lengthtogateway = []
		corrosgatewayid = []
		flag = (i in gateway)

		for j in p:
			# Check if node[i] is nongateway
			if flag == False:
				# Record the length of path of nongateway node[i] to each gateway
				if j in gateway:
					lengthtogateway.append(len(p[j])) 
					corrosgatewayid.append(j)

			# Construct the forwarding table for each node in the same AS
			# The type of the 'IntraTable' is dictionary {dest: next node id}
			if len(p[j]) != 1:
				p[j] = p[j][1]
			else:
				p[j] = p[j][0]
		G.add_node(i, IntraTable = p)
		# 'DefaultGateway' is the next node id to the cloest (shortest path length) gateway for the node[i]
		if flag == False:
			index = lengthtogateway.index(min(lengthtogateway))
			G.add_node(i, DefaultGateway = nx.shortest_path(G, source = i, target = corrosgatewayid[index])[1])

