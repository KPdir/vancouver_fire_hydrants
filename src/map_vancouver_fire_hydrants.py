import json
import folium
import numpy as np 
import pandas as pd 

def map_hydrant_data(relpath):
    # Load data
    df = pd.read_csv(relpath, sep=';')

    # Custom function Get Type, Latitude, Longitude
    def return_coordinates(x):
        d = json.loads(x)
        lst = [d['type']]+ d['coordinates']
        return pd.Series(lst, index=['type','lon','lat'])

    # Add processed data
    df = pd.concat([df, df['Geom'].apply(return_coordinates)], axis=1)
    df['color'] = df['COLOR'].fillna('NA')

    # Color map for hydrants
    colors= {'Blue':'blue', 
             'Green':'green',        
             'Yellow':'#ffff00',         
             'Red':'red',    
             'NA':'gray',       
             'White':'white'}


    # Use folium to display hydrants on the map
    van_cluster = folium.Map(location=[49.28721476882593,-123.11269938372442],zoom_start=16)

    from folium import plugins
    cluster = plugins.MarkerCluster().add_to(van_cluster)

    for idx, location in enumerate(zip(df.lat, df.lon)): 
        popup_html = '<p>ID: {ID}<br>STATUS: {STATUS}</p>'.format(**dict(df.loc[idx, ['ID','STATUS']]))
        popup_iframe = folium.IFrame(html= popup_html, width=200, height=50)

        if (idx < 50):
            popup = folium.Popup(popup_iframe, parse_html=True, show=True)
        else:
            popup = folium.Popup(popup_iframe, parse_html=True)

        folium.CircleMarker(
                        location,
                        radius=6,
                        color=colors[df['color'][idx] ],
                        fill=True,
                        fill_color=colors[df['color'][idx]],
                        fill_opacity=0.4,
                        popup=popup
                ).add_to(cluster)

    return van_cluster