import streamlit as st
import streamlit.components.v1 as components
import streamlit
import pandas as pd
import numpy as np
from pyvis.network import Network
from ter_networkx import df_final
from ter_pyvis import gnet_pyvis
from random_pyvis import Gnet_pyvis_random

# Set header title
st.set_page_config(layout="wide")
st.title(' Analyse social network and random graph ')

base = st.get_option("theme.base")
primary_color = st.get_option("theme.primaryColor")
base = "dark"
primaryColor = "#35b6dc"

# Load HTML file in HTML component for display on Streamlit page
col1, col2 = st.columns([0.2, 0.8])
with col1:    
    data_list = ['Mapping Networks of Terrorist Cells',
                 'Random Graph with communities']
    data = st.selectbox("Select data:", data_list)
    
    com_list = ['Communities: Girvan Newman',
                'Communities: Clauset, Newman Moore',
                'Communities: Louvain']
    random_model_list =['Erdős–Rényi model',
                        'Watts and Strogatz model',
                        'Caveman model',
                        'Caveman connected model',
                        'Caveman relaxed model']
    com_cen_list = ['Communities: AF11, AF175, AF77, AF93, other ',
                    'Communities: Girvan Newman',
                    'Communities: Clauset, Newman Moore',
                    'Communities: Louvain',
                    'Centrality : Betweenness Centrality',
                    'Centrality : Degree Centrality',
                    'Centrality : Closeness Centrality',
                    'Centrality : Eigenvector Centrality']
    algo =[ 'gine','gmc','louvain']
    if data == data_list[0] :
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
        df_final,df_mes = df_final()
        G = scripts.gnet_pyvis(df_final, df_com)
        st.subheader("Network Properties")
        st.write(df_mes.T.rename(columns={0: "Properties"}))
    if data == data_list[1]:
        random_model = st.selectbox("Select model:", random_model_list)
        com = st.selectbox("Select communities or centrality:", com_list)
        if random_model == random_model_list[0] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random( algo[0],'poisson') 
        elif random_model == random_model_list[0] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random( algo[1],'poisson') 
        elif random_model == random_model_list[0] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random( algo[2],'poisson') 
        elif random_model == random_model_list[1] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random( algo[0],'wa_st') 
        elif random_model == random_model_list[1] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random( algo[1],'wa_st') 
        elif random_model == random_model_list[1] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random( algo[2],'wa_st')             
        elif random_model == random_model_list[2] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random( algo[0],'caveman') 
        elif random_model == random_model_list[2] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random( algo[1],'caveman') 
        elif random_model == random_model_list[2] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random( algo[2],'caveman') 
        elif random_model == random_model_list[3] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random( algo[0],'caveman_con') 
        elif random_model == random_model_list[3] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random( algo[1],'caveman_con') 
        elif random_model == random_model_list[3] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random( algo[2],'caveman_con') 
        elif random_model == random_model_list[4] and com == com_list[0]:
            G, df_mes = Gnet_pyvis_random( algo[0],'caveman_re') 
        elif random_model == random_model_list[4] and com == com_list[1]:
            G, df_mes = Gnet_pyvis_random( algo[1],'caveman_re') 
        elif random_model == random_model_list[4] and com == com_list[2]:
            G, df_mes = Gnet_pyvis_random( algo[2],'caveman_re') 
        st.write(df_mes.T.rename(columns={0: "Properties"}))
with col2:
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        G.save_graph('ouput\\pyvis_graph.html')
        HtmlFile = open('output\\pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        G.save_graph('output\\pyvis_graph.html')
        HtmlFile = open('output\\pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height = 1020)
        

    
