import networkx as nx
from networkx.algorithms.community import louvain_communities
from networkx.algorithms.community.quality import modularity
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd


def get_network_dataframe(file_index):
    # Load the nodes and edges dataframes
    nodes_df = pd.read_csv(f"../movies/movies/networks/{file_index}_nodes.csv", on_bad_lines='skip')
    edges_df = pd.read_csv(f"../movies/movies/networks/{file_index}_edges.csv", on_bad_lines='skip')
    return nodes_df, edges_df

def create_graph_from_dataframes(nodes_df, edges_df):
    # Create graph
    G = nx.Graph()

    # Add nodes with 'label' attribute
    for _, row in nodes_df.iterrows():
        G.add_node(row['Id'], label=row['Label'])  # <- Match exact column name here

    # Add edges (with or without weights)
    if 'Weight' in edges_df.columns:
        G.add_weighted_edges_from(edges_df[['Source', 'Target', 'Weight']].values)
    else:
        G.add_edges_from(edges_df[['Source', 'Target']].values)
    return G

def compute_louvain_communities(G, edges_df):
    # Run Louvain algorithm
    communities = louvain_communities(G, seed=42, weight='Weight' if 'Weight' in edges_df.columns else None)

    # Compute modularity
    mod_score = modularity(G, communities, weight='Weight' if 'Weight' in edges_df.columns else None)
    print(f"Modularity using Louvain algorithm from NetworkX: {mod_score:.4f}")

    community_data = {
        "n_communities": len(communities),
        "modularity_score": mod_score,
        "community_list": [{"Community": i, "Nodes": sorted(community)} for i, community in enumerate(communities)] 
    }
    return communities, community_data

def compute_pagerank(G, edges_df):
    pagerank_scores = nx.pagerank(G, weight='Weight' if 'Weight' in edges_df.columns else None)
    return pagerank_scores


def visualize_communities(G, communities, title):        
    pos = nx.spring_layout(G, seed=42)
    colors = cm.rainbow(np.linspace(0, 1, len(communities)))

    for color, community in zip(colors, communities):
        nx.draw_networkx_nodes(G, pos, nodelist=community,
                            node_color=[color], node_size=80)

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.title(f"{title} - Louvain Communities")
    plt.axis("off")
    plt.show()
    

def visualize_communities_pgrank(G, communities, title, pagerank_scores=None, with_labels=True):
    labels = {node: G.nodes[node].get('label', str(node)) for node in G.nodes()}
    pos = nx.spring_layout(G, seed=42)
    colors = cm.rainbow(np.linspace(0, 1, len(communities)))

    # Map each node to its community ID
    node_community_map = {node: i for i, comm in enumerate(communities) for node in comm}
    
    # Compute node sizes based on PageRank or default
    if pagerank_scores:
        node_sizes = [5000 * pagerank_scores[node] for node in G.nodes()]
    else:
        node_sizes = [400 for _ in G.nodes()]

    # Get color per node based on community ID
    node_colors = [colors[node_community_map[node]] for node in G.nodes()]

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(),
                           node_color=node_colors,
                           node_size=node_sizes, alpha=0.9)

    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.4)

    # Optionally add labels
    if with_labels:
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    # Final plot settings
    plt.title(f"{title} - Louvain Communities")
    plt.axis("off")
    plt.show()
    