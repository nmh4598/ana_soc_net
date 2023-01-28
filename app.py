import streamlit as st
import streamlit.components.v1 as components
import streamlit
import pandas as pd
import numpy as np
from pyvis.network import Network
import networkx as nx
import networkx.algorithms.community as nxcom
import re
import matplotlib.pyplot as plt
import webcolors
import random

n = 100
average_degree = 4.90322


def create_centrality_df(centrality_dict, column_name, df_init):
    df_centrality = pd.DataFrame.from_dict(centrality_dict, orient="index")
    df_centrality.columns = [column_name]
    df_centrality["Top_" + column_name.split()[-1]] = (
        df_centrality[column_name] >= df_centrality[column_name].nlargest(8).min()
    ).astype(int)
    df_fin_centrality = pd.concat([df_init, df_centrality], axis=1)
    return df_fin_centrality


def df_final():
    edges = pd.read_csv("data/ter/edges.csv")
    nodes = pd.read_csv("data/ter/nodes.csv")
    nodes = nodes.rename(
        {
            "# index": "index",
            " id": "id",
            " name": "name",
            " group": "group",
            " _pos": "pos",
        },
        axis="columns",
    )
    nodes["pos"] = nodes["pos"].apply(
        lambda s: tuple(
            [float(re.search(r"\d+\.\d+", part).group()) for part in s.split(",")]
        )
    )

    def separate_row(row):
        row["x"], row["y"] = row["pos"]
        return row

    nodes = nodes.apply(separate_row, axis=1).assign(pos=nodes["pos"])
    # Créer un graphique vide
    G = nx.Graph()
    for index, row in edges.iterrows():
        G.add_edge(row["# source"], row[" target"])
    # Ajouter les attributs de nœud au graphique
    nx.set_node_attributes(
        G,
        nodes[["index", "id", "name", "group", "pos"]]
        .set_index("index")
        .to_dict(orient="index"),
    )

    cen_deg = nx.degree_centrality(G)
    df_cen_deg = create_centrality_df(cen_deg, "La centralité de degré", nodes)

    cen_pro = nx.closeness_centrality(G)
    df_cen_pro = create_centrality_df(cen_pro, "La centralité de proximité", df_cen_deg)

    cen_int = nx.betweenness_centrality(G, normalized=False)
    df_cen_int = create_centrality_df(
        cen_int, "La centralité de intermédiaire", df_cen_pro
    )

    cen_eig = nx.eigenvector_centrality(G)
    df_cen_eig = create_centrality_df(
        cen_eig, "La centralité vecteur propre", df_cen_int
    )

    # Algorithme de Girvan Newman
    gine = nxcom.girvan_newman(G)
    com_gine = next(gine)
    df_com_gine = []
    for i, my_set in enumerate(com_gine):
        df = pd.DataFrame({"index": list(my_set)})
        df["group_gine"] = i
        df_com_gine.append(df)

    final_df_gine = pd.concat(df_com_gine, ignore_index=True)
    df_com_gine = pd.merge(
        df_cen_eig, final_df_gine, left_on="index", right_on="index", how="inner"
    )

    # Algorithme de Clauset, Newman Moore
    com_cmm = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
    df_com_cmm = []
    for i, my_set in enumerate(com_cmm):
        df = pd.DataFrame({"index": list(my_set)})
        df["group_cmm"] = i
        df_com_cmm.append(df)

    final_df_cmm = pd.concat(df_com_cmm, ignore_index=True)
    df_com_cmm = pd.merge(
        df_com_gine, final_df_cmm, left_on="index", right_on="index", how="inner"
    )

    # Algorithme de Louvain
    com_louvain = sorted(nxcom.louvain_communities(G, seed=123))
    df_com_louvain = []
    for i, my_set in enumerate(com_louvain):
        df = pd.DataFrame({"index": list(my_set)})
        df["group_louvain"] = i
        df_com_louvain.append(df)

    final_df_louvain = pd.concat(df_com_louvain, ignore_index=True)
    df_com_louvain = pd.merge(
        df_com_cmm, final_df_louvain, left_on="index", right_on="index", how="inner"
    )

    degrees = nx.degree_histogram(G)
    average_degree = (
        sum(i * degrees[i] for i in range(len(degrees))) / G.number_of_nodes()
    )
    df_mes = pd.DataFrame(
        data={
            "Number of nodes": [G.number_of_nodes()],
            "Number of edges": [G.number_of_edges()],
            "Directed graph": [nx.is_directed(G)],
            "Number of Components": [nx.number_connected_components(G)],
            "Average degre": [round(average_degree, 3)],
            "Density": [round(nx.density(G), 3)],
            "Diameter of Network": [nx.diameter(G)],
            "Average Shortest Path": [round(nx.average_shortest_path_length(G), 3)],
            "Clustering": [round(nx.average_clustering(G), 3)],
        }
    )
    return df_com_louvain, df_mes


