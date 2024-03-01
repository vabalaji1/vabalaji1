from node import Node

class Edge:
    def __init__(self, start:Node, end:Node,  color = None, ltail = None, lhead = None, weight = None):
        self.start = start
        self.end = end
        self.label = str(start.label) + str(end.label)
        self.color = color
        self.ltail = ltail
        self.lhead = lhead
        self.weight = weight

    def setColor(self, val):
        self.color = val
    
    def __str__(self):
        content = ""
        start = 0
        if self.color != None:
            if start == 0:
                content = content + f"color=\"{self.color}\""
                start+=1
            else:
                content = content + f",color=\"{self.color}\""
        if self.ltail !=None:
            if start == 0:
                content = content + f"ltail=\"{self.ltail}\""
                start+=1
            else:
                content = content + f",ltail=\"{self.ltail}\""
        if self.lhead !=None:
            if start == 0:
                content = content + f"lhead=\"{self.ltail}\""
                start+=1
            else:
                content = content + f",lhead=\"{self.ltail}\""
        if self.weight !=None:
            if start == 0:
                content = content + f"weight=\"{self.weight}\""
                start+=1
            else:
                content = content + f",weight=\"{self.weight}\""
        return f"{self.start.name}->{self.end.name} [{content}];"