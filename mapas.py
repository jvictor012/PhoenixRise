import folium

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
    mapa_local = folium.Map(location=[-5.6615146308316975, -37.797283767920206], zoom_start=13)
    if opcao == 'academia':
        for nome, coord in zip(academias, coordenadas_academias):
            folium.Marker(location=coord, popup=nome).add_to(mapa_local)
    elif opcao == 'lojas':
        for nome, coord in zip(lojas, coordenadas_lojas):
            folium.Marker(location=coord, popup=nome, icon=folium.Icon(color='green')).add_to(mapa_local)
    return mapa_local._repr_html_()




