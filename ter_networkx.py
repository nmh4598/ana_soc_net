# Importation les packages
import matplotlib.pyplot as plt
import pandas as pd
import re
import networkx.algorithms.community as nxcom
import random
import networkx as nx

def create_centrality_df(centrality_dict,column_name,df_init):
    df_centrality = pd.DataFrame.from_dict(centrality_dict, orient='index')
    df_centrality.columns=[column_name]
    df_centrality["Top_"+column_name.split()[-1]] = (df_centrality[column_name] >= df_centrality[column_name].nlargest(8).min()).astype(int)
    df_fin_centrality = pd.concat([df_init,df_centrality], axis=1)
    return df_fin_centrality

def df_final():
    edges = pd.read_csv('data\\ter\\edges.csv')
    nodes = pd.read_csv('data\\ter\\nodes.csv')
    nodes= nodes.rename({'# index': 'index',
                        ' id': 'id', 
                        ' name': 'name', 
                        ' group': 'group', 
                        ' _pos': 'pos'}, axis='columns')
    nodes['pos'] = nodes['pos'].apply(lambda s: tuple([float(re.search(r'\d+\.\d+', part).group()) for part in s.split(',')]))
    def separate_row(row):
        row['x'], row['y'] = row['pos']
        return row
    nodes = nodes.apply(separate_row, axis=1).assign(pos=nodes['pos'])
    # Créer un graphique vide
    G = nx.Graph()
    for index, row in edges.iterrows():
        G.add_edge(row['# source'], row[' target'])
    # Ajouter les attributs de nœud au graphique
    nx.set_node_attributes(G, nodes[['index', 'id', 'name', 'group', 'pos']].set_index('index').to_dict(orient='index'))
    
    cen_deg = nx.degree_centrality(G)
    df_cen_deg = create_centrality_df(cen_deg,"La centralité de degré",nodes)

    cen_pro = nx.closeness_centrality(G)
    df_cen_pro = create_centrality_df(cen_pro,"La centralité de proximité",df_cen_deg)

    cen_int = nx.betweenness_centrality(G, normalized=False)
    df_cen_int = create_centrality_df(cen_int,"La centralité de intermédiaire",df_cen_pro)

    cen_eig = nx.eigenvector_centrality(G)
    df_cen_eig = create_centrality_df(cen_eig,"La centralité vecteur propre",df_cen_int)
    
    # Algorithme de Girvan Newman
    gine = nxcom.girvan_newman(G)
    com_gine = next(gine)
    df_com_gine = []
    for i, my_set in enumerate(com_gine):
        df = pd.DataFrame({'index':list(my_set)})
        df['group_gine'] = i
        df_com_gine.append(df)
        
    final_df_gine = pd.concat(df_com_gine, ignore_index=True)
    df_com_gine=pd.merge(df_cen_eig, final_df_gine, left_on='index', right_on='index', how='inner')
        
    # Algorithme de Clauset, Newman Moore
    com_cmm = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
    df_com_cmm = []
    for i, my_set in enumerate(com_cmm):
        df = pd.DataFrame({'index':list(my_set)})
        df['group_cmm'] = i
        df_com_cmm.append(df)
        
    final_df_cmm = pd.concat(df_com_cmm, ignore_index=True)
    df_com_cmm= pd.merge(df_com_gine, final_df_cmm, left_on='index', right_on='index', how='inner')
    
    # Algorithme de Louvain
    com_louvain = sorted(nxcom.louvain_communities(G, seed=123))
    df_com_louvain = []
    for i, my_set in enumerate(com_louvain):
        df = pd.DataFrame({'index':list(my_set)})
        df['group_louvain'] = i
        df_com_louvain.append(df)
        
    final_df_louvain = pd.concat(df_com_louvain, ignore_index=True)
    df_com_louvain = pd.merge(df_com_cmm, final_df_louvain, left_on='index', right_on='index', how='inner')
    
    
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
    return df_com_louvain, df_mes

if __name__ == '__main__':
    df_final,df_mes= df_final()
    print( df_mes)