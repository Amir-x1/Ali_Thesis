from MyFunctions import *
from pathlib import Path
import json
import matplotlib.pyplot as plt

# ################## User inputs
# number of nodes
NodesCount = 500
# Maximum signal range in meters
MaxSignalDistance = 25
# Distance calculation error
error = 0.000
# X  and Y of study area in meters
X = 100
Y = 100
# the position of Sink node
SinkX = 50
SinkY = 41
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
Sink = [SinkX, SinkY]
if not NodesGeneratedBefore:
    Nodes = {
        0: {"x": SinkX, "y": SinkY},
        1: {"x": FnodeX, "y": FnodeY},
        2: {"x": SnodeX, "y": SnodeY}
    }
    for i in range(3, NodesCount + 1):
        newNode = {i: node_generator(X, Y)}
        if newNode == Sink:
            print(newNode)
            newNode = {i: node_generator(X, Y)}
            print(newNode)
        Nodes = {**Nodes, **newNode}
    json_file = json.dumps(Nodes, indent=2)
    with open(file_name, 'w') as f:
        f.write(json_file)
    with open(file_name, 'r') as h:
        Nodes = json.loads(h.read())
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
for i in Nodes:
    node = [Nodes[i]['x'], Nodes[i]['y']]
    distanceToSink.append(distance(Sink, node, error))
# print(distanceToSink)
# ###########################################################
# Start sending signals
calculatedLocations = []
for i in range(NodesCount + 1):
    calculatedLocations.append([0, 0])
anchors = []
for i in range(NodesCount + 1):
    anchors.append([0, 0])
allInOneStraightLine = []
for i in range(NodesCount + 1):
    allInOneStraightLine.append(0)
knownNodes = []
for i in range(NodesCount + 1):
    knownNodes.append(0)
knownNodes[0] = 1
knownNodes[1] = 1
knownNodes[2] = 1
# print(len(knownNodes))
# print(len(Nodes))
# print((knownNodes))
nn = 0
while sum(knownNodes) <= NodesCount:
    # Update anchor - find an unknown node and search for a signal that it can receive
    for i in Nodes:
        if knownNodes[int(i)] == 0:
            # print(i)
            firstNode = [Nodes[i]['x'], Nodes[i]['y']]
            for j in Nodes:
                if knownNodes[int(j)] == 1 and anchors[int(i)][0] != int(j):
                    secondNode = [Nodes[j]['x'], Nodes[j]['y']]
                    r = receiver(firstNode, secondNode, MaxSignalDistance, error)
                    if r and anchors[int(i)][0] == 0:
                        anchors[int(i)][0] = int(j)
                        # print(joints[int(i)][0])
                    elif r and anchors[int(i)][1] == 0:
                        anchors[int(i)][1] = int(j)
                        # print(joints[int(i)][0])
                        # print('2 break')
                        # break
                    elif r and anchors[int(i)][1] < 0:
                        # print(joints[int(i)][1])
                        anchors[int(i)][1] += 1

    # calculate position for nodes which have received two signals
    for i in Nodes:
        if knownNodes[int(i)] == 0 and anchors[int(i)][0] != 0 and anchors[int(i)][1] > 0:
            # print('node ' + i)
            knownNodes[int(i)] = 1
            thisNode = [Nodes[i]['x'], Nodes[i]['y']]
            fN = [Nodes[str(anchors[int(i)][0])]['x'], Nodes[str(anchors[int(i)][0])]['y']]
            sN = [Nodes[str(anchors[int(i)][1])]['x'], Nodes[str(anchors[int(i)][1])]['y']]
            radius1 = distance(fN, thisNode, error)
            radius2 = distance(sN, thisNode, error)
            radiusSink = distance(Sink, thisNode, error)
            calculatedLocations[int(i)] = position_calculator(fN, radius1, sN, radius2, Sink, radiusSink, error)
            # if the node and its two joint nodes are in a straight line function returns None
            if calculatedLocations[int(i)] is None:
                # print(calculatedPositions[int(i)])
                # print(joints[int(i)])
                print('again ' + i)
                knownNodes[int(i)] = 0
                allInOneStraightLine[int(i)] -= 1
                calculatedLocations[int(i)] = [0, 0]
                anchors[int(i)][1] = allInOneStraightLine[int(i)]
                print(calculatedLocations[int(i)])
                # print(joints[int(i)][1])
    nn += 1
    print('Iteration: ' + str(nn))
    if nn > 100:
        break
    # print(i)
    # print(knownNodes)
# ###################################################################################
# print(calculatedLocation)
# print(joints)
# print(knownNodes)
print(str(sum(knownNodes)-1) + " Nodes has been Found!")
print(calculatedLocations[190])

ActualLocations = []
for i in range(NodesCount + 1):
    ActualLocations.append([0, 0])
for i in Nodes:
    ActualLocations[int(i)][0] = Nodes[i]['x']
    ActualLocations[int(i)][1] = Nodes[i]['y']


# x-axis values
xx = []
yy = []
xxA = []
yyA = []
for i in range(3, len(calculatedLocations)):
    xx.append(calculatedLocations[i][0])
    yy.append(calculatedLocations[i][1])
    xxA.append(ActualLocations[i][0])
    yyA.append(ActualLocations[i][1])


# plotting points as a scatter plot
plt.scatter(xxA, yyA, label="Actual Locations", color="black", marker=".", s=30)
plt.scatter(xx, yy, label="Nodes", color="green", marker=".", s=30)
plt.scatter(SinkX, SinkY, label="Sink", color="red", marker="*", s=50)
plt.scatter(FnodeX, FnodeY, label="First known node", color="blue", marker=".", s=30)
plt.scatter(SnodeX, SnodeY, label="Second known node", color="red", marker=".", s=30)


# x-axis label
plt.xlabel('x - axis')
# frequency label
plt.ylabel('y - axis')
# plot title
plt.title('All Nodes')
# showing legend
# plt.legend()
plt.grid()
# function to show the plot
plt.show()

totalError = 0

for i in range(len(ActualLocations)):
    if ActualLocations[i][0] - calculatedLocations[i][0] == ActualLocations[i][0]:
        pass
    else:
        xError = ActualLocations[i][0] - calculatedLocations[i][0]
        yError = ActualLocations[i][1] - calculatedLocations[i][1]
        totalError += math.sqrt(xError**2 + yError**2)
print("Total Error is: " + str(totalError))
