# Author: Andrew Liu

import networkx as nx

def InterAS(G, DictGWs):
	# Input: 
	# G is the global graph object
	# DictGWs is a dictionary object {ASnumber: [corrosponding gateway nodes id]}
	# Output: 
	# GW, a graph object in which the gateways have attribute ['InterTable']
	# ['InterTable'] is a dictionary {ASnumber: next gateway node id}

	# AS is a list object [ASnumber].
	AS = list(DictGWs.keys())

	# Create the gateway level graph object
	GW = nx.Graph()
	# Add the gateways to GW
	for i in AS:
		gatewayfori = DictGWs[i]
		for j in gatewayfori:
			GW.add_node(j)
	# Add the edges between the gateways
	for i in list(GW.nodes):
		for j in list(GW.nodes):
			if i != j:
				if G.has_edge(i,j):
					GW.add_edge(i,j)
	# Compute the InterTable for gateways in ASi
	for i in AS:
		gatewayfori = DictGWs[i]
		# Here j is the jth gateway in ASi
		for j in gatewayfori:
			# Compute the InterTable for jth gateway in ASi
			InterTableforj = {}
			for k in AS:
				if k != i:
					gatewayfork = DictGWs[k]
					lengthtogateway = []
					corrosgatewayid = []
					# Here l is the lth gateway in ASk
					for l in gatewayfork:
						lengthtogateway.append(nx.shortest_path_length(GW, source = j, target = l))	
						corrosgatewayid.append(l)
					# Find the shortest path for j to ASk
					index = lengthtogateway.index(min(lengthtogateway))
					corrospath = nx.shortest_path(GW, source = j, target = corrosgatewayid[index])
					InterTableforj[k] = corrospath[1]
			G.add_node(j, InterTable = InterTableforj)
