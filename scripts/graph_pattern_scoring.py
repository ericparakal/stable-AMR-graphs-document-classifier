import os
import re
import pickle
import pandas as pd
import networkx as nx
import base_functions as bf

from itertools import chain
from sklearn.metrics import classification_report


def flatten_chain(matrix):
    return list(chain.from_iterable(matrix))


def graph_pattern_scoring(weighted_class_graph_patterns, classes, prefix, penalty):

    column = []

    for class_name in classes:
        graph_data_prefix = prefix + '/' + class_name
        graph_file_names = [os.path.join(graph_data_prefix, graph_file_name) for graph_file_name in os.listdir(graph_data_prefix) if '_test_' in graph_file_name and graph_file_name.endswith('.gml')]
        graph_file_names.sort()

        graphs = [nx.read_gml(graph_file_name) for graph_file_name in graph_file_names]

        for graph in graphs:
            score = 0
            weighted_class_graph_pattern_counter = 0

            for weighted_class_graph_pattern in weighted_class_graph_patterns:
                weighted_class_graph_pattern_counter += 1

                multiple_subsumption = bf.multiple_subsumption_check(graph, weighted_class_graph_pattern['subgraphs'])

                if multiple_subsumption == 1:
                    weighted_class_graph_pattern_weight = bf.find_graph_pattern_weight(weighted_class_graph_pattern)
                    score += (weighted_class_graph_pattern_weight/weighted_class_graph_pattern['penalty_1'])

            column.append(score / weighted_class_graph_pattern_counter)
    return column


def graph_pattern_classification(classes, prefix, mode):
    d = {}
    index_list = []

    for class_name in classes:
        weighted_class_graph_patterns_file_name = prefix + '/' + class_name + '/' + class_name + '_weighted_' + mode + '.pickle'

        with open(weighted_class_graph_patterns_file_name, 'rb') as f:
            weighted_class_graph_patterns = pickle.load(f)

        d[class_name] = graph_pattern_scoring(weighted_class_graph_patterns, classes, prefix, mode)

    for class_name in classes:
        string_pattern = fr"{class_name}_test_graph_([0-9])*"

        graph_data_prefix = prefix + '/' + class_name
        graph_file_names = [os.path.join(graph_data_prefix, graph_file_name) for graph_file_name in os.listdir(graph_data_prefix) if '_test_' in graph_file_name and graph_file_name.endswith('.gml')]
        graph_file_names.sort()

        index_list.append([re.search(string_pattern, graph_file_name).group() for graph_file_name in graph_file_names])

    index_list_2 = flatten_chain(index_list)

    classification_df = pd.DataFrame(data=d, index=index_list_2)

    maxValueIndex = classification_df.idxmax(axis=1)

    y_true = []
    y_pred = list(maxValueIndex.values)

    for class_name in classes:
        graph_data_prefix = prefix + '/' + class_name
        graph_file_names = [os.path.join(graph_data_prefix, graph_file_name) for graph_file_name in os.listdir(graph_data_prefix) if '_test_' in graph_file_name and graph_file_name.endswith('.gml')]
        graph_file_names.sort()

        for j in range(len(graph_file_names)):
            y_true.append(class_name)

    cr = classification_report(y_true, y_pred, target_names=classes, output_dict=True)

    print(cr)
