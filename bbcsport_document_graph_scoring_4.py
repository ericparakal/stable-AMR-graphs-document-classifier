#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:41:25 2022

@author: eric
"""

import pickle
import pandas as pd
import networkx as nx

from sklearn.metrics import classification_report

prefix = '/home/eric/Eric/PhD/ResearchCode/Formal Concept Analysis/bbcsport_graph_archive/'
classes = ['athletics', 'cricket', 'football', 'rugby', 'tennis']

test_indices = [[0, 9],
                [0, 12],
                [0, 26],
                [0, 14],
                [0, 9]]


def classification_score(t_c):
    global prefix, classes, test_indices

    column = []

    for i_index, i in enumerate(classes):
        for j in range(test_indices[i_index][0], test_indices[i_index][1] + 1):

            test_file_name = prefix + i + '/' + i + '_test_graph_' + str(j) + '.gml'
            test_graph = nx.read_gml(test_file_name)

            score = 0
            concept_counter = 0

            for k in range(len(t_c)):
                concept_counter += 1

                intersection = [e for e in t_c[k]['graph_pattern'].edges(data=True) if e in test_graph.edges(data=True)]

                if intersection == list(t_c[k]['graph_pattern'].edges(data=True)):
                    score += ((t_c[k]['support']) / t_c[k]['penalty_1'])

            column.append(score / concept_counter)
    return column


def classification():
    global prefix, classes

    d = {}

    index_list = []

    for i in classes:
        train_file_name = prefix + i + '/' + i + '_final_concepts_2.pickle'

        with open(train_file_name, 'rb') as f:
            train_concepts = pickle.load(f)

        d[i] = classification_score(train_concepts)

    # print("Break point.")

    for j_index, j in enumerate(classes):
        for k in range(test_indices[j_index][0], test_indices[j_index][1] + 1):
            index_list.append(j + '_test_graph_' + str(k))

    classification_df = pd.DataFrame(data=d, index=index_list)

    # print(classification_df)

    maxValueIndex = classification_df.idxmax(axis=1)

    y_true = []
    y_pred = list(maxValueIndex.values)

    for c_index, c in enumerate(classes):
        for r in range(test_indices[c_index][0], test_indices[c_index][1] + 1):
            y_true.append(c)
        print(f"{c} finished")

    cr = classification_report(y_true, y_pred, target_names=classes)

    print(cr)


if __name__ == "__main__":
    classification()
