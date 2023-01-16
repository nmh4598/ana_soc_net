from pyvis.network import Network
import networkx as nx
import networkx.algorithms.community as nxcom
import pandas as pd
import re
import matplotlib.pyplot as plt
import webcolors
import random

n = 100
average_degree = 4.90322

def generate_random_color():
    return webcolors.rgb_to_hex((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
def graph(G,algo):    
    if algo == 'gine':
        frozenset_com = nxcom.girvan_newman(G)
        list_com= next(frozenset_com)
    elif algo == 'gmc':
        list_com  = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
    elif algo == 'louvain':
        list_com  = sorted(nxcom.louvain_communities(G, seed=123))
    else:
        print(f"{algo} is not a valid community detection algorithm. Skipping...")         
    list_test = []
    for frozenset in list_com:
        color = generate_random_color()
        for num in frozenset:
            list_test.append({'color': color, 'id': num})
    return G,list_test
def mes(G): 
    degrees = nx.degree_histogram(G)
    average_degree = sum(i * degrees[i] for i in range(len(degrees))) / G.number_of_nodes()
    df_mes = pd.DataFrame(
        data={"Number of nodes": [G.number_of_nodes()], 
            "Number of edges": [G.number_of_edges()],
            "Directed graph": [nx.is_directed(G)],
            "Number of Components":  [nx.number_connected_components(G)],
            "Average degre": [round(average_degree,3)],
            "Density": [round(nx.density(G),3)],
            "Diameter of Network": [nx.diameter(G)],
            "Average Shortest Path": [round(nx.average_shortest_path_length(G), 3)],
            "Clustering": [round(nx.average_clustering(G), 3)]})
    return df_mes
def mes_caveman(G): 
    degrees = nx.degree_histogram(G)
    average_degree = sum(i * degrees[i] for i in range(len(degrees))) / G.number_of_nodes()
    df_mes = pd.DataFrame(
        data={"Number of nodes": [G.number_of_nodes()], 
            "Number of edges": [G.number_of_edges()],
            "Directed graph": [nx.is_directed(G)],
            "Number of Components":  [nx.number_connected_components(G)],
            "Average degre": [round(average_degree,3)],
            "Density": [round(nx.density(G),3)],
            "Clustering": [round(nx.average_clustering(G), 3)]})
    return df_mes
def Gnet_pyvis_random(algo, random_model):   
    if random_model == 'poisson':
        G = nx.erdos_renyi_graph(n, 4.94/100, seed=2)
        G, list_test = graph(G,algo)
        df_mes =mes(G)
    if random_model == 'wa_st': 
        G = nx.watts_strogatz_graph(n, int(4.94), 0.5 , seed=3)
        G, list_test = graph(G,algo)
        df_mes =mes(G)        
    if random_model == 'caveman': 
        G = nx.caveman_graph(20, 5)
        G, list_test = graph(G,algo)
        df_mes = mes_caveman(G)        
    if random_model == 'caveman_con': 
        G = nx.connected_caveman_graph(20, 5)
        G, list_test = graph(G,algo)     
        df_mes = mes(G)     
    if random_model == 'caveman_re': 
        G = nx.relaxed_caveman_graph(20, 5, 0.3)
        G, list_test = graph(G,algo)     
        df_mes = mes(G)          
        
    G_pyvis = Network(height='1000px', width='100%', bgcolor='#E0E0E0', font_color='black')   
    G_pyvis.from_nx(G)
    list_nodes = G_pyvis.get_network_data()[0]
    for node in list_nodes:
        node['color'] = next((item['color'] for item in list_test if item["id"] == node["id"]), None)
    G_pyvis.set_options("""
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
if __name__ == '__main__':
    algo =[ 'gine','gmc','louvain']
    #G_pyvis.show_buttons(filter_=['physics'])
    ## Test poisson
    G_pyvis, df_mes = Gnet_pyvis_random( algo[0],'poisson')    
    G_pyvis.show('output/random_graph/randomgraph_poisson_gine.html')
    print(df_mes)
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[1],'poisson') 
    # G_pyvis.show('output/random_graph/randomgraph_poisson_gmc.html')
    
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[2],'poisson') 
    # G_pyvis.show('output/random_graph/randomgraph_poisson_louvain.html')   
     
    # ## Test Watts et Strogatz
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[0],'wa_st')    
    # G_pyvis.show('output/random_graph/randomgraph_wa_st_gine.html')
    
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[1],'wa_st') 
    # G_pyvis.show('output/random_graph/randomgraph_wa_st_gmc.html')
    
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[2],'wa_st') 
    # G_pyvis.show('output/random_graph/randomgraph_wa_st_louvain.html')    
    
    ## Test Caveman
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[0],'caveman')    
    # G_pyvis.show('output/random_graph/randomgraph_caveman_gine.html')
    
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[1],'caveman') 
    # G_pyvis.show('output/random_graph/randomgraph_caveman_gmc.html')
    
    # G_pyvis, df_mes = Gnet_pyvis_random( algo[2],'caveman') 
    # G_pyvis.show('output/random_graph/randomgraph_caveman_louvain.html')   
