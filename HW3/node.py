class Node:
    def __init__(self, val, count, color = None, shape = None):
        self.label = val
        self.color = color
        self.shape = shape
        self.name = "node" + str(count)

    def setColor(self, val):
        self.color = val

    def setShape(self, val):
        self.shape = val
    
    def __str__(self):
        strLabel = f"label=\"{self.label}\""
        strColor = ""
        strShape = ""
        if self.color != None:
            strColor = f",color=\"{self.color}\",style=\"filled\""
        if self.shape !=None:
            strShape = f",shape=\"{self.shape}\""
        return self.name + " [" + strLabel + strColor + strShape + "];"

    
    