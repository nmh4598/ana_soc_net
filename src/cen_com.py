"""Class Centrality and Community"""
import networkx as nx
import pandas as pd
from .carac import Carac
import networkx.algorithms.community as nxcom
import webcolors
import random


class CenCom(Carac):
    """Class CenCom"""

    CEN_LIST = [
        "Centrality : Degree Centrality",
        "Centrality : Betweenness Centrality",
        "Centrality : Closeness Centrality",
        "Centrality : Eigenvector Centrality",
    ]

    COM_LIST = [
        "Communities: AF11, AF175, AF77, AF93, other ",
        "Communities: Girvan Newman",
        "Communities: Clauset, Newman Moore",
        "Communities: Louvain",
    ]

    def init(self):
        """Inheritance from class Carac"""
        Carac.__init__(self, edges_path, nodes_path)

    def _create_centrality_df(self, centrality_dict: dict, algo: str, n: int = 8):
        df_centrality = pd.DataFrame.from_dict(centrality_dict, orient="index")
        df_centrality.columns = [algo]
        df_centrality["Top_" + algo.split()[-1]] = (
            df_centrality[algo] >= df_centrality[algo].nlargest(n).min()
        ).astype(int)
        self.df_centrality = pd.concat([self.nodes, df_centrality], axis=1)

    def centrality(self, algo: str, n: int = 8):
        """Calculate degree centrality and assign top n nodes a value of 1, otherwise 0.

        Args:
            algo (str): Name of the centrality column to create.
            n (int): Number of top nodes to assign a value of 1.

        This function creates a self.centrality dataframe with self.nodes and 2 new columns:
            - `algo`: Column with degree centrality values.
            - "Top_centrality": Top n nodes will have a value of 1, other nodes will have 0.
        """
        if algo not in CenCom.CEN_LIST:
            raise ValueError(
                f"Invalid centrality name. Expected one of: {CenCom.CEN_LIST}"
            )

        elif algo == CenCom.CEN_LIST[0]:
            centrality_algo = nx.degree_centrality(self.graph)

        elif algo == CenCom.CEN_LIST[1]:
            centrality_algo = nx.betweenness_centrality(self.graph, normalized=False)

        elif algo == CenCom.CEN_LIST[2]:
            centrality_algo = nx.closeness_centrality(self.graph)

        elif algo == CenCom.CEN_LIST[3]:
            centrality_algo = nx.eigenvector_centrality(self.graph)

        self._create_centrality_df(centrality_algo, algo, n)
        print("Centrality calculated...")

    def _generate_random_color():
        return webcolors.rgb_to_hex(
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )

    def _create_communities_df(self, communities: frozenset, algo: str):
        if self.rg == True:
            # Creat color for random graph
            self.list_test = []
            for frozenset in communities:
                color = CenCom._generate_random_color()
                for num in frozenset:
                    self.list_test.append({"color": color, "id": num})
            print("Created color for undirected graph...")
        else:
            df_com = []
            for i, my_set in enumerate(communities):
                df = pd.DataFrame({"index": list(my_set)})
                df[algo] = i
                df_com.append(df)

            final_df = pd.concat(df_com, ignore_index=True)
            self.df_communities = pd.merge(
                self.nodes, final_df, left_on="index", right_on="index", how="inner"
            )

    def communities(self, algo: str):
        if algo not in CenCom.COM_LIST:
            raise ValueError(
                f"Invalid centrality name. Expected one of: {CenCom.COM_LIST}"
            )

        elif algo == CenCom.COM_LIST[1]:
            communities_algo = next(nxcom.girvan_newman(self.graph))

        elif algo == CenCom.COM_LIST[2]:
            communities_algo = sorted(
                nxcom.greedy_modularity_communities(self.graph), key=len, reverse=True
            )

        elif algo == CenCom.COM_LIST[3]:
            communities_algo = sorted(nxcom.louvain_communities(self.graph, seed=123))

        self._create_communities_df(communities_algo, algo)
        print("Communities calculated...")
