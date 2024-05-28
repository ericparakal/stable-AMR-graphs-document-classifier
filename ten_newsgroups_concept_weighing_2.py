import copy
import pickle
import shutil
import networkx as nx

classes = ['graphics', 'food', 'medical', 'space', 'sport', 'technologie', 'business', 'politics', 'entertainment',
           'historical']
graph_prefix = 'ten_newsgroups_graphs/'


def penalty_calculation(concept, graph_list):
    concept_penalty_1 = 1

    for graph in graph_list:

        non_subsumption = 0

        for i in range(concept['num_subgraphs']):
            intersection = [e for e in concept[f'subgraph_{i}'].edges(data=True) if e in graph.edges(data=True)]

            if intersection != list(concept[f'subgraph_{i}'].edges(data=True)):
                non_subsumption = 1
                break

        if non_subsumption == 0 and concept['num_subgraphs'] != 0:
            # concept_penalty_1 += concept['num_subgraphs']
            concept_penalty_1 += 1

    return concept_penalty_1


def concept_weighing():
    global classes, graph_prefix

    final_concepts = []

    for class_name in classes:
        graph_list = []

        for j in range(11, 101):

            graph_name = class_name + '_train_graph_' + str(j) + '.gml'
            file_path = graph_prefix + class_name + '/' + graph_name

            try:
                graph_list.append(nx.read_gml(file_path))
            except FileNotFoundError:
                print(f"Graph {graph_name} is absent for now.")

        # print('Break point.')

        class_negation = [n for n in classes if n != class_name]

        for negated_class in class_negation:

            concepts_file_name = graph_prefix + negated_class + '/' + negated_class + '_concepts.pickle'

            with open(concepts_file_name, 'rb') as f:
                concepts = pickle.load(f)

            for c_i, concept in enumerate(concepts):
                concept_id = negated_class + 'concept_' + str(c_i)
                concept_penalty_1 = penalty_calculation(concept, graph_list)

                relevant_index = [c_k for c_k, concept_ele in enumerate(final_concepts)
                                  if concept_ele['id'] == concept_id]

                if not relevant_index:

                    final_concept_ele = {}

                    for s in range(concept['num_subgraphs']):
                        final_concept_ele[f'subgraph_{s}'] = concept[f'subgraph_{s}']
                        final_concept_ele[f'subgraph_{s}_support'] = concept[f'subgraph_{s}_support']

                    final_concept_ele['id'] = concept_id
                    final_concept_ele['support'] = concept['support']
                    final_concept_ele['num_subgraphs'] = concept['num_subgraphs']
                    final_concept_ele['penalty_1'] = copy.deepcopy(concept_penalty_1)

                    final_concepts.append(final_concept_ele)

                else:
                    if len(relevant_index) == 1:
                        final_concepts[relevant_index[0]]['penalty_1'] += copy.deepcopy(concept_penalty_1)
                    else:
                        print("More than 1 relevant concept.")
                        return

            print(f"Concept {negated_class} finished for training object graphs of class {class_name} finished")

        print(f"Class {class_name} training object graphs finished")

    for class_name in classes:
        relevant_indices = [c_k for c_k, concept_ele in enumerate(final_concepts)
                            if class_name in concept_ele['id']]

        class_concepts = []

        for r_i in relevant_indices:
            class_concepts.append(final_concepts[r_i])

        concepts_file_name_2 = class_name + '_final_concepts.pickle'

        with open(concepts_file_name_2, 'wb') as handle:
            pickle.dump(class_concepts, handle, protocol=pickle.HIGHEST_PROTOCOL)

        concepts_path = graph_prefix + class_name + '/' + concepts_file_name_2

        shutil.move(concepts_file_name_2, concepts_path)


if __name__ == "__main__":
    concept_weighing()
