import random
import math


def node_generator(x, y):
    x = random.randint(0, x)
    y = random.randint(0, y)
    return {"x": x, "y": y}


def distance(first_node, second_node, error):
    e = error * random.randint(-100, 100) / 100
    e = e + 1
    d = e * math.sqrt((first_node[0] - second_node[0]) ** 2 + (first_node[1] - second_node[1]) ** 2)
    return d


def receiver(first_node, second_node, max_signal_distance, error):
    d = distance(first_node, second_node, error)
    if d <= max_signal_distance:
        return d
    else:
        return 0


def position_calculator(first_node, second_node, sink, error):
    x1 = first_node[0]
    y1 = first_node[1]
    x2 = second_node[0]
    y2 = second_node[1]
    x3 = sink[0]
    y3 = sink[1]

    x12 = first_node[0] ** 2
    y12 = first_node[1] ** 2
    x22 = second_node[0] ** 2
    y22 = second_node[1] ** 2
    x32 = sink[0]**2
    y32 = sink[1]**2

    print(x1)
    print(x2)
    print(x3)
    print(y1)
    print(y2)
    print(y3)

    a = -(-x12*y2 + x12*y3 + x22*y1 - x22*y3 - x32*y1 + x32*y2 - y12*y2 + y12*y3 + y1*y22 - y1*y32 - y22*y3 + y32*y2) \
        / (2*x1*y2 - 2*x1*y3 - 2*x2*y1 - 2*x2*y3 - 2*x3*y1 - 2*x3*y2)
    b = -(x12*x2 - x12*x3 - x1*x22 + x1*x32 - x1*y22 + x1*y32 + x3*x22 - x32*x2 + y12*x2 - x2*y32 - y12*x3 + x3*y22)\
        / (2*x1*y2 - 2*x1*y3 - 2*x2*y1 + 2*x2*y3 + 2*x3*y1 - 2*x3*y2)
    return [a, b]
