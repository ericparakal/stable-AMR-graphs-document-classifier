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

prefix = 'ten_newsgroups_graphs/'
classes = ['business', 'entertainment', 'food', 'graphics', 'historical', 'medical', 'politics', 'space', 'sport', 'technologie']


def classification_score(t_c):
    global prefix, classes

    column = []
    
    for i in classes:
        for j in range(1, 11):
            
            test_file_name = prefix + i + '/' + i + '_test_graph_' + str(j) + '.gml'
            test_graph = nx.read_gml(test_file_name)
            
            score = 0
            concept_counter = 0
            
            for k in range(len(t_c)):
                concept_counter += 1

                subsumption_counter = 0

                subgraph_weight = 0

                for s in range(t_c[k]['num_subgraphs']):
                    subgraph_weight += (len(t_c[k][f'subgraph_{s}'].nodes) * t_c[k][f'subgraph_{s}_support'])
                    # subgraph_weight += len(t_c[k][f'subgraph_{s}'].nodes)
                    intersection = [e for e in t_c[k][f'subgraph_{s}'].edges(data=True) if e in test_graph.edges(data=True)]

                    if intersection == list(t_c[k][f'subgraph_{s}'].edges(data=True)):
                        subsumption_counter += 1

                if subsumption_counter >= (t_c[k]['num_subgraphs']):
                    score += ((subgraph_weight) / t_c[k]['penalty_1'])

            column.append(score/concept_counter)
    return column


def classification():
    global prefix, classes

    d = {}

    index_list = []

    for i in classes:
        train_file_name = prefix + i + '/' + i + '_final_concepts.pickle'

        with open(train_file_name, 'rb') as f:
            train_concepts = pickle.load(f)

        d[i] = classification_score(train_concepts)

    # print("Break point.")

    for j in classes:
        for k in range(1, 11):
            index_list.append(j + '_test_graph_' + str(k))

    classification_df = pd.DataFrame(data=d, index=index_list)

    # print(classification_df)

    maxValueIndex = classification_df.idxmax(axis=1)

    y_true = []
    y_pred = list(maxValueIndex.values)

    for c in classes:
        for r in range(0, 10):
            y_true.append(c)
        print(f"{c} finished")

    cr = classification_report(y_true, y_pred, target_names=classes, output_dict=True)

    print(cr)


if __name__ == "__main__":
    classification()
