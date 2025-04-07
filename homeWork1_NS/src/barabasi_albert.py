# The comments in this code were created with the help of the copilot, 
# and the code was created by me, but there was proposed code that changed my idea of ​​how to write the code.

import numpy as np
import random

def generate_barabasi_albert(n, m0=3, m=2, random_seed=None):
    """
    Generates a Barabási-Albert graph with n nodes.
    The graph starts with m0 fully connected nodes and grows by adding new nodes
    that connect to m existing nodes with a probability proportional to their degree.
    
    Parameters:
        n (int): Number of nodes in the graph.
        m0 (int): Initial number of nodes in the graph.
        m (int): Number of edges to attach from a new node to existing nodes.
    returns:
        graph (dict): A dictionary representing the graph where keys are node indices and values are sets of connected nodes.
    """
    if n < m0:
        raise ValueError("Number of nodes n must be greater than m0.")
    if m0 < 1 or m < 1:
        raise ValueError("m0 and m must be positive integers.")
    if m >= n:
        raise ValueError("m must be less than n.")
    # this start verifications was made by the copilot
    
    if not (random_seed is None):
        random.seed(random_seed)
    
    # Start with a fully connected network of m0 nodes
    # made by the copilot
    graph = {i: set(range(m0)) - {i} for i in range(m0)}
    
    # keep track of edge endpoints in one large array and select 
    # an element from this array at random
    edge_endpoints = list(range(m0)) * m  # Each initial node appears m times
    
    for node in range(m0, n):
        # Choose a neighor with probability proportional to its degree 
        node_neighbors = set(random.choices(edge_endpoints, k=m)) 
        # the probability of selecting any one vertex will be proportional to the number
        # of times it appears in the array – which corresponds to its degree
        
        # Add new node
        graph[node] = node_neighbors
        for neighbor in node_neighbors:
            graph[neighbor].add(node)
            edge_endpoints.append(neighbor)  # Add the neighbor to the edge endpoints list
        
        # Update the edge endpoints list with the new node
        edge_endpoints.extend([node] * m)
    
    print("edge endpoints = ",edge_endpoints)
    return graph