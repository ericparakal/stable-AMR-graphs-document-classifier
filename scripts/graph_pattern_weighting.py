import base_functions as bf


def penalty_calculation(graph_pattern, graphs):
    graph_pattern_penalty_1 = 1
    graph_pattern_penalty_2 = 1
    graph_pattern_penalty_3 = 1
    graph_pattern_penalty_4 = 1

    for graph in graphs:
        multiple_subsumption = bf.multiple_subsumption_check(graph, graph_pattern['subgraphs'])

        if multiple_subsumption == 1:
            graph_pattern_penalty_1 += 1



