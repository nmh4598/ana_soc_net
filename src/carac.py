import networkx as nx
import pandas as pd
from graphs import Graph
import re


class Carac(Graph):
    def init(self):
        Graph.__init__(self, edges_path, nodes_path)

    def info(self):
        self.nb_nodes = self.graph.number_of_nodes()
        self.nb_edges = self.graph.number_of_edges()
        self.nb_components = nx.number_connected_components(self.graph)
        self.degrees = nx.degree_histogram(self.graph)
        self.avg_degree = round(
            (
                sum(i * self.degrees[i] for i in range(len(self.degrees)))
                / self.nb_nodes
            ),
            3,
        )
        self.density = round(nx.density(self.graph), 3)
        self.clustering = round(nx.average_clustering(self.graph), 3)
        self.directed = nx.is_directed(self.graph)

        if self.rg == False:
            self.avg_spl = round(nx.average_shortest_path_length(self.graph), 3)
            self.diameter = nx.diameter(self.graph)
            df_carac = pd.DataFrame(
                data={
                    "Number of nodes": [self.nb_nodes],
                    "Number of edges": [self.nb_edges],
                    "Directed graph": [self.directed],
                    "Number of Components": [self.nb_components],
                    "Average degre": [self.avg_degree],
                    "Density": [self.density],
                    "Clustering": [self.clustering],
                    "Diameter of Network": [self.diameter],
                    "Average Shortest Path": [self.avg_spl],
                }
            )
        else:
            df_carac = pd.DataFrame(
                data={
                    "Number of nodes": [self.nb_nodes],
                    "Number of edges": [self.nb_edges],
                    "Directed graph": [self.directed],
                    "Number of Components": [self.nb_components],
                    "Average degre": [self.avg_degree],
                    "Density": [self.density],
                    "Clustering": [self.clustering],
                }
            )
        return df_carac
