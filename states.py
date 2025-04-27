import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from geobr import read_state

# 1. Carregar shapefile dos estados brasileiros via geobr
estados = read_state()

# 2. Tabela de homicídios (com siglas)
dados = {
    "estado": [
        "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
        "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
        "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro",
        "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina",
        "São Paulo", "Sergipe", "Tocantins"
    ],
    "taxa": [
        34.5, 42.2, 35.1, 39.8, 45.3, 38.9, 18.2, 20.5, 26.7, 29.9, 27.4, 24.3,
        15.1, 41.7, 32.5, 19.4, 37.6, 31.1, 19.9, 36.2, 17.3, 28.5, 33.0, 10.9,
        9.8, 36.0, 26.5
    ],
    "uf": [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF",
        "ES", "GO", "MA", "MT", "MS",
        "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
        "RN", "RS", "RO", "RR", "SC",
        "SP", "SE", "TO"
    ]
}

df_homi = pd.DataFrame(dados)

# 3. Merge dos dados com o shape usando sigla
mapa = estados.merge(df_homi, left_on="abbrev_state", right_on="uf", how="left")

# 4. Plotando o mapa
fig, ax = plt.subplots(figsize=(10, 10))
mapa.plot(
    column="taxa",
    cmap="Reds",
    linewidth=0.8,
    ax=ax,
    edgecolor="0.8",
    legend=True,
    legend_kwds={'label': "Homicide rate per 100k inhabitants", 'orientation': "vertical"}
)

plt.title("Taxa de Homicídios no Brasil por Estado (2021)", fontsize=15)
plt.axis('off')
plt.savefig("homicidios_brasil.png", dpi=300, bbox_inches='tight')
