from node import Node

class Cluster:
    def __init__(self, label, name):
        self.label = label
        self.name = name
        self.nodes = []
        
    def addNodes(self, node:Node):
        self.nodes.append(node)
    