# Author: Andrew Liu

import networkx as nx
import InterAS as InterAS
import IntraAS as IntraAS
import project_utility as pu
import mcl as mcl 
import time

def recursive(G,start,dest, path):
	next = G.nodes[start]['IntraTable'][dest]
	path.append(next)
	if(next != dest):
		recursive(G,next,dest, path)

def pathfinding(SourceNodeID, DestNodeID, G):
	# The source and dest are in defferent ASes
	path = [SourceNodeID]
	if G.nodes[SourceNodeID]['AS_N'] != G.nodes[DestNodeID]['AS_N']:
		# Finf the gateway level path, GWpath
		# If the source is nongateway, send the packet to the default gateway first
		if G.nodes[SourceNodeID]['isGateway'] == False:
			path.extend(G.nodes[G.nodes[SourceNodeID]['DefaultGateway']]['InterTable'][str(G.nodes[DestNodeID]['AS_N'])])
		else:
			path2 = G.nodes[SourceNodeID]['InterTable'][str(G.nodes[DestNodeID]['AS_N'])]
			path.extend(path2[1:])
		# Complete the path from the gateway to the dest
		if path[-1] != DestNodeID:
			recursive(G, path[-1], DestNodeID, path)

	# The source and dest are in the same AS
	else:
		# Both the source and dest are gateways
		if (G.nodes[SourceNodeID]['isGateway'] == True) and (G.nodes[DestNodeID]['isGateway'] == True):
			path = G.edges[SourceNodeID,DestNodeID]['LogicalEdge']
		else:
			recursive(G, SourceNodeID, DestNodeID, path)
	print('The path from node {} to node {} is {}'.format(SourceNodeID, DestNodeID, path))
	return path

def TableSetup(G,filename,cluster_rate = 1.5):
	pu.buildG(G, filename)
	mcl.graph_clustering(G,cluster_rate)
	pu.get_gateway(G)
	DictGWs = G.graph['gateWayList']
	AS = list(DictGWs.keys())
	# Construct the IntraTable for each AS. 
	# Here, i is str
	for i in AS:
		nodesinASi = []
		# Find the nodes in ASi
		for j in list(G.nodes):
			if str(G.nodes[j]['AS_N']) == i:
				nodesinASi.append(j)
		IntraAS.IntraAS(G, i, nodesinASi, DictGWs)
	print('IntraTable have constructed')
	# Construct the InterTable
	InterAS.InterAS(G, DictGWs)
	print('InterTable have constructed')
