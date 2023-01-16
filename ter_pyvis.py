from pyvis.network import Network
import pandas as pd
import re
# Importation edges
edges = pd.read_csv('data\\ter\\edges.csv')

def gnet_pyvis(df_final,couleur):
    
    color_map = {0: "#ff4d4d", 1: "#33cc33", 2: "#0066cc", 3: "#990000", 4: '#F8C471', 5: 'DarkSlateGray'}
    df_final['color'] = df_final[couleur].map(color_map)
       
    # G = Network( filter_menu=True)
    G = Network(height='1000px', width='100%', bgcolor='#E0E0E0', font_color='black')
    G.add_nodes(df_final["index"],
                x = df_final["x"],
                y = df_final["y"],
                label = df_final["name"],
                color = df_final["color"])

    sources = edges['# source']
    targets = edges[' target']

    edge_data = zip(sources, targets)

    for e in edge_data:
                    src = e[0]
                    dst = e[1]
                    G.add_edge(src, dst)
    G.set_options("""
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
    return(G)
#    G.show("basic.html")

if __name__ == '__main__':
    df_final,df_mes = df_final()
    #print(df_final)
    G = gnet_pyvis(df_final,"group")
    G.show("basic1.html")