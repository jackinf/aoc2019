from dijkstar import Graph, find_path
graph = Graph()
graph.add_edge("AA", "BB", 110)
graph.add_edge("BB", "CC", 125)
graph.add_edge("CC", "ZZ", 108)
graph.add_edge("AA", "ZZ", 500)
path = find_path(graph, "AA", "ZZ")
print(path)