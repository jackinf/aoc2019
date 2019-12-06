from functools import reduce
from typing import List


class Node:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

    def __str__(self):
        return f'[{self.value}] -> {self.parent}'


def from_node_into_array(node: Node) -> List[str]:
    current = node.parent
    res = []
    while current is not None:
        res.append(current.value)
        current = current.parent
    return res


with open('input.txt', 'r') as f:
    lines = [x.strip().split(')') for x in f.readlines()]  # parse the input so that format is Array[Array[2]]
    all_unique = set(reduce(list.__add__, lines))  # reduce operation flattens the array; set filters out duplicates

    nodes_dict = {}
    for item in all_unique:
        nodes_dict[item] = Node(item, None)

    for parent_val, child_val in lines:
        parent = nodes_dict[parent_val]
        child = nodes_dict[child_val]
        child.parent = parent

    references = 0

    you_node = None
    san_node = None

    for node in nodes_dict.values():
        parent = node.parent

        if you_node is None and node.value == "YOU":
            you_node = node
        if san_node is None and node.value == "SAN":
            san_node = node

        while parent is not None:
            references += 1
            parent = parent.parent

    print(f'Part 1 answer: {references}')

    you_nodes = from_node_into_array(you_node)
    san_nodes = from_node_into_array(san_node)
    you_nodes_without_san_nodes = [value for value in you_nodes if value not in san_nodes]
    san_nodes_without_you_nodes = [value for value in san_nodes if value not in you_nodes]

    print(f'Part 2 answer: {str(len(you_nodes_without_san_nodes) + len(san_nodes_without_you_nodes))}')

