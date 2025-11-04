import folium
from folium.plugins import LocateControl, Terminator
from flask import request


quadras = ['Quadra Poliesportiva', 'Quadra de esportes da Garilândia', 'Quadra do Bacural 1', 'Arena Hiper', 'Arena Morais', 'Ginásio de esportes de Apodi']
coordenadas_quadras = [
    [-5.632274690348239, -37.80171350910772],
    [-5.659308325813112, -37.788538498298166],
    [-5.664379714532668, -37.80992930851204],
    [-5.644477600704771, -37.80399807877793], 
    [-5.648769664778595, -37.791917409344826],
    [-5.661216703028881, -37.797571732595024]

]

academias = ['Academia Top Fitness', 'Foco Academia', 'Academia Prime Core','Soufit', 'Academia Perfomance']
coordenadas_academias = [
    [-5.663812521428317, -37.80741868034249],
    [-5.658043198588798, -37.79612277145106],
    [-5.65034687947221, -37.79995285916965],
    [-5.648767002876063, -37.79925649914765],
    [-5.665555680785641, -37.79491094724948]
]
lojas = ['Fit Closet Apodi', 'Sport Center', 'Meu suplemento','Prosup']
coordenadas_lojas = [
    [-5.664434892555351, -37.79916604047842],
    [-5.6638995267040935, -37.798567762811786],
    [-5.665122192856129, -37.79933227345832],
    [-5.653764880171134, -37.799500951946094]
]
def gerar_mapa(opcao):
    mapa_local = folium.Map(
        location=[-5.6615146308316975, -37.797283767920206],
        zoom_start=10,
        width='100vw',
        height='100vw'
    )
    LocateControl(auto_start=True, drawmarker=True, markerStyle = dict(classname="leaflet-control-locate-marker")).add_to(mapa_local)
    Terminator().add_to(mapa_local)
    if opcao in (None, '', '0'):
        for nome, coord in zip(academias, coordenadas_academias):
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='dumbbell', prefix='fa', color='orange')  
            ).add_to(mapa_local)
        for nome, coord in zip(lojas, coordenadas_lojas):
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='shopping-cart', prefix='fa', color='pink')  
            ).add_to(mapa_local)
        for nome, coord in zip(quadras, coordenadas_quadras):
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='shopping-cart', prefix='fa', color='pink')  
            ).add_to(mapa_local)
        
    if opcao == '1':
        for nome, coord in zip(academias, coordenadas_academias):
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='dumbbell', prefix='fa', color='orange')  
            ).add_to(mapa_local)

    if opcao == '2':
        for nome, coord in zip(quadras, coordenadas_quadras):
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='', prefix='fa', color='pink')  
            ).add_to(mapa_local)
    elif opcao == '4':
        for nome, coord in zip(lojas, coordenadas_lojas):
            folium.Marker(
                location=coord,
                popup=nome,
                icon=folium.Icon(icon='shopping-cart', prefix='fa', color='pink')  
            ).add_to(mapa_local)
    return mapa_local._repr_html_()




