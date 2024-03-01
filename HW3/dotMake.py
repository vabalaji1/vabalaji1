import pandas as pd
from random import randint
import math
from node import Node
from edge import Edge
from cluster import Cluster

class DotMake:
    def __init__(self):
        self.nodes = dict()
        self.clusters = []
        self.clusterPair = dict()
        self.edges = dict()
        self.clusterCount = 1
        self.nodeCount = 0
    
    def addNode(self, val, color= None, shape = None, clusterName = None):
        if val in self.nodes:
            raise Exception("node already done")
        tmp = Node(val, self.nodeCount, color, shape)
        self.nodeCount+=1
        
        self.nodes[val] = tmp
        if clusterName !=None:
            try:
                position = self.clusters.index(clusterName)
                self.clusterPair[clusterName].addNodes(self.nodes[val])
            except ValueError:
                clusterC = "cluster" + str(self.clusterCount)
                self.clusterCount+=1
                newCluster = Cluster(clusterC, clusterName)
                newCluster.addNodes(self.nodes[val])
                self.clusters.append(clusterName)
                self.clusterPair[clusterName] = newCluster
        return tmp
    
    def addEdge(self, start:Node, end:Node,  color = None, ltail = None, lhead = None, weight = None):
        tmp = Edge(start,end,color,ltail,lhead, weight)
        if tmp.label in self.edges:
            raise Exception("edge already done")
        self.edges[tmp.label] = tmp
    
    def addCluster(self, name):
        if name in self.clusterPair:
            raise Exception("cluster already made")
        clusterC = "cluster" + str(self.clusterCount)
        self.clusterCount+=1
        newCluster = Cluster(clusterC, name)
        self.clusters.append(name)
        self.clusterPair[name] = newCluster


    
    def __str__(self):
        total = "digraph G {\ncompound=true;\nsize=\"150,150\";\nrankdir = \"LR\";\nranksep = 1.5;\n"


        nodesSeen = set()
        for indCluster in self.clusters:
            total = total + f"subgraph {self.clusterPair[indCluster].label} {{\nlabel=\"{self.clusterPair[indCluster].name}\";\n"
            for indNode in self.clusterPair[indCluster].nodes:
                
                total = total + str(indNode) + '\n'
                nodesSeen.add(indNode.label)
            total = total + '}\n'
        for indNode in self.nodes:
            if indNode in nodesSeen:
                continue
            total = total + str(self.nodes[indNode]) + '\n'
        for indEdge in self.edges:
            total = total + str(self.edges[indEdge]) + '\n'
        total = total + '}'
        return total
    



    
# #generate the graph
# def generateGraph(nodes, linking):
#     graph = dict()
#     for i in range(nodes):
#         graph[i] = []
#     for i in range(nodes):
#         for j in range(nodes):
#             if i == j:
#                 continue
#             prob = randint(1,int(linking.as_integer_ratio()[1]))
#             if(prob <= int(linking.as_integer_ratio()[0])):
#                 graph[i].append(j)
#     return graph

# # smallGraph = generateGraph(20,.1)
# # totalDegree = 0
# # graph = DotMake()
# # gvComp = dict()
# # even = graph.addCluster("Even")
# # odd = graph.addCluster("Odd")
# # for startN in smallGraph:
# #     if startN not in gvComp:
# #         if startN%2 == 0:
# #             gvComp[startN] = graph.addNode(val = "<f0> 0xf7fc4380| <f1> | <f2> |-1" + str(startN), clusterName="Even", shape = "record")
# #         else:
# #             gvComp[startN] = graph.addNode(val = str(startN), clusterName="Odd")
# #     for endN in smallGraph[startN]:
# #         if endN %2 == startN %2:
# #             continue
# #         if endN not in gvComp:
# #             if endN %2 == 0:
# #                 gvComp[endN] = graph.addNode(val = str(endN), clusterName="Even", shape = "record")
# #             else:
# #                 gvComp[endN] = graph.addNode(val = str(endN), clusterName="Odd")
# #         try:
# #             graph.addEdge(start = gvComp[startN],end = gvComp[endN])
# #         except:
# #             continue
# # print(graph)
            