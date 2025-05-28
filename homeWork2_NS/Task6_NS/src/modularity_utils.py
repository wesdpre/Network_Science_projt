from itertools import combinations
import matplotlib.pyplot as plt


def get_intra_community_modularity(G, comm):   
    total_weight_in_graph = G.size(weight='weight')
    def curr_combination_density(G, i, j, total_weight_in_graph):
        curr_comb_weight = G[i][j]['weight'] if G.has_edge(i,j) else 0 #Aij
        Ki = G.degree(i, weight='weight') 
        Kj = G.degree(j, weight='weight')
        curr_combination_density = ((curr_comb_weight * total_weight_in_graph) - Ki * Kj) / total_weight_in_graph
        return curr_combination_density
    community_mod = sum(curr_combination_density(G, u, v, total_weight_in_graph) for u, v in G.edges(comm) if u in comm and v in comm)
    community_mod = community_mod / total_weight_in_graph
    #print("Community modularity:", community_mod)
    return community_mod

def compute_modularity(G, communities):
    total_modularity = sum(get_intra_community_modularity(G, comm) for comm in communities)
    print(f"Local algorithm modularity: {total_modularity:.4f}")
    return total_modularity


def greedy_agglomerative(G):
    
    progress_mod_scores = []
    
    # Step 1: Initialize each node as its own community
    communities = [{node} for node in G.nodes()]
    
    # Track improvement
    improved = True
    
    while improved:
        best_increase = float('-inf')
        best_merge = None

        # Step 2: Try all community pairs
        for c1, c2 in combinations(communities, 2):
            merged = c1.union(c2)

            # Compute modularity for the merged community
            mod_merged = get_intra_community_modularity(G, merged)

            # Compute modularity of individual communities
            mod_c1 = get_intra_community_modularity(G, c1)
            mod_c2 = get_intra_community_modularity(G, c2)

            gain = mod_merged - (mod_c1 + mod_c2)

            if gain > best_increase:
                best_increase = gain
                best_merge = (c1, c2)

        # Step 3: Merge the best pair if improvement
        if best_merge and best_increase >= 0:
            print(f"Best merge found with increase: {best_increase:.4f}")
            c1, c2 = best_merge
            communities.remove(c1)
            communities.remove(c2)
            communities.append(c1.union(c2))
            
        else:
            improved = False  # No further improvement
        total_modularity = sum(get_intra_community_modularity(G, comm) for comm in communities)
        progress_mod_scores.append(total_modularity)
        print(f"New modularity after merge: {total_modularity:.4f}")
        print("Number of communities:", len(communities))
    print(f"Final number of communities: {len(communities)}")
    return communities, progress_mod_scores


def plot_progress(progress_scores):
    # Create iteration index
    iterations = list(range(len(progress_scores)))

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(iterations, progress_scores, color='blue', label='Values per iteration')

    # Add labels
    for i, val in enumerate(progress_scores):
        plt.text(i, val, f"{val:.3f}", fontsize=8, ha='right', va='bottom', rotation=45)
        
    plt.title('Scatter Plot of Values by Iteration')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()