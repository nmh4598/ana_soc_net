"""Class Graph"""
import re

import networkx as nx
import pandas as pd


class Graph:
    """A class representing a graph."""

    DATA_LIST = ["Mapping Networks of Terrorist Cells", "Random Graph"]

    RANDOM_MODEL_LIST = [
        "Erdős–Rényi model",
        "Watts and Strogatz model",
        "Caveman model",
        "Caveman connected model",
        "Caveman relaxed model",
    ]

    N: int = 100

    L: int = 20

    K: int = 5

    def __init__(self, edges_path: str, nodes_path: str) -> None:
        """Initializes a new Graph object."""
        self.edges_path: str = edges_path
        self.nodes_path: str = nodes_path
        self.edges: pd.DataFrame = None
        self.nodes: pd.DataFrame = None
        self.graph: nx.Graph = None
        self.rada: bool = None

    def load_data(self) -> None:
        """Loads the edges and nodes data from the CSV files."""
        self.edges = pd.read_csv(self.edges_path)
        self.nodes = pd.read_csv(self.nodes_path)
        print("Loading data...")
        # Clean nodes dataframe
        self.nodes = self.nodes.rename(
            {
                "# index": "index",
                " id": "id",
                " name": "name",
                " group": "group",
                " _pos": "pos",
            },
            axis="columns",
        )

        self.nodes["pos"] = self.nodes["pos"].apply(
            lambda s: tuple(
                float(re.search(r"\d+\.\d+", part).group())
                for part in s.split(",")
            )
        )

        def separate_row(row):
            row["x"], row["y"] = row["pos"]
            return row

        self.nodes = self.nodes.apply(separate_row, axis=1).assign(
            pos=self.nodes["pos"]
        )

    def create_graph(self) -> None:
        """Creates a graph from the loaded data."""
        self.load_data()

        g_pyvis = nx.Graph()

        for _, row in self.edges.iterrows():
            g_pyvis.add_edge(row["# source"], row[" target"])

        nx.set_node_attributes(
            g_pyvis,
            self.nodes[["index", "id", "name", "group", "pos"]]
            .set_index("index")
            .to_dict(orient="index"),
        )
        self.graph = g_pyvis
        print("Graph created...")

    def random_graph(self, random_model: str) -> None:
        """Creates a random graph of the specified model.

        Args:
            random_model (str): The model of the random graph to create.

        Raises:
            ValueError: If the specified model is not valid.

        """
        if random_model not in Graph.RANDOM_MODEL_LIST:
            raise ValueError(f"Invalid centrality name. Expected one of: \
                {Graph.RANDOM_MODEL_LIST}")

        if random_model == Graph.RANDOM_MODEL_LIST[0]:
            self.graph = nx.erdos_renyi_graph(
                Graph.N, 4.94 / Graph.N, seed=2023)

        elif random_model == Graph.RANDOM_MODEL_LIST[1]:
            self.graph = nx.watts_strogatz_graph(
                Graph.N, Graph.K, 0.5, seed=2023)

        elif random_model == Graph.RANDOM_MODEL_LIST[2]:
            self.graph = nx.caveman_graph(Graph.L, Graph.K)

        elif random_model == Graph.RANDOM_MODEL_LIST[3]:
            self.graph = nx.connected_caveman_graph(Graph.L, Graph.K)

        elif random_model == Graph.RANDOM_MODEL_LIST[4]:
            self.graph = nx.relaxed_caveman_graph(Graph.L, Graph.K,
                                                  0.3, seed=2023)

        print("Random graph created...")

    def choose_data(self, type_data: str, random_model: str = None) -> None:
        """Chooses the type of data to use:
        - "Mapping Networks of Terrorist Cells"
        - "Random Graph"

        Args:
            type_data (str): The type of data to use.
            random_model (str, optional): The model of the random graph to create. 
            Defaults to None.

        Raises:
            ValueError: If the specified data type is not valid.

        """
        if type_data == Graph.DATA_LIST[0]:
            self.create_graph()
            self.rada = False
        elif type_data == Graph.DATA_LIST[1]:
            self.random_graph(random_model)
            self.rada = True