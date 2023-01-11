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


def intersecting_points_of_two_circle(first_node, r0, second_node, r1):
    x0 = first_node[0]
    y0 = first_node[1]
    x1 = second_node[0]
    y1 = second_node[1]
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1
    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        return [x3, y3], [x4, y4]


def position_calculator(first_node, r0, second_node, r1, sink, rs, error):
    a, b = intersecting_points_of_two_circle(first_node, r0, second_node, r1)
    c, d = intersecting_points_of_two_circle(first_node, r0, sink, rs)

    # print(a)
    # print(b)
    # print(c)
    # print(d)
    if a[0] == c[0] and a[1] == c[1]:
        print('a1')
        return a
    elif a[0] == d[0] and a[1] == d[1]:
        print('a2')
        return a
    elif b[0] == c[0] and b[1] == c[1]:
        print('b1')
        return b
    elif b[0] == d[0] and b[1] == d[1]:
        print('b2')
        return b
