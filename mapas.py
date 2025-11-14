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
        name='Black'
    ).add_to(mapa_local)

    folium.LayerControl().add_to(mapa_local)
    LocateControl(auto_start=True, drawmarker=True).add_to(mapa_local)
    Terminator().add_to(mapa_local)

    # ► Mostrar TODOS
    if opcao in (None, "", "0"):
        for tipo in TIPOS:
            adicionar_marcadores(mapa_local, tipo)

    # ► Mostrar apenas um tipo
    elif opcao in TIPOS:
        adicionar_marcadores(mapa_local, opcao)

    return mapa_local._repr_html_()
