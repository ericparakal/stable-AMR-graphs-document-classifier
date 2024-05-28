import copy
import pickle
import shutil
import networkx as nx

classes = ['graphics', 'food', 'medical', 'space', 'sport', 'technologie', 'business', 'politics', 'entertainment', 'historical']
graph_prefix = 'graph_archive_4/'

edge_penalties = {}


def penalty_calculation(concept, graph_list):
    global edge_penalties

    concept_penalty_1 = 1
    concept_penalty_2 = 1
    concept_penalty_3 = 1

    for graph in graph_list:

        intersection = [e for e in concept['graph_pattern'].edges(data=True) if e in graph.edges(data=True)]

        if intersection == list(concept['graph_pattern'].edges(data=True)):
            concept_penalty_1 += len(concept['graph_pattern'].nodes())
            concept_penalty_2 += 1/(len(graph.nodes()))
            concept_penalty_3 += 1/abs((sorted(graph.degree, key=lambda x: x[1], reverse=True)[0][1]) - (sorted(concept['graph_pattern'].degree, key=lambda x: x[1], reverse=True)[0][1]))

            for node1, node2, data in concept['graph_pattern'].edges(data=True):

                if (node1, node2, data['label']) in edge_penalties:
                    edge_penalties[(node1, node2, data['label'])] += 1

                else:
                    edge_penalties[(node1, node2, data['label'])] = 1

    return concept_penalty_1, concept_penalty_2, concept_penalty_3


def concept_weighing():
    global classes, graph_prefix, edge_penalties

    final_concepts = []

    for i in classes:
        graph_list = []

        for j in range(11, 101):

            graph_name = i + '_train_graph_' + str(j) + '.gml'
            file_path = graph_prefix + i + '/' + graph_name

            try:
                graph_list.append(nx.read_gml(file_path))
            except FileNotFoundError:
                print(f"Graph {graph_name} is absent for now.")

        # print('Break point.')

        class_negation = [n for n in classes if n != i]

        for k in class_negation:

            concepts_file_name = graph_prefix + k + '/' + k + '_concepts.pickle'

            with open(concepts_file_name, 'rb') as f:
                concepts = pickle.load(f)

            for c_i, concept in enumerate(concepts):
                concept_id = k + '_' + str(c_i + 1)
                concept_penalty_1, concept_penalty_2, concept_penalty_3 = penalty_calculation(concept, graph_list)

                relevant_index = [c_k for c_k, concept_ele in enumerate(final_concepts)
                                  if concept_ele['id'] == concept_id]

                if not relevant_index:
                    final_concepts.append({'id': concept_id, 'graph_pattern': concept['graph_pattern'], 'support': concept['support'],
                                           'penalty_1': copy.deepcopy(concept_penalty_1),
                                           'penalty_2': copy.deepcopy(concept_penalty_2),
                                           'penalty_3': copy.deepcopy(concept_penalty_3)})

                else:
                    if len(relevant_index) == 1:
                        final_concepts[relevant_index[0]]['penalty_1'] += copy.deepcopy(concept_penalty_1)
                        final_concepts[relevant_index[0]]['penalty_2'] += copy.deepcopy(concept_penalty_2)
                        final_concepts[relevant_index[0]]['penalty_3'] += copy.deepcopy(concept_penalty_3)
                    else:
                        print("More than 1 relevant concept.")
                        return

            print(f"Concept {k} finished for training object graphs of class {i} finished")

        print(f"Class {i} training object graphs finished")

    for c in classes:
        relevant_indices = [c_k for c_k, concept_ele in enumerate(final_concepts)
                            if c in concept_ele['id']]

        class_concepts = []

        for r_i in relevant_indices:
            class_concepts.append(final_concepts[r_i])

        concepts_file_name_2 = c + '_final_concepts_3.pickle'

        with open(concepts_file_name_2, 'wb') as handle:
            pickle.dump(class_concepts, handle, protocol=pickle.HIGHEST_PROTOCOL)

        concepts_path = graph_prefix + c + '/' + concepts_file_name_2

        shutil.move(concepts_file_name_2, concepts_path)

    edge_file_name = 'edge_penalties_2.pickle'

    with open(edge_file_name, 'wb') as handle:
        pickle.dump(edge_penalties, handle, protocol=pickle.HIGHEST_PROTOCOL)

    edge_path = graph_prefix

    shutil.move(edge_file_name, edge_path)


if __name__ == "__main__":
    concept_weighing()
