"""Class PyvisGraph"""
from pyvis.network import Network

from .cen_com import CenCom


class PyvisGraph(CenCom):
    """A class for creating a pyvis graph."""

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

    def __init__(self, edges_path: str, nodes_path: str) -> None:
        super().__init__(edges_path, nodes_path)
        self.pyvis = None

    def _add_nodes_and_edges(self, graph, df_pyvis) -> None:
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
        for edge in edge_data:
            src = edge[0]
            dst = edge[1]
            graph.add_edge(src, dst)

    def gnet_pyvis(self, algo: str, n_cen: int = 8) -> None:
        """Create a pyvis graph"""
        print("Initializing pyvis graph...")
        g_pyvis = Network(
            height="900px", width="100%", bgcolor="#FFFFFF", font_color="black"
        )

        if algo not in CenCom.CEN_LIST + CenCom.COM_LIST:
            raise ValueError(
                f"Invalid centrality name. Expected one of:\
                {CenCom.COM_LIST + CenCom.COM_LIST}"
            )

        if algo in CenCom.CEN_LIST:
            print(f"Calculating {algo}")
            self.centrality(algo, n_cen)
            df_pyvis = self.df_centrality
            df_pyvis["color"] = df_pyvis.iloc[:, 8].map(PyvisGraph.COLOR_MAP)
            self._add_nodes_and_edges(g_pyvis, df_pyvis)
            g_pyvis.set_options(PyvisGraph.OPTION1)

        elif algo in CenCom.COM_LIST:
            print(f"Calculating {algo}")
            if self.rada is False:
                if algo == CenCom.COM_LIST[0]:
                    df_pyvis = self.nodes.copy()
                    df_pyvis["color"] = df_pyvis["group"].map(PyvisGraph.COLOR_MAP)
                    print("Data default")
                else:
                    self.communities(algo)
                    df_pyvis = self.df_community.copy()
                    df_pyvis["color"] = df_pyvis.iloc[:, 7].map(PyvisGraph.COLOR_MAP)
                self._add_nodes_and_edges(g_pyvis, df_pyvis)
                g_pyvis.set_options(PyvisGraph.OPTION1)
            elif self.rada is True:
                self.communities(algo)
                g_pyvis.from_nx(self.graph)
                list_nodes = g_pyvis.get_network_data()[0]
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
                g_pyvis.set_options(PyvisGraph.OPTION2)

            print("Created graph pyvis")
        # G.show_buttons(filter_=['physics'])
        self.pyvis = g_pyvis
