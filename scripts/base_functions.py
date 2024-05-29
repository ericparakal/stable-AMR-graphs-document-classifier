def singular_subsumption_check(graph, subgraph):
    intersection = [e for e in subgraph.edges(data=True) if e in graph.edges(data=True)]

    if intersection == list(subgraph.edges(data=True)):
        subsumption = 1

    else:
        subsumption = 0

    return subsumption


def multiple_subsumption_check(graph, subgraphs):
    for subgraph in subgraphs:
        singular_subsumption = singular_subsumption_check(graph, subgraph)

        if singular_subsumption == 0:
            multiple_subsumption = 0
            return multiple_subsumption

    multiple_subsumption = 1
    return multiple_subsumption
