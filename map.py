import folium

academias = ['Academia Top Fitness', 'Foco', 'Prime']
coordenadas = [
    [-5.663713623879048, -37.80741733339656],
    [-5.623916502429825, -37.786758022414936],
    [-5.606476308610599, -37.8066211657921]
]

mapa = folium.Map(location=[-5.6615146308316975, -37.797283767920206], zoom_start=13)
for nome, coord in zip(academias, coordenadas):
    folium.Marker(location=coord, popup=nome).add_to(mapa)