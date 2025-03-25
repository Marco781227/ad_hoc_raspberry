import pandas as pd
import folium

#charger les data
df = pd.read_csv("gps_data.csv")

#Prendre la dernière position + centrer carte
last_point = df.iloc[-1]
map_center = [last_point['latitude'], last_point['longitude']]
carte = folium.Map(location=map_center, zoom_start=10)

#Ajout des points sur la map
for index, row in df.iterrows():
	folium.CircleMarker(
		location = [row['latitude'], row['longitude']],
		radius = 5,
		popup = row['timestamp'],
		color = 'blue',
		fill = True,
		fill_color = 'blue'
	).add_to(carte)
		
#sauvegarde dans fichier HTML
carte.save("gps_map.html")
print("carte générée OK")