def gnet_pyvis(df_final, couleur):
    edges = pd.read_csv("data/ter/edges.csv")
    color_map = {
        0: "#ff4d4d",
        1: "#33cc33",
        2: "#0066cc",
        3: "#990000",
        4: "#F8C471",
        5: "DarkSlateGray",
    }
    df_final["color"] = df_final[couleur].map(color_map)

    # G = Network( filter_menu=True)
    G = Network(height="1000px", width="100%", bgcolor="#E0E0E0", font_color="black")
    G.add_nodes(
        df_final["index"],
        x=df_final["x"],
        y=df_final["y"],
        label=df_final["name"],
        color=df_final["color"],
    )

    sources = edges["# source"]
    targets = edges[" target"]

    edge_data = zip(sources, targets)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        G.add_edge(src, dst)
    G.set_options(
        """
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
    )
    return G


def generate_random_color():
    return webcolors.rgb_to_hex(
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    )


def graph(G, algo):
    if algo == "gine":
        frozenset_com = nxcom.girvan_newman(G)
        list_com = next(frozenset_com)
    elif algo == "gmc":
        list_com = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
    elif algo == "louvain":
        list_com = sorted(nxcom.louvain_communities(G, seed=123))
    else:
        print(f"{algo} is not a valid community detection algorithm. Skipping...")
    list_test = []
    for frozenset in list_com:
        color = generate_random_color()
        for num in frozenset:
            list_test.append({"color": color, "id": num})
    return G, list_test


def mes(G):
    degrees = nx.degree_histogram(G)
    average_degree = (
        sum(i * degrees[i] for i in range(len(degrees))) / G.number_of_nodes()
    )
    df_mes = pd.DataFrame(
        data={
            "Number of nodes": [G.number_of_nodes()],
            "Number of edges": [G.number_of_edges()],
            "Directed graph": [nx.is_directed(G)],
            "Number of Components": [nx.number_connected_components(G)],
            "Average degre": [round(average_degree, 3)],
            "Density": [round(nx.density(G), 3)],
            "Diameter of Network": [nx.diameter(G)],
            "Average Shortest Path": [round(nx.average_shortest_path_length(G), 3)],
            "Clustering": [round(nx.average_clustering(G), 3)],
        }
    )
    return df_mes


def mes_caveman(G):
    degrees = nx.degree_histogram(G)
    average_degree = (
        sum(i * degrees[i] for i in range(len(degrees))) / G.number_of_nodes()
    )
    df_mes = pd.DataFrame(
        data={
            "Number of nodes": [G.number_of_nodes()],
            "Number of edges": [G.number_of_edges()],
            "Directed graph": [nx.is_directed(G)],
            "Number of Components": [nx.number_connected_components(G)],
            "Average degre": [round(average_degree, 3)],
            "Density": [round(nx.density(G), 3)],
            "Clustering": [round(nx.average_clustering(G), 3)],
        }
    )
    return df_mes


def Gnet_pyvis_random(algo, random_model):
    if random_model == "poisson":
        G = nx.erdos_renyi_graph(n, 4.94 / 100, seed=2)
        G, list_test = graph(G, algo)
        df_mes = mes(G)
    if random_model == "wa_st":
        G = nx.watts_strogatz_graph(n, int(4.94), 0.5, seed=3)
        G, list_test = graph(G, algo)
        df_mes = mes(G)
    if random_model == "caveman":
        G = nx.caveman_graph(20, 5)
        G, list_test = graph(G, algo)
        df_mes = mes_caveman(G)
    if random_model == "caveman_con":
        G = nx.connected_caveman_graph(20, 5)
        G, list_test = graph(G, algo)
        df_mes = mes(G)
    if random_model == "caveman_re":
        G = nx.relaxed_caveman_graph(20, 5, 0.3)
        G, list_test = graph(G, algo)
        df_mes = mes(G)

    G_pyvis = Network(
        height="1000px", width="100%", bgcolor="#E0E0E0", font_color="black"
    )
    G_pyvis.from_nx(G)
    list_nodes = G_pyvis.get_network_data()[0]
    for node in list_nodes:
        node["color"] = next(
            (item["color"] for item in list_test if item["id"] == node["id"]), None
        )
    G_pyvis.set_options(
        """
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
    )

    return G_pyvis, df_mes


