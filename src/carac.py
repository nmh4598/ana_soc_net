"""Class Carac"""
import networkx as nx
import pandas as pd

from .graphs import Graph


class Carac(Graph):
    """A class for computing the main characteristics of a graph."""

    def __init__(self, edges_path: str, nodes_path: str):
        """Initialize a new Carac object.
        """
        super().__init__(edges_path, nodes_path)

    def info(self) -> pd.DataFrame:
        """Compute the main characteristics of the graph and return them as a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the following columns:
                - Number of nodes
                - Number of edges
                - Directed graph
                - Number of components
                - Average degree
                - Density
                - Clustering
                - Diameter of Network (if the graph is not a RADA graph)
                - Average Shortest Path (if the graph is not a RADA graph)
        """
        # Compute the main characteristics of the graph
        nb_nodes = self.graph.number_of_nodes()
        nb_edges = self.graph.number_of_edges()
        nb_components = nx.number_connected_components(self.graph)
        degrees = nx.degree_histogram(self.graph)
        avg_degree = round(
            (sum(i * degrees[i] for i in range(len(degrees))) / nb_nodes),
            3,
        )
        density = round(nx.density(self.graph), 3)
        clustering = round(nx.average_clustering(self.graph), 3)
        directed = nx.is_directed(self.graph)

        if self.rada is False:
            avg_spl = round(nx.average_shortest_path_length(self.graph), 3)
            diameter = nx.diameter(self.graph)
            df_carac = pd.DataFrame(
                data={
                    "Number of nodes": [nb_nodes],
                    "Number of edges": [nb_edges],
                    "Directed graph": [directed],
                    "Number of Components": [nb_components],
                    "Average degree": [avg_degree],
                    "Density": [density],
                    "Clustering": [clustering],
                    "Diameter of Network": [diameter],
                    "Average Shortest Path": [avg_spl],
                }
            )
        else:
            df_carac = pd.DataFrame(
                data={
                    "Number of nodes": [nb_nodes],
                    "Number of edges": [nb_edges],
                    "Directed graph": [directed],
                    "Number of Components": [nb_components],
                    "Average degree": [avg_degree],
                    "Density": [density],
                    "Clustering": [clustering],
                }
            )
        return df_carac