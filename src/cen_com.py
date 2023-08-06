"""Class Centrality and Community"""
import random
from typing import List, Dict, Union

import networkx as nx

# import networkx.algorithms.community as nxcom
import pandas as pd
import webcolors

from .carac import Carac


class CenCom(Carac):
    """A class for computing the centrality and communities of a graph."""

    CEN_LIST: List[str] = [
        "Centrality : Degree Centrality",
        "Centrality : Betweenness Centrality",
        "Centrality : Closeness Centrality",
        "Centrality : Eigenvector Centrality",
    ]

    COM_LIST: List[str] = [
        "Communities: AF11, AF175, AF77, AF93, other ",
        "Communities: Girvan Newman",
        "Communities: Clauset, Newman Moore",
        "Communities: Louvain",
    ]

    def __init__(self, edges_path: str, nodes_path: str) -> None:
        """Initialize a new CenCom object."""
        super().__init__(edges_path, nodes_path)
        self.df_centrality: pd.DataFrame = None
        self.df_community: pd.DataFrame = None
        self.list_test: List[Dict[str, Union[str, int]]] = []

    def _create_centrality_df(
        self, centrality_dict: dict, algo: str, n_cen: int = 8
    ) -> None:
        df_centrality = pd.DataFrame.from_dict(centrality_dict, orient="index")
        df_centrality.columns = [algo]
        df_centrality["Top_" + algo.split()[-1]] = (
            df_centrality[algo] >= df_centrality[algo].nlargest(n_cen).min()
        ).astype(int)
        self.df_centrality = pd.concat([self.nodes, df_centrality], axis=1)
        print(self.df_centrality)

    def centrality(self, algo: str, n_cen: int = 8) -> None:
        """Calculate degree centrality and assign top n nodes a value of
            1, otherwise 0.

            Args:
                algo (str): Name of the centrality column to create.
                n_cen (int): Number of top nodes to assign a value of 1.

            This function creates a self.df_centrality dataframe with self.nodes and 2 new columns:
            `algo`: Column with degree centrality values and `Top_centrality` Top n nodes will have 
            a value of 1, other nodes will have 0.
        """
        if algo not in CenCom.CEN_LIST:
            raise ValueError(
                f"Invalid centrality name. Expected one of: \
                             {CenCom.CEN_LIST}"
            )

        if algo == CenCom.CEN_LIST[0]:
            centrality_algo = nx.degree_centrality(self.graph)

        elif algo == CenCom.CEN_LIST[1]:
            centrality_algo = nx.betweenness_centrality(self.graph, normalized=False)

        elif algo == CenCom.CEN_LIST[2]:
            centrality_algo = nx.closeness_centrality(self.graph)

        elif algo == CenCom.CEN_LIST[3]:
            centrality_algo = nx.eigenvector_centrality(self.graph)

        self._create_centrality_df(centrality_algo, algo, n_cen)
        print("Centrality calculated...")

    def _create_communities_df(self, communities, algo: str) -> None:
        if self.rada is True:
            # Creat color for random graph
            for frozen_set in communities:
                color = webcolors.rgb_to_hex(
                    (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
                )
                for num in frozen_set:
                    self.list_test.append({"color": color, "id": num})
            print("Created color for undirected graph...")
        else:
            df_com = []
            for i, my_set in enumerate(communities):
                df_color = pd.DataFrame({"index": list(my_set)})
                df_color[algo] = i
                df_com.append(df_color)

            final_df = pd.concat(df_com, ignore_index=True)
            self.df_community = pd.merge(
                self.nodes, final_df, left_on="index", right_on="index", how="inner"
            )
            print(self.df_community)

    def communities(self, algo: str) -> None:
        """Compute the communities of the graph and assign a color to each community.

            Args:
                algo (str): The name of the algorithm to use for computing the communities.

            This function creates a self.df_community dataframe with self.nodes with a new column
            `communities`: Column with the communities values. 
        """
        if algo not in CenCom.COM_LIST:
            raise ValueError(
                f"Invalid centrality name. Expected one of: {CenCom.COM_LIST}"
            )

        if algo == CenCom.COM_LIST[1]:
            communities_algo = next(nx.algorithms.community.girvan_newman(self.graph))

        elif algo == CenCom.COM_LIST[2]:
            communities_algo = sorted(
                nx.algorithms.community.greedy_modularity_communities(self.graph),
                key=len,
                reverse=True,
            )

        elif algo == CenCom.COM_LIST[3]:
            communities_algo = sorted(
                nx.algorithms.community.label_propagation_communities(self.graph)
            )

        self._create_communities_df(communities_algo, algo)
        print("Communities calculated...")
