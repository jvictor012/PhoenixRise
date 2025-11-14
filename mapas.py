import folium
from folium.plugins import LocateControl, Terminator
from flask import request
from database import executar_comandos
import branca

# ================================
# BUSCA DOS DADOS
# ================================
coordenadas_academias = executar_comandos("SELECT latitude, longitude, nome FROM academias")
coordenadas_quadras = executar_comandos("SELECT latitude, longitude, nome FROM quadras")
coordenadas_crossfits = executar_comandos("SELECT latitude, longitude, nome FROM crossfits")
coordenadas_lojas = executar_comandos("SELECT latitude, longitude, nome FROM lojas")
coordenadas_academias_livres = executar_comandos("SELECT latitude, longitude, nome FROM academias_livres")

# ================================
# DICIONÁRIO DOS TIPOS
# ================================
TIPOS = {
    "1": {
        "dados": coordenadas_academias,
        "icon": "dumbbell",
        "prefix": "fa",
        "color": "orange"
    },
    "2": {
        "dados": coordenadas_academias_livres,
        "icon": "dumbbell",
        "prefix": "fa",
        "color": "blue"
    },
    "3": {
        "dados": coordenadas_quadras,
        "icon": "glyphicon-fire",
        "prefix": "glyphicon",
        "color": "green"
    },
    "4": {
        "dados": coordenadas_crossfits,
        "icon": "glyphicon glyphicon-flash",
        "prefix": "glyphicon",
        "color": "black"
    },
    "5": {
        "dados": coordenadas_lojas,
        "icon": "shopping-cart",
        "prefix": "fa",
        "color": "pink"
    }
}

# ================================
# FUNÇÃO AUXILIAR
# ================================
def adicionar_marcadores(mapa, tipo):
    info = TIPOS[tipo]

    for lat, lon, nome in info["dados"]:
        folium.Marker(
            location=[lat, lon],
            popup=nome,
            icon=folium.Icon(
                icon=info["icon"],
                prefix=info["prefix"],
                color=info["color"]
            )
        ).add_to(mapa)


# ================================
# FUNÇÃO PRINCIPAL
# ================================
def gerar_mapa(opcao):
    mapa_local = folium.Map(
        location=[-5.6615146308316975, -37.797283767920206],
        zoom_start=10,
        width='100vw',
        height='100vw'
    )
    folium.TileLayer(
        tiles='https://tile.jawg.io/jawg-dark/{z}/{x}/{y}{r}.png?access-token=ibuk3ZTj3Ebly6X9wlX6W9Hjql0bxNrZ3eXvdmIvQFXeAjPZtX00h3J6kRJwQVWG',
        attr='<a href="https://jawg.io" target="_blank">&copy; Jawg Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        name='Black').add_to(mapa_local)

    folium.LayerControl().add_to(mapa_local)

    LocateControl(auto_start=True, drawmarker=True, markerStyle = dict(classname="leaflet-control-locate-marker")).add_to(mapa_local)
    Terminator().add_to(mapa_local)
    if opcao in (None, '', '0'):
        for academia in coordenadas_academias:
            lat = academia[0]
            lon = academia[1]
            nome = academia[2]
            coord= [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='dumbbell', prefix='fa', color='orange')  
            ).add_to(mapa_local)
        for academia_livre in coordenadas_academias_livres:
            lat = academia_livre[0]
            lon = academia_livre[1]
            nome = academia_livre[2]
            coord = [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='dumbbell', prefix='fa', color='blue')  
            ).add_to(mapa_local)
        for quadra in coordenadas_quadras:
            lat = quadra[0]
            lon = quadra[1]
            nome = quadra[2]
            coord= [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon_image='\static\icons\person-arms-up.svg',color='green', icon_color='white')  
            ).add_to(mapa_local)
        for crosfits in coordenadas_crossfits:
            lat = crosfits[0]
            lon = crosfits[1]
            nome = crosfits[2]
            coord = [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='glyphicon glyphicon-flash', prefix='glyphicon', color='black', icon_color='white')  
            ).add_to(mapa_local)
        for lojas in coordenadas_lojas:
            lat = lojas[0]
            lon = lojas[1]
            nome = lojas[2]
            coord= [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='shopping-cart', prefix='fa', color='pink')  
            ).add_to(mapa_local)
        
        
    if opcao == '1':
        for academia in coordenadas_academias:
            lat = academia[0]
            lon = academia[1]
            nome = academia[2]
            coord = [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='dumbbell', prefix='fa', color='orange')  
            ).add_to(mapa_local)

    if opcao == '2':
        for academia_livre in coordenadas_academias_livres:
            lat = academia_livre[0]
            lon = academia_livre[1]
            nome = academia_livre[2]
            coord = [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='dumbbell', prefix='fa', color='blue')  
            ).add_to(mapa_local)

    if opcao == '3':
        for quadra in coordenadas_quadras:
            lat = quadra[0]
            lon = quadra[1]
            nome = quadra[2]
            coord= [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='glyphicon glyphicon-fire',color='green', icon_color='white')  
            ).add_to(mapa_local)
    if opcao == '4':
         for crosfits in coordenadas_crossfits:
            lat = crosfits[0]
            lon = crosfits[1]
            nome = crosfits[2]
            coord = [lat, lon]
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='glyphicon glyphicon-flash', prefix='glyphicon', color='black', icon_color='white') 
            ).add_to(mapa_local)

    return mapa_local._repr_html_()
