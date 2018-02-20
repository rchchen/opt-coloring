#!/usr/bin/python
# -*- coding: utf-8 -*-

# problems to think: 1. which node to color first 2.If multiple colors are available, say from 0,1,4,5 both 2,3 are free, which one to choose?
import math

def getOccurance(item):
    return item[1]

def getID(item):
    return item[0]
 
	#color shall be returned from this function
def getSmallestAvailableColor(coloredNodes, tempNode):
    #coloredNodes: [[nodeID,color],[],[]...]
    #tempNode, currentNode:[currentNodeID, node 1, node 2..] node 1, node 2 and etc. are connected with currentNode
    currentColors = []
    currentNode = list(tempNode)
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

#choose chosen node based on three criteria: a.is not colored;  b.has higher degree; c.is connected to an existing colored node;
def getChosenNode(rankedNodes,coloredNodes,nodesArr):
    #rankedNodes:[[nodeID,occurance,color],[],[],...]
    #coloredNodes: [[nodeID,color],[],[]...]
    #nodesArr:[[currentNodeID, node 1, node 2..]]node 1, node 2 and etc. are connected with currentNode
    if len(coloredNodes) ==0:
        chosenNode = rankedNodes[0]
        del rankedNodes[0]
    else:
        neighbors = []
        for element in coloredNodes:
            #find neighbors of all colored nodes including colored nodes
            neighbors = nodesArr[element[0]] + neighbors

        tempHighestDegree = rankedNodes[0][1] #degree of first ranked node
        chosenNode = rankedNodes[0]
        for element in rankedNodes:
            if element[1] < tempHighestDegree: #only select nodes with highest degree
                break
            if element[0] in neighbors:
                chosenNode = element
                break
        del rankedNodes[rankedNodes.index(chosenNode)]
    return chosenNode

def findCompleteGraph(node, completeGraph, nodeNeighbors):
    nodeNeighbors = list(nodeNeighbors)
    if len(completeGraph) == 0:
        completeGraph.append(node[0])

    else:
        del nodeNeighbors[0] #remove current node from nodeNeighbors to get true neighbors of node
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
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    #generate list of nodes
    nodes = [] #first element indicates node number, second element indicates number of occurance, 3rd element indicates node color
    nodesArr = [] #nodesArr will store the connection of nodes to a certain node[[a, 1,2,3,4..], ... ] nodes 1,2,3,4 are connected with node a.
    coloredNodes = []
    for i in range(0,node_count):
        nodes.append([i,0,0]) #first element indicates node number, second element indicates number of occurance, 3rd element indicates node color
        nodesArr.append([i])
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        nodes[int(parts[0])][1] = nodes[int(parts[0])][1] +1
        nodes[int(parts[1])][1] = nodes[int(parts[1])][1] + 1
        nodesArr[int(parts[0])].append(int(parts[1]))
        nodesArr[int(parts[1])].append(int(parts[0]))
    #sort nodes based on occurance, larger occruance appears in front
    nodes = sorted(nodes, reverse=True, key=getOccurance)

    # used to store number of colors
    maxColor = 0
    tempColor = 0
    completeGraph = []

    #find complete graph
    for element in nodes:
        completeGraph = findCompleteGraph(element, completeGraph, nodesArr[element[0]])
    #color complete graph)
    for element in completeGraph:
        node = [element, tempColor]
        coloredNodes.append(node)
        tempColor = tempColor + 1

    #remove colored nodes from nodes
    completeGraph = sorted(completeGraph, reverse=True )
    nodes = sorted(nodes, key = getID)
    for element in completeGraph:
        del nodes[element]

    maxColor = tempColor -1
    nodes = sorted(nodes, reverse=True, key=getOccurance)
    node_count = node_count - len(completeGraph)

    for i in range(0, node_count):
        # chosenNode = (rankedNodes[k])[i]
        # get chosenNode
        chosenNode = getChosenNode(nodes, coloredNodes, nodesArr)
        tempColor = getSmallestAvailableColor(coloredNodes, nodesArr[chosenNode[0]])  # chosenNode[0] is node ID
        node = [chosenNode[0], tempColor] # chosenNode[0] is node color
        if tempColor > maxColor:
            maxColor = tempColor
        coloredNodes.append(node)
        # append maxColor for each rankedNodes
   # nodes = coloredNodes[minMaxColorIndex]
    numberOfColors = maxColor + 1
    nodes = sorted(coloredNodes, key=getID)
    solution = []
    for node in nodes:
        solution.append(int(node[1]))

    # prepare the solution in the specified output format
    #
    output_data = str(numberOfColors) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    #if len(sys.argv) > 1:
        #file_location = sys.argv[1].strip()
    #following line is for testing only
    file_location = 'C:/Users/Richie/Desktop/Optimization/discrete optimization/3coloring/data/gc_50_3'
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
    #else:
         #print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

