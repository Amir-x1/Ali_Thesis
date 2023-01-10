from MyFunctions import *
import json

# ################## User inputs

# Nodes generator ----> 1 = you have nodes   #  0 = you dont have nodes
NodesGeneratedBefore = 0
# Enter number of nodes
NodesCount = 100
# Enter X  and Y of study area
X = 100
Y = 100
# Enter the position of Sink node
SinkX = 50
SinkY = 50
# Enter the position of first known node
FnodeX = 54
FnodeY = 54
# Enter the position of second known node
SnodeX = 46
SnodeY = 46
# ################################ Main ##################################
file_name = '%i Nodes for (%i)in(%i) Area.json' % (NodesCount, X, Y)
if not NodesGeneratedBefore:
    Nodes = {
        0: {"x": SinkX, "y": SinkY},
        1: {"x": FnodeX, "y": FnodeY},
        2: {"x": SnodeX, "y": SnodeY}
    }
    for i in range(3, NodesCount + 1):
        newNode = {i: node_generator(X, Y)}
        Nodes = {**Nodes, **newNode}
    json_file = json.dumps(Nodes, indent=2)
    with open(file_name, 'w') as f:
        f.write(json_file)

# print(Nodes)
