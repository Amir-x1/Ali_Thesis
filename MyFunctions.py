import random


def node_generator(x, y):
    x = random.randint(0, x)
    y = random.randint(0, y)
    return {"x": x, "y": y}
