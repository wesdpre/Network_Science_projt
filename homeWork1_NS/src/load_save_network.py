# The comments in this code were created with the help of the copilot, 
# and the code was created by me, but there was proposed code that changed my idea of ​​how to write the code.

import collections
import numpy as np
import os


def save_network(graph, filename=None, file_remove=False):
    if filename is None:
        raise ValueError("Filename cannot be None")
    
    if file_remove:
        if os.path.exists(filename):
            os.remove(filename) 
        else:
            print(f"File {filename} does not exist.")
    elif os.path.exists(filename):
        print(f"File {filename} already exists.")
        delete_file = input("Do you want to delete it? (y/n): ")
        if delete_file.lower() == 'y':
            os.remove(filename) 
    
    with open(filename, 'w') as f:
        for u, v in graph:
            f.write(f"{u} {v}\n")

def save_network_nx(graph, filename=None):
    if filename is None:
        raise ValueError("Filename cannot be None")
    
    if os.path.exists(filename):
        print(f"File {filename} already exists.")
        delete_file = input("Do you want to delete it? (y/n): ")
        if delete_file.lower() == 'y':
            os.remove(filename) 
            
        else : None
    
    with open(filename, 'w') as f:
        for u, v in graph.edges():
            f.write(f"{u} {v}\n")

def save_graph_network(graph, filename, directed_graph=False):
    """Saves the network in the format of edge list."""
    if filename is None:
        raise ValueError("Filename cannot be None")
    
    with open(filename, "w") as f:
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                if directed_graph:
                    f.write(f"{node} {neighbor}\n")
                elif node < neighbor:  # Avoid duplicate edges
                    f.write(f"{node} {neighbor}\n")

#load network file to the same structure 
def load_network_file(filename):
    """
    Reads the network from a file and returns an adjacency list.
    Each line in the file should contain two integers representing an edge.
    The first integer is the source node and the second integer is the target node.

    args:
        filename (str): The name of the file containing the network.
    returns:
        dict: A dictionary representing the adjacency list of the network.
            The keys are node indices and the values are sets of connected nodes.
    """
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    edges = []
    with open(filename, "r") as file:
        for line in file:
            u, v = map(int, line.split())
            edges.append((u,v))
    return edges

def load_network_line(line, edges):
    if not (line is None):
        raise FileNotFoundError(f"Line cannot be None")
    if not (edges is None):
        raise FileNotFoundError(f"Edges cannot be None")
    
    u, v = map(int, line.split())
    edges.append((u,v))
    return edges

#load network file to a different structure, using collections.defaultdict
def load_network_advanced(filename, undirected_graph=True):
    """
    Reads the network from a file and returns an adjacency list.
    Each line in the file should contain two integers representing an edge.
    The first integer is the source node and the second integer is the target node.

    args:
        filename (str): The name of the file containing the network.
    returns:
        dict: A dictionary representing the adjacency list of the network.
            The keys are node indices and the values are sets of connected nodes.
    """
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    
    graph = collections.defaultdict(set)
    
    with open(filename, "r") as file:
        for line in file:
            u, v = map(int, line.split())
            graph[u].add(v)
            if undirected_graph:
                graph[v].add(u)
                
    return graph