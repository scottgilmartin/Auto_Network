#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 15:25:37 2019
@author: scottgilmartin
"""

import numpy
import networkx as nx
import matplotlib.pyplot as plt
import community
import random
from string import punctuation


def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)


with open('script.txt') as myfile:  # add your script file here

    w0 = myfile.read().split()
    w = []
    for u in w0:
        w.append(strip_punctuation(u))  # strip punctuation from the text

threshold = 5


# how many instances of a character name in caps has to appear before being considered. 
# If too low, might accidentally include scene directions etc.

def detect_chars():
    """
    Detect characters in the script by searching the uppercase words. May need to add some extra words to
    the 'all not in' part depending on the script.
    Here we exclude one part of a two-word character name 'KHAL DROGO' and 'THE' as an example.
    """
    caps = []
    for i in range(len(w)):
        if w[i].isupper() and len(w[i]) > 1 and all(
                ['KHAL' not in w[i], 'THE' not in w[i]]):  # extract the list of all uppercase words from script
            caps.append(w[i])

    chars = list(
        set([cap for cap in caps if caps.count(cap) > threshold and len(cap) > 1]))  # generate the character list
    return chars


def build_char_matrix(chars):
    """
    For each character in our generated list of characters we search the script for an instance of this character name,
    then we check for an instance of another character within a specified range of words. If we find such an instance then
    we add one to the character matrix element with row number equal to the position of the first character in the char list
    and column number equal to the position of the second.
    """
    mat = numpy.zeros((len(chars), len(chars)))  # build a matrix of size nxn for an n character list

    for n in range(len(chars)):  # for the nth character in the char list...

        for i in range(16, len(
                w) - 16):  # for the ith string in the script... starting at the 16th word to avoid out of range

            if chars[n].lower().capitalize() == w[i] or chars[n] == w[i]:  
                # if the current character is found in the string list as the ith string...

                for m in range(len(chars)):  # for each character in the char list...

                    for j in range(10, -16, -1):  # in the specified range...

                        if chars[m].lower().capitalize() == w[i - j] or chars[m] == w[
                                    i - j] and m != n:  
                            # if character m is found j words away from  character n = w[i]...

                            mat[n, m] += 1  # add one to the matrix position corresponding to (character n, character m)
    return mat


def filter(mat, chars, filter_threshold):
    """
    Filter out the false positives; i.e. the characters that connect less than a specified threshold number of times.
    """
    for n in range(len(chars)):
        for m in range(len(chars)):
            if mat[n, m] < filter_threshold:
                mat[n, m] = 0
    return mat


chars = detect_chars()
mat = filter(build_char_matrix(chars), chars, 2)

A = mat / 15  # make the network more readable
G = nx.from_numpy_matrix(A, parallel_edges=False)
pos = nx.spring_layout(G)

labels = {}
for l in range(len(chars)):
    labels[l] = str(chars[l])

edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_labels(G, pos, labels, font_size=8)
nx.draw_networkx_edges(G, pos, width=weights, edge_color=weights, edge_cmap=plt.cm.Blues)

color = ['#f97589', '#ffe3d3', '#89b2bc', '#fcca6f', '#513a2a', '#c2ebed', '#e8d0e3']  # custom node colors

r = lambda: random.randint(0, 255)
ran_hex_lst = ['#%02X%02X%02X' % (r(), r(), r()) for _ in
               range(len(chars))]  # randomly generated node colors, use for large char lists 

partition = community.best_partition(G, resolution=5.0)

count = 0
for com in set(partition.values()):
    count = count + 1  # counts the number of communities
    list_nodes = [nodes for nodes in partition.keys()
                  if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size=80,
                           node_color=color[count - 2])
plt.show()


# ----------------------------------------------------------------------------
# Some network analysis

# Define maximal_cliques()
def maximal_cliques(G, size):
    """
    Finds all maximal cliques in graph G that are of the specified size.
    """
    mcs = []
    for clique in nx.find_cliques(G):
        if len(clique) == size:
            mcs.append(clique)
    return mcs


print(len(maximal_cliques(G, 3)))

# [nx.shortest_path_length(G, i, j) for i,j in range(len(chars))] 
# #use this when you know whole graph is connected e.g. for a play or sitcom

bet_cen = nx.betweenness_centrality(G)


def highest_centrality(cent_dict):
    """
    Returns tuple with highest value from centrality dict.
    """
    # Create ordered tuple of centrality data
    cent_items = [(b, a) for (a, b) in cent_dict.items()]
    # Sort in descending order
    cent_items.sort()
    cent_items.reverse()
    return tuple(reversed(cent_items[0]))


print(chars[highest_centrality(bet_cen)[0]])

