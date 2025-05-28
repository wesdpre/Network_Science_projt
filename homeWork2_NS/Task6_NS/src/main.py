import modularity_utils as modularity_utils
import utils
import pandas as pd
import os


if __name__ == "__main__":
    print("This is the main entry point of the application.")
    print("We will use as input the movies.csv file and the movies network files.")
    print("Validating if the movies.csv files is in the path ../movies/movies.csv")
    movies_csv_path = "../movies/movies/movies.csv"
    if os.path.isfile(movies_csv_path):
        print("File exists.")
    else:
        print("File does not exist. Exiting the program.")
        exit(1)

    movies_data = pd.read_csv("../movies/movies/movies.csv")
    print("please check a sample of movies ids and choose on of them:")

    sampled = movies_data.sample(10)
    result = [{"id": row["ID"], "title": row["Title"]} for _, row in sampled.iterrows()]
    print(result)

    file_index = input("Please enter the file index (e.g., 1, 2, 3): ")
    input_movie_title = movies_data.loc[
        movies_data["ID"] == int(file_index), "Title"].values[0]
    print(f"You have selected the movie: {input_movie_title} with index {file_index}")
    
    print("Computing the network community using NetworkX Louvain algorithm.")
    nodes_df, edges_df = utils.get_network_dataframe(file_index)
    G = utils.create_graph_from_dataframes(nodes_df, edges_df)
    communities, _ = utils.compute_louvain_communities(G, edges_df)
    pagerank_scores = utils.compute_pagerank(G, edges_df)
    labels = {node: G.nodes[node].get("label") for node in G.nodes()}
    print(f"Self implemented modularity score: {modularity_utils.compute_modularity(G, communities):.4f}")
    modularity_utils.compute_modularity(G, communities)
    # print(labels)
    utils.visualize_communities_pgrank(
        G, communities, title=input_movie_title, pagerank_scores=pagerank_scores
    )
    
    print("Computing the communities using self implemented greedy agglomerative algorithm.")
    communities_greedy, progress_scoress = modularity_utils.greedy_agglomerative(G)
    modularity_utils.compute_modularity(G, communities_greedy)
    utils.visualize_communities_pgrank(
        G, communities_greedy, title=input_movie_title + " - Self implemented Greedy Agglomerative"
    )
    print(f"Modularity score for the greedy agglomerative algorithm: {modularity_utils.compute_modularity(G, communities_greedy):.4f}")
    
    modularity_utils.plot_progress(progress_scoress)
