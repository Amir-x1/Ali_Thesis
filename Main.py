from MyFunctions import *
from pathlib import Path
import json

# ################## User inputs
# number of nodes
NodesCount = 100
# Maximum signal range in meters
MaxSignalDistance = 15
# Distance calculation error
error = 0.01
# X  and Y of study area in meters
X = 100
Y = 100
# the position of Sink node
SinkX = 50
SinkY = 50
# position of first known node
FnodeX = 54
FnodeY = 54
# position of second known node
SnodeX = 46
SnodeY = 46
# ################################ Main ##################################
# ########## This part generates nodes and save them in a json file
# check if the file generated before
file_name = '%i Nodes for (%i)in(%i) Area.json' % (NodesCount, X, Y)
my_file = Path(file_name)
NodesGeneratedBefore = my_file.exists()
# ##########
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
else:
    with open(file_name, 'r') as h:
        Nodes = json.loads(h.read())
        # for node in Nodes:
        # node = int(node)
        # print(Nodes[node]['x'])
# print(Nodes)
# #########################################################################
# Calculate distance of each node to sink
distanceToSink = []
Sink = [SinkX, SinkY]
for i in Nodes:
    node = [Nodes[i]['x'], Nodes[i]['y']]
    distanceToSink.append(distance(Sink, node, error))
# print(distanceToSink)
# ###########################################################
# Start sending signals
calculatedPositions = []
for i in range(NodesCount + 1):
    calculatedPositions.append([0, 0])
joints = []
for i in range(NodesCount + 1):
    joints.append([0, 0])
knownNodes = []
for i in range(NodesCount + 1):
    knownNodes.append(0)
knownNodes[0] = 1
knownNodes[1] = 1
knownNodes[2] = 1
# print(len(knownNodes))
# print(len(Nodes))
# print((knownNodes))
for i in Nodes:
    if knownNodes[int(i)] == 0:
        firstNode = [Nodes[i]['x'], Nodes[i]['y']]
        for j in Nodes:
            if knownNodes[int(j)] == 1:
                secondNode = [Nodes[j]['x'], Nodes[j]['y']]
                r = receiver(firstNode, secondNode, MaxSignalDistance, error)
                if r and joints[int(i)][0] == 0:
                    joints[int(i)][0] = int(j)
                elif r and joints[int(i)][1] == 0:
                    joints[int(i)][1] = int(j)
for i in Nodes:
    if joints[int(i)][0] != 0 and joints[int(i)][1] != 0:
        knownNodes[int(i)] = 1
        fN = [Nodes[str(joints[int(i)][0])]['x'], Nodes[str(joints[int(i)][0])]['y']]
        sN = [Nodes[str(joints[int(i)][1])]['x'], Nodes[str(joints[int(i)][1])]['y']]
        # print(str(joints[int(i)][1]))
        # print(joints[int(i)])
        # print(fN)
        # print(sN)
        # print(Sink)
        calculatedPositions[int(i)] = position_calculator(fN, sN, Sink, error)

# print(joints)
# print(knownNodes)
