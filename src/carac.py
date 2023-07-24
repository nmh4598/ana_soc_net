"""Class Carac"""
import networkx as nx
import pandas as pd
from graphs import Graph
import re


class Carac(Graph):
    """Class Carac"""
    def init(self):
        Graph.__init__(self, edges_path, nodes_path)

    def info(self):
        nb_nodes = self.graph.number_of_nodes()
        nb_edges = self.graph.number_of_edges()
        nb_components = nx.number_connected_components(self.graph)
        degrees = nx.degree_histogram(self.graph)
        avg_degree = round(
            (
                sum(i * degrees[i] for i in range(len(degrees)))
                / nb_nodes
            ),
            3,
        )
        density = round(nx.density(self.graph), 3)
        clustering = round(nx.average_clustering(self.graph), 3)
        directed = nx.is_directed(self.graph)

        if self.rg == False:
            avg_spl = round(nx.average_shortest_path_length(self.graph), 3)
            diameter = nx.diameter(self.graph)
            df_carac = pd.DataFrame(
                data={
                    "Number of nodes": [nb_nodes],
                    "Number of edges": [nb_edges],
                    "Directed graph": [directed],
                    "Number of Components": [nb_components],
                    "Average degre": [avg_degree],
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
                    "Average degre": [avg_degree],
                    "Density": [density],
                    "Clustering": [clustering],
                }
            )
        return df_carac
