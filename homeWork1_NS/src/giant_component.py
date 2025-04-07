# The comments in this code were created with the help of the copilot, 
# and the code was created by me, but there was proposed code that changed my idea of ​​how to write the code.

import collections

# Two different architectures were implemented to obtain the size of the giant component, 
# i believe that the first implementation is the most correct.

# ---------------------------------------------------------------------------------------------------------------------------------
# normal giant_component_size function, using BFS as described in the slides

def bfs(start, graph, visited):
    """Performs BFS and returns the size of the connected component."""
    queue = collections.deque([start])
    visited.add(start)
    size = 0

    while queue:
        node = queue.popleft()
        size += 1
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return size

def giant_component_size(graph):
    """
        Computes the size of the largest connected component.
        
        args:
            graph (dict): A dictionary representing the adjacency list of the network.
                The keys are node indices and the values are sets of connected nodes.
        returns:
            int: The size of the largest connected component in the graph.
    """
    visited = set()
    max_size = 0

    for node in graph:
        if node not in visited:
            component_size = bfs(node, graph, visited)
            max_size = max(max_size, component_size)

    return max_size



# ---------------------------------------------------------------------------------------------------------------------------------
# try to build a more efficient function, taking use of the fact that we can remove nodes from the graph
# after visiting all connected nodes

def bfs_TryRemove(start, graph):
    """Performs BFS and returns the size of the connected component."""
    queue = collections.deque([start])
    connected_node_list = []
    connected_node_list.append(start)
    size = 0

    while queue:
        node = queue.popleft()
        size += 1
        for neighbor in graph[node]:
            connected_node_list.append(neighbor)
            queue.append(neighbor)

    return size , connected_node_list

def giant_component_size_TryRemove(graph):
    """
        Computes the size of the largest connected component.
        
        args:
            graph (dict): A dictionary representing the adjacency list of the network.
                The keys are node indices and the values are sets of connected nodes.
        returns:
            int: The size of the largest connected component in the graph.
    """
    
    new_graph = graph.copy()
    
    visited = set()
    max_giant_component_size = 0

    while new_graph:
        start_node = next(iter(new_graph))
        component_size, connected_node_list = bfs_TryRemove(start_node, new_graph)
        max_giant_component_size = max(max_giant_component_size, component_size)
        for connected_node in connected_node_list:
            new_graph.pop(connected_node, None)

    return max_giant_component_size
