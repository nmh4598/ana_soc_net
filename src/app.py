"""Streamlit app"""
import streamlit as st
import streamlit.components.v1 as components


from .pyvis_graph import PyvisGraph
from .graphs import Graph
from .cen_com import CenCom


def main():
    """Streamlit main page"""
    # Set header title
    st.set_page_config(layout="wide")
    st.title(" Analyse social network and random graph ")

    # Load HTML file in HTML component for display on Streamlit page
    col1, col2 = st.columns([0.3, 0.7])

    with col1:
        graph_ter = PyvisGraph(edges_path="data/ter/edges.csv", nodes_path="data/ter/nodes.csv")
        data = st.radio("Select data:", Graph.DATA_LIST)
        if data == Graph.DATA_LIST[0]:
            algo = st.radio(
                "Select centrality or community:", ("Community", "Centrality")
            )
            if algo == "Community":
                cen = st.selectbox("Select Community:", CenCom.COM_LIST)
                graph_ter.choose_data(Graph.DATA_LIST[0])
                graph_ter.gnet_pyvis(cen)
            else:
                com = st.selectbox("Select Centrality:", CenCom.CEN_LIST)
                graph_ter.choose_data(Graph.DATA_LIST[0])
                graph_ter.gnet_pyvis(com)
        else:
            st.write("Random Graph with communities.")
            randomgraph = st.selectbox("Select random graph:", Graph.RANDOM_MODEL_LIST)
            graph_ter.choose_data(Graph.DATA_LIST[1], randomgraph)

            com = st.selectbox("Select community:", CenCom.COM_LIST[1:])
            graph_ter.gnet_pyvis(com)
        st.write(graph_ter.info().T.rename(columns={0: "Properties"}))

    with col2:

        graph_ter.pyvis.save_graph("pyvis_graph.html")
        graph_ter_html = open("pyvis_graph.html", "r", encoding="utf-8")

        # Load HTML file in HTML component for display on Streamlit page
        components.html(graph_ter_html.read(), height=1020)


if __name__ == "__main__":
    main()
