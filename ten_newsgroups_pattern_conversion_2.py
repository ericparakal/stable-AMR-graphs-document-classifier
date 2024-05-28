#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:13:56 2022

@author: eric
"""
import shutil
import json
import copy
import pickle
import networkx as nx


'''
def merge_graph_patterns(frequent_subgraphs_2):
    print(frequent_subgraphs_2)
'''


def frequent_frequent_subgraphs_builder(class_name):
    prefix = 'ten_newsgroups_graphs'
    
    frequent_subgraphs = []
    frequent_subgraph_ele = {}
    
    vertex_positions = {}

    graph_patterns_file_name = prefix + '/' + class_name + '/' + class_name + '_patterns.OUT'
    
    vertex_labels_file_name = prefix + '/' + class_name + '/' + class_name + '_vertex_labels.pickle'

    edge_labels_file_name = prefix + '/' + class_name + '/' + class_name + '_edge_labels.pickle'
    
    with open(vertex_labels_file_name, 'rb') as f:
        vertex_labels_fake = pickle.load(f)
        
    vertex_labels = {v: k for k, v in vertex_labels_fake.items()}

    with open(edge_labels_file_name, 'rb') as f:
        edge_labels_fake = pickle.load(f)

    edge_labels = {e: k for k, e in edge_labels_fake.items()}

    with open(graph_patterns_file_name) as f:
        lines = f.read().splitlines()
        
    g = nx.MultiDiGraph()

    id = 0
        
    for line in lines:
        words = line.split(" ")
        if words[0] == "#":
            frequent_subgraph_ele['support'] = copy.deepcopy(int(words[1]))
            
        if words[0] == "v":
            vertex_positions[int(words[1])] = copy.deepcopy(vertex_labels[int(words[2])])
            
        if words[0] == "e":
            g.add_edge(edge_labels[int(words[3])][0],
                       edge_labels[int(words[3])][1],
                       label=edge_labels[int(words[3])][2])
            
        if words[0] == "x":
            frequent_subgraph_ele['subgraph'] = copy.deepcopy(g)
            frequent_subgraph_ele['extent'] = words[1:]
            frequent_subgraph_ele['id'] = class_name + '_frequent_subgraph_' + str(id)

            if len(frequent_subgraph_ele['extent']) != frequent_subgraph_ele['support']:
                print("Sanity check 1 failed.")
                return

            frequent_subgraphs.append(copy.deepcopy(frequent_subgraph_ele))
            
            g = nx.MultiDiGraph()
            frequent_subgraph_ele = {}
            vertex_positions = {}

            id += 1

    frequent_subgraphs_file_name = class_name + '_frequent_subgraphs.pickle'

    with open(frequent_subgraphs_file_name, 'wb') as handle:
        pickle.dump(frequent_subgraphs, handle, protocol=pickle.HIGHEST_PROTOCOL)

    frequent_subgraphs_path = prefix + '/' + class_name + '/' + frequent_subgraphs_file_name

    shutil.move(frequent_subgraphs_file_name, frequent_subgraphs_path)

    return frequent_subgraphs


def subsumption_check(maximal_subgraph, subgraph):
    intersection = [e for e in subgraph.edges(data=True) if e in maximal_subgraph.edges(data=True)]

    if intersection == list(subgraph.edges(data=True)):
        subsumption = 1

    else:
        subsumption = 0

    return subsumption


def find_maximal_subgraph_index(indices, frequent_subgraphs):

    maximal_subgraph_node_count = 0
    maximal_subgraph_edge_count = 0
    maximal_subgraph_index = 0

    for i in indices:
        if len(frequent_subgraphs[i]['subgraph'].nodes) > maximal_subgraph_node_count:
            maximal_subgraph_node_count = len(frequent_subgraphs[i]['subgraph'].nodes)

            if len(frequent_subgraphs[i]['subgraph'].edges) > maximal_subgraph_edge_count:
                maximal_subgraph_edge_count = len(frequent_subgraphs[i]['subgraph'].edges)

            maximal_subgraph_index = i

        elif len(frequent_subgraphs[i]['subgraph'].nodes) == maximal_subgraph_node_count:
            subsumption = subsumption_check(frequent_subgraphs[maximal_subgraph_index]['subgraph'],
                                            frequent_subgraphs[i]['subgraph'])

            if subsumption == 0 and len(frequent_subgraphs[i]['subgraph'].edges) > maximal_subgraph_edge_count:
                maximal_subgraph_node_count = len(frequent_subgraphs[i]['subgraph'].nodes)
                maximal_subgraph_edge_count = len(frequent_subgraphs[i]['subgraph'].edges)
                maximal_subgraph_index = i

    return maximal_subgraph_index


def filter_frequent_subgraphs(indices, frequent_subgraphs):

    filtered_indices = []

    while len(indices) > 0:
        maximal_subgraph_index = find_maximal_subgraph_index(indices, frequent_subgraphs)
        filtered_indices.append(maximal_subgraph_index)

        indices.remove(maximal_subgraph_index)

        bad_indices = []

        for i in indices:
            subsumption = subsumption_check(frequent_subgraphs[maximal_subgraph_index]['subgraph'],
                                            frequent_subgraphs[i]['subgraph'])

            if subsumption:
                bad_indices.append(i)

        indices = [index for index in indices if index not in bad_indices]

    return filtered_indices


def graph_patterns_builder(class_name, frequent_subgraphs):
    prefix = 'ten_newsgroups_graphs'

    concepts = []
    concept_ele = {}

    lattice_file_name = prefix + '/' + class_name + '/' + class_name + '_lattice.json'

    with open(lattice_file_name) as f:
        lattice = json.load(f)

    for ext_index, ext in enumerate(lattice[1]['Nodes']):
        matching_indices = [f_index for f_index, frequent_subgraph_ele_2 in enumerate(frequent_subgraphs)
                            if set(ext['Ext']['Inds']).issubset(list(map(int, frequent_subgraph_ele_2['extent'])))]

        concept_ele['support'] = ext['Ext']['Count']

        m_count = 0

        filtered_indices = filter_frequent_subgraphs(matching_indices, frequent_subgraphs)

        for m in filtered_indices:
            concept_ele[f'subgraph_{m_count}'] = copy.deepcopy(frequent_subgraphs[m]['subgraph'])
            concept_ele[f'subgraph_{m_count}_support'] = copy.deepcopy(frequent_subgraphs[m]['support'])
            m_count += 1

        concept_ele['num_subgraphs'] = m_count
        concept_ele['id'] = class_name + '_concept_' + str(ext_index)
        concepts.append(copy.deepcopy(concept_ele))
        concept_ele = {}

    concepts_file_name = class_name + '_concepts.pickle'

    with open(concepts_file_name, 'wb') as handle:
        pickle.dump(concepts, handle, protocol=pickle.HIGHEST_PROTOCOL)

    concepts_path = prefix + '/' + class_name + '/' + concepts_file_name

    shutil.move(concepts_file_name, concepts_path)


if __name__ == "__main__":

    classes = ['business', 'graphics', 'food', 'medical', 'space',
               'sport', 'technologie', 'politics', 'entertainment', 'historical']

    for c in classes:
        frequent_subgraphs = frequent_frequent_subgraphs_builder(c)

        if frequent_subgraphs == 1:
            print("Something wrong.")

        else:
            graph_patterns_builder(c, frequent_subgraphs)
            print(f"{c} finished.")
