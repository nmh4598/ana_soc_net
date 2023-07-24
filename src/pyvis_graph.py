import networkx as nx
import pandas as pd
from pyvis.network import Network
import streamlit as st

from .cen_com import CenCom
from .graphs import Graph


class PyvisGraph(CenCom):
    COLOR_MAP = {
        0: "#ff4d4d",
        1: "#33cc33",
        2: "#0066cc",
        3: "#990000",
        4: "#F8C471",
        5: "DarkSlateGray",
    }

    OPTION1 = """
        const options = {
          "nodes": {
            "borderWidth": 7,
            "opacity": 0.2,
            "font": {
              "size": 31
            },
            "scaling": {
              "min": 29,
              "max": 85
            },
            "shapeProperties": {
              "borderRadius": 7
            },
            "size": 30
          },
          "physics": {
            "forceAtlas2Based": {
              "springLength": 100
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """

    OPTION2 = """
        const options = {   
          "physics": {
            "forceAtlas2Based": {
              "springLength": 100
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """

    def init(self):
        CenCom.__init__(self, edges_path, nodes_path)

    def _add_nodes_and_edges(self, graph, df_pyvis):
        graph.add_nodes(
            df_pyvis["index"],
            x=df_pyvis["x"],
            y=df_pyvis["y"],
            label=df_pyvis["name"],
            color=df_pyvis["color"],
        )
        sources = self.edges["# source"]
        targets = self.edges[" target"]
        edge_data = zip(sources, targets)
        for e in edge_data:
            src = e[0]
            dst = e[1]
            graph.add_edge(src, dst)

    def gnet_pyvis(self, algo: str, n: int = 8):
        print("Initializing pyvis graph...")
        G = Network(height="900px", width="100%", bgcolor="#FFFFFF", font_color="black")

        if algo not in CenCom.CEN_LIST + CenCom.COM_LIST:
            raise ValueError(
                f"Invalid centrality name. Expected one of: {CenCom.COM_LIST + CenCom.COM_LIST}"
            )

        if algo in CenCom.CEN_LIST:
            print(f"Calculating {algo}")
            self.centrality(algo, n)
            df_pyvis = self.df_centrality
            df_pyvis["color"] = df_pyvis.iloc[:, 8].map(PyvisGraph.COLOR_MAP)
            self._add_nodes_and_edges(G, df_pyvis)
            G.set_options(PyvisGraph.OPTION1)

        elif algo in CenCom.COM_LIST:
            print(f"Calculating {algo}")
            if self.rg == False:
                if algo == CenCom.COM_LIST[0]:
                    df_pyvis = self.nodes.copy()
                    df_pyvis["color"] = df_pyvis["group"].map(PyvisGraph.COLOR_MAP)
                    print("Data default")
                else:
                    self.communities(algo)
                    df_pyvis = self.df_communities.copy()
                    df_pyvis["color"] = df_pyvis.iloc[:, 7].map(PyvisGraph.COLOR_MAP)
                self._add_nodes_and_edges(G, df_pyvis)
                G.set_options(PyvisGraph.OPTION1)
            elif self.rg == True:
                self.communities(algo)
                G.from_nx(self.graph)
                list_nodes = G.get_network_data()[0]
                for node in list_nodes:
                    node["color"] = next(
                        (
                            item["color"]
                            for item in self.list_test
                            if item["id"] == node["id"]
                        ),
                        None,
                    )
                print("Created random graph pyvis...")
                G.set_options(PyvisGraph.OPTION2)

            print("Created graph pyvis")
        # G.show_buttons(filter_=['physics'])
        self.pyvis = G


if __name__ == "__main__":
    G1 = PyvisGraph(edges_path="data/ter/edges.csv", nodes_path="data/ter/nodes.csv")
    G1.create_graph()
    G1.choose_data(Graph.DATA_LIST[0])
    # G1.info()
    G1.gnet_pyvis(CenCom.CEN_LIST[0])
    G1.pyvis.save_graph("pyvis_graph.html")
