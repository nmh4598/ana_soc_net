"""Streamlit app"""
import streamlit as st
import streamlit.components.v1 as components


from .pyvis_graph import PyvisGraph
from .graphs import Graph
from .cen_com import CenCom


def main():
    # Set header title
    st.set_page_config(layout="wide")
    st.title(" Analyse social network and random graph ")

    base = st.get_option("theme.base")
    primary_color = st.get_option("theme.primaryColor")
    base = "black"
    primaryColor = "#35b6dc"

    # Load HTML file in HTML component for display on Streamlit page
    col1, col2 = st.columns([0.3, 0.7])

    with col1:
        G = PyvisGraph(edges_path="data/ter/edges.csv", nodes_path="data/ter/nodes.csv")
        data = st.radio("Select data:", Graph.DATA_LIST)
        if data == Graph.DATA_LIST[0]:
            algo = st.radio(
                "Select centrality or community:", ("Community", "Centrality")
            )
            if algo == "Community":
                cen = st.selectbox("Select Community:", CenCom.COM_LIST)
                G.choose_data(Graph.DATA_LIST[0])
                G.gnet_pyvis(cen)
            else:
                com = st.selectbox("Select Centrality:", CenCom.CEN_LIST)
                G.choose_data(Graph.DATA_LIST[0])
                G.gnet_pyvis(com)
        else:
            st.write("Random Graph with communities.")
            rg = st.selectbox("Select random graph:", Graph.RANDOM_MODEL_LIST)
            G.choose_data(Graph.DATA_LIST[1], rg)

            com = st.selectbox("Select community:", CenCom.COM_LIST[1:])
            G.gnet_pyvis(com)
        st.write(G.info().T.rename(columns={0: "Properties"}))

    with col2:
        try:
            G.pyvis.save_graph("pyvis_graph.html")
            HtmlFile = open("pyvis_graph.html", "r", encoding="utf-8")

        # Save and read graph as HTML file (locally)
        except:
            G.pyvis.save_graph("pyvis_graph.html")
            HtmlFile = open("pyvis_graph.html", "r", encoding="utf-8")

        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=1020)


if __name__ == "__main__":
    main()
