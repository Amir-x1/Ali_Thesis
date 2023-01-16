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
    if d >= r0 + r1:
        return None, None
    # One circle within other
    if d <= abs(r0 - r1):
        return None, None
    # coincident circles
    if d == 0 and r0 == r1:
        return None, None
    else:
        try:
            a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
            h = math.sqrt(r0 ** 2 - a ** 2)
            x2 = x0 + a * (x1 - x0) / d
            y2 = y0 + a * (y1 - y0) / d
            x3 = x2 + h * (y1 - y0) / d
            y3 = y2 - h * (x1 - x0) / d

            x4 = x2 - h * (y1 - y0) / d
            y4 = y2 + h * (x1 - x0) / d

            return [x3, y3], [x4, y4]
        except Exception:
            return None, None


def position_calculator(first_node, r0, second_node, r1, sink, rs, error):
    e = error * random.randint(-100, 100) / 100
    e = e + 1
    a, b = intersecting_points_of_two_circle(first_node, r0, sink, rs)
    c, d = intersecting_points_of_two_circle(second_node, r1, sink, rs)
    if a is None or b is None:
        print("None: Changing circles")
        a, b = intersecting_points_of_two_circle(first_node, r0, second_node, r1)
    if c is None or d is None:
        print("None: Changing circles")
        c, d = intersecting_points_of_two_circle(second_node, r1, first_node, r0)
    if a is None or b is None or c is None or d is None:
        return None
    if abs(a[0] - c[0]) < 0.0001 and abs(a[1] - c[1]) < 0.0001:
        if a is None or c is None:
            print("None")
        a[0] *= e
        a[1] *= e
        return a
    elif abs(a[0] - d[0]) < 0.0001 and abs(a[1] - d[1]) < 0.0001:
        if a is None or d is None:
            print("None")
        a[0] *= e
        a[1] *= e
        return a
    elif abs(b[0] - c[0]) < 0.0001 and abs(b[1] - c[1]) < 0.0001:
        if c is None or b is None:
            print("None")
        b[0] *= e
        b[1] *= e
        return b
    elif abs(b[0] - d[0]) < 0.0001 and abs(b[1] - d[1]) < 0.0001:
        if d is None or b is None:
            print("None")
        b[0] *= e
        b[1] *= e
        return b
    else:
        print("None: No interaction point found")
        return None
