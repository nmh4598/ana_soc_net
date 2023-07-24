"""Main module for the streamlit app."""
import os

import streamlit as st
import streamlit.components.v1 as components

from src.pyvis_graph import PyvisGraph
from src.graphs import Graph
from src.cen_com import CenCom


def main():
    """Main function of the App."""
    # Set header title
    st.set_page_config(layout="wide")
    st.title(" Analyse social network and random graph ")

    # Load HTML file in HTML component for display on Streamlit page
    col1, col2 = st.columns([0.2, 0.8])

    with col1:
        g_pyvis = PyvisGraph(
            edges_path="data/ter/edges.csv", nodes_path="data/ter/nodes.csv"
        )
        data = st.radio("Select data:", Graph.DATA_LIST)
        if data == Graph.DATA_LIST[0]:
            algo = st.radio(
                "Select centrality or community:", ("Community", "Centrality")
            )
            if algo == "Community":
                cen = st.selectbox("Select Community:", CenCom.COM_LIST)
                g_pyvis.choose_data(Graph.DATA_LIST[0])
                g_pyvis.gnet_pyvis(cen)
            else:
                com = st.selectbox("Select Centrality:", CenCom.CEN_LIST)
                g_pyvis.choose_data(Graph.DATA_LIST[0])
                g_pyvis.gnet_pyvis(com)
        else:
            st.write("Random Graph with communities.")
            rada = st.selectbox("Select random graph:", Graph.RANDOM_MODEL_LIST)
            g_pyvis.choose_data(Graph.DATA_LIST[1], rada)

            com = st.selectbox("Select community:", CenCom.COM_LIST[1:])
            g_pyvis.gnet_pyvis(com)
        st.write(g_pyvis.info().astype(float).T.rename(columns={0: "Properties"}))

    with col2:
        output_path = os.path.join("output", "pyvis_graph.html")
        g_pyvis.pyvis.save_graph(output_path)
        # Load HTML file in HTML component for display on Streamlit page
        with open(output_path, "r", encoding="utf-8") as graph_ter_html:
            components.html(graph_ter_html.read(), height=1020)


if __name__ == "__main__":
    main()