# Set header title
st.set_page_config(layout="wide")
st.title(" Analyse social network and random graph ")

base = st.get_option("theme.base")
primary_color = st.get_option("theme.primaryColor")
base = "dark"
primaryColor = "#35b6dc"

# Load HTML file in HTML component for display on Streamlit page
col1, col2 = st.columns([0.2, 0.8])
with col1:
    data_list = ["Mapping Networks of Terrorist Cells", "Random Graph with communities"]
    data = st.selectbox("Select data:", data_list)

    com_list = [
        "Communities: Girvan Newman",
        "Communities: Clauset, Newman Moore",
        "Communities: Louvain",
    ]
    random_model_list = [
        "Erdős–Rényi model",
        "Watts and Strogatz model",
        "Caveman model",
        "Caveman connected model",
        "Caveman relaxed model",
    ]
    com_cen_list = [
        "Communities: AF11, AF175, AF77, AF93, other ",
        "Communities: Girvan Newman",
        "Communities: Clauset, Newman Moore",
        "Communities: Louvain",
        "Centrality : Betweenness Centrality",
        "Centrality : Degree Centrality",
        "Centrality : Closeness Centrality",
        "Centrality : Eigenvector Centrality",
    ]
    algo = ["gine", "gmc", "louvain"]
    if data == data_list[0]:
        com_cen = st.selectbox("Select communities or centrality:", com_cen_list)
        if com_cen == com_cen_list[0]:
            df_com = "group"
        elif com_cen == com_cen_list[1]:
            df_com = "group_gine"
        elif com_cen == com_cen_list[2]:
            df_com = "group_cmm"
        elif com_cen == com_cen_list[3]:
            df_com = "group_louvain"
        elif com_cen == com_cen_list[4]:
            df_com = "Top_intermédiaire"
        elif com_cen == com_cen_list[5]:
            df_com = "Top_degré"
        elif com_cen == com_cen_list[6]:
            df_com = "Top_proximité"
        else:
            df_com = "Top_propre"
        df_final, df_mes = df_final()
        G = gnet_pyvis(df_final, df_com)
        st.subheader("Network Properties")
        st.write(df_mes.T.rename(columns={0: "Properties"}))
    if data == data_list[1]:
        random_model = st.selectbox("Select model:", random_model_list)
        com = st.selectbox("Select communities or centrality:", com_list)
        if random_model == random_model_list[0] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random(algo[0], "poisson")
        elif random_model == random_model_list[0] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random(algo[1], "poisson")
        elif random_model == random_model_list[0] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random(algo[2], "poisson")
        elif random_model == random_model_list[1] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random(algo[0], "wa_st")
        elif random_model == random_model_list[1] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random(algo[1], "wa_st")
        elif random_model == random_model_list[1] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random(algo[2], "wa_st")
        elif random_model == random_model_list[2] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random(algo[0], "caveman")
        elif random_model == random_model_list[2] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random(algo[1], "caveman")
        elif random_model == random_model_list[2] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random(algo[2], "caveman")
        elif random_model == random_model_list[3] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random(algo[0], "caveman_con")
        elif random_model == random_model_list[3] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random(algo[1], "caveman_con")
        elif random_model == random_model_list[3] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random(algo[2], "caveman_con")
        elif random_model == random_model_list[4] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random(algo[0], "caveman_re")
        elif random_model == random_model_list[4] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random(algo[1], "caveman_re")
        elif random_model == random_model_list[4] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random(algo[2], "caveman_re")
        st.write(df_mes.T.rename(columns={0: "Properties"}))
with col2:
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        G.save_graph("ouput/pyvis_graph.html")
        HtmlFile = open("output/pyvis_graph.html", "r", encoding="utf-8")

    # Save and read graph as HTML file (locally)
    except:
        G.save_graph("output/pyvis_graph.html")
        HtmlFile = open("output/pyvis_graph.html", "r", encoding="utf-8")

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=1020)
