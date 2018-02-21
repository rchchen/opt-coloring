#!/usr/bin/python
# -*- coding: utf-8 -*-

# problems to think: 1. which node to color first 2.If multiple colors are available, say from 0,1,4,5 both 2,3 are free, which one to choose?
import math

def getOccurrence(item):
	return item[1]

def getID(item):
	return item[0]
 
	#color shall be returned from this function
def getSmallestAvailableColor(coloredNodes, tempNode):
	#coloredNodes: [[nodeID,color],[],[]...]
	#tempNode, currentNode:[currentNodeID, node 1, node 2..] node 1, node 2 and etc. are connected with currentNode
	currentColors = []
	currentNode = list(tempNode) #remake list of tempNode
	del currentNode[0] #remove first element from currentNode, the remaining would be neighbor nodes
	if len(coloredNodes) == 0:
		return 0
	#find colors that neighbors are already using
	for neighbor in currentNode:
		for x in coloredNodes:
			if (x[0] == neighbor) and (x[1] not in currentColors):
				currentColors.append(x[1])
	currentColors = sorted(currentColors) #re-arrange currentColors from small to large

	if len(currentColors) == 0:  # if there are no colored nodes
		return 0
	counter = 0
	for tempColor in currentColors: #return the smallest color
		if tempColor != counter:
			color = counter
			return color
		counter = counter + 1

	return currentColors[-1]+1

# Criteria 1: choose node based on three criteria: a.is not colored;  b.is connected to an existing colored node; c.has higher degree;
def getChosenNode_crt1(uncoloredNodes,coloredNodes,nodesArr):
	# nodes:[[nodeID,occurrence,color],[],[],...]
	# coloredNodes: [[nodeID,color],[],[]...]
	# nodesArr:[[currentNodeID, node 1, node 2..]]node 1, node 2 and etc. are connected with currentNode
	if len(coloredNodes) ==0:
		chosenNode = uncoloredNodes[0]
		del uncoloredNodes[0]
	else:
		neighbors = []
		for element in coloredNodes:
			# find neighbors of all colored nodes including colored nodes
			_nodeID = element[0]
			neighbors = nodesArr[_nodeID] + neighbors

		chosenNode = uncoloredNodes[0] # if no ranked nodes are in neighbors, choose the one with highest degree
		for element in uncoloredNodes:
			_nodeID = element[0]
			if _nodeID in neighbors:
				chosenNode = element
				break
		del uncoloredNodes[uncoloredNodes.index(chosenNode)]
	return chosenNode

# Criteria 2: choose high degree node firstly, choose neighbors of high degree node secondly, choose second high degree node thirdly and etc...
def getChosenNode_crt2(neighborsTobeColored, nodes, uncoloredNodes,nodesArr, counter, orderedNodes):
	# uncoloredNodes:[[nodeID,occurrence,color],[],[],...], it is ranked by reverse occurrence
	# nodesArr:[[currentNodeID, node 1, node 2..]]node 1, node 2 and etc. are connected with currentNode
	# neighborsTobeColored:[nodeID1, nodeID2, nodeID3, ...] neighbor nodes of the high degree node

	while not neighborsTobeColored: # if empty, neighborsTobeColored set should be refilled
		tempNeighbors = nodesArr[orderedNodes[counter[0]][0]]
		del tempNeighbors[0]
		for element in tempNeighbors:
			if nodes[element] in uncoloredNodes:
				neighborsTobeColored.append(nodes[element])
		neighborsTobeColored.sort(reverse=True,key=getOccurrence)
		counter[0] = counter[0]+1
	# if len(coloredNodes) ==0:
	# 	chosenNode = rankedNodes[0]
	# 	del rankedNodes[0]

	chosenNode = neighborsTobeColored[0]
	uncoloredNodes.remove(chosenNode)
	del neighborsTobeColored[0]

	return chosenNode


def findCompleteGraph(node, completeGraph, nodeNeighbors):
	nodeNeighbors = list(nodeNeighbors)
	if len(completeGraph) == 0:
		completeGraph.append(node[0])

	else:
		del nodeNeighbors[0]   # remove current node from nodeNeighbors to get true neighbors of node
		if set(completeGraph) <= set(nodeNeighbors):
			completeGraph.append(node[0])

	return completeGraph

