from functools import reduce


class Node:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

    def __str__(self):
        return f'[{self.value}] -> {self.parent}'


with open('input.txt', 'r') as f:
    lines = [x.strip().split(')') for x in f.readlines()]
    all_unique = set(reduce(list.__add__, lines))
    nodes_dict = {}
    for item in all_unique:
        nodes_dict[item] = Node(item, None)

    for parent_val, child_val in lines:
        parent = nodes_dict[parent_val]
        child = nodes_dict[child_val]
        child.parent = parent

    references = 0
    nodes = nodes_dict.values()

    for node in nodes_dict.values():
        parent = node.parent
        while parent is not None:
            references += 1
            parent = parent.parent

    print(references)

