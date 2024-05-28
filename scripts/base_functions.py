def subsumption_check(graph, subgraph):
    intersection = [e for e in subgraph.edges(data=True) if e in graph.edges(data=True)]

    if intersection == list(subgraph.edges(data=True)):
        subsumption = 1

    else:
        subsumption = 0

    return subsumption