def getRankedNodes(nodes):
   #  #the sequence that nodes are colored have to methods
   #  # a. rotate all kinds of sequence of nodes with same degree
   #  # b. whether neborhood nodes are colored
   #
   #  #nodes are sorted with occurance already
   #  #scheme a: rotate all kinds of sequence of nodes with same degree.
   #
   # # get array with number of nodes with same node degree
   #  sameDegreeNodesNumberArr = []
   #  tempSameDegreeNodeNumber = 1
   #  for i in range(len(nodes)):
   #      tempDegree = nodes[i][1]
   #      if(i+1) < len(nodes):
   #          if nodes[i+1][1] != tempDegree:
   #              sameDegreeNodesNumberArr.append(tempSameDegreeNodeNumber)
   #              tempSameDegreeNodeNumber = 1
   #          else:
   #              tempSameDegreeNodeNumber=tempSameDegreeNodeNumber+1
   #      if(i+1) == len(nodes):
   #          sameDegreeNodesNumberArr.append(tempSameDegreeNodeNumber)
   #
   #  sameDegreeNodesPossibilitiesArr = []
   #  for i in range(len(sameDegreeNodesNumberArr)):
   #      sameDegreeNodesPossibilitiesArr.append(math.factorial(sameDegreeNodesNumberArr[i]))
   #
   #  #get total number of iteration needed
   #  totalCombinationNum = 1
   #  for element in sameDegreeNodesPossibilitiesArr:
   #      totalCombinationNum = totalCombinationNum*element
   #
   #
   #  sameDegreeNodesNumberArr
	rankedNodes = [nodes]

	return rankedNodes

def solve_it(input_data):
	# Modify this code to run your optimization algorithm

	# parse the input
	# generate useful data structures
	lines = input_data.split('\n')
	first_line = lines[0].split()
	node_count = int(first_line[0])
	edge_count = int(first_line[1])
	#generate list of nodes
	nodes = [] #first element indicates node number, second element indicates number of occurrence, 3rd element indicates node color
	orderedNodes = [] # ordered nodes are nodes with occurrence ordered from high to low
	nodesArr = [] #nodesArr will store the connection of nodes to a certain node[[a, 1,2,3,4..], ... ] nodes 1,2,3,4 are connected with node a.
	coloredNodes = []
	for i in range(0,node_count):
		nodes.append([i,0,0]) #first element indicates node number, second element indicates number of occurrence, 3rd element indicates node color
		nodesArr.append([i])
	for i in range(1, edge_count + 1):
		line = lines[i]
		parts = line.split()
		nodes[int(parts[0])][1] = nodes[int(parts[0])][1] +1
		nodes[int(parts[1])][1] = nodes[int(parts[1])][1] + 1
		nodesArr[int(parts[0])].append(int(parts[1]))
		nodesArr[int(parts[1])].append(int(parts[0]))

	#sort nodes based on occurrence, larger occurrence appears in front
	orderedNodes = sorted(nodes, reverse=True, key=getOccurrence)
	uncoloredNodes = list(orderedNodes)
	# used to store number of colors
	tempColor = 0
	completeGraph = []

	#find complete graph
	for element in orderedNodes:
		completeGraph = findCompleteGraph(element, completeGraph, nodesArr[element[0]])
	#color complete graph
	for element in completeGraph:
		node = [element, tempColor]
		coloredNodes.append(node)
		tempColor = tempColor + 1
	#remove colored complete graph nodes from nodes
	orderedCompleteGraph = sorted(completeGraph, reverse=True ) #delete from large index to small index
	uncoloredNodes = sorted(uncoloredNodes, key = getID)
	for element in orderedCompleteGraph:
		del uncoloredNodes[element]

	#generate first set of nodes to be colored
	neighborsTobeColored = []
	tempNeighbors = list(nodesArr[completeGraph[0]]) # the set contains neighbors of high rank node, which is to be colored after coloring of high rank node
	del tempNeighbors[0]
	for element in tempNeighbors:
		if nodes[element] in uncoloredNodes:
			neighborsTobeColored.append(nodes[element])
	neighborsTobeColored = sorted(neighborsTobeColored,reverse=True,key=getOccurrence)

	maxColor = tempColor -1 #get current max color
	uncoloredNodes = sorted(uncoloredNodes, reverse=True, key=getOccurrence)
	node_count = node_count - len(completeGraph)
	counter = [1]
	for i in range(0, node_count):
		# chosenNode = (rankedNodes[k])[i]
		# get chosenNode
		chosenNode = getChosenNode_crt2(neighborsTobeColored, nodes, uncoloredNodes,nodesArr,counter, orderedNodes)
		tempColor = getSmallestAvailableColor(coloredNodes, nodesArr[chosenNode[0]])  # chosenNode[0] is node ID
		node = [chosenNode[0], tempColor] # chosenNode[0] is node color
		if tempColor > maxColor:
			maxColor = tempColor
		coloredNodes.append(node)
		# append maxColor for each rankedNodes
   # nodes = coloredNodes[minMaxColorIndex]
	numberOfColors = maxColor + 1
	resultNodes = sorted(coloredNodes, key=getID)
	solution = []
	for node in resultNodes:
		solution.append(int(node[1]))

	# prepare the solution in the specified output format
	#
	output_data = str(numberOfColors) + ' ' + str(0) + '\n'
	output_data += ' '.join(map(str, solution))

	return output_data


import sys

if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
	#following line is for testing only
	#for gc_50_3, the best result should be or better than 6
	#for gc_70_7, result should be better than 20
	#file_location = 'C:/Users/Richie/Desktop/Optimization/discrete optimization/3coloring/data/gc_50_3'
		with open(file_location, 'r') as input_data_file:
			input_data = input_data_file.read()
			print(solve_it(input_data))
	else:
		print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

