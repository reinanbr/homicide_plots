import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# 1. Carregar o shapefile mundial
world = gpd.read_file("ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

# 3. Corrigir possíveis nomes errados
correcoes = {
    'Russia': 'Russian Federation',
    'United States': 'United States of America',
    'Venezuela': 'Venezuela, Bolivarian Republic of',
    'South Korea': 'Korea, Republic of',
    'North Korea': 'Korea, Democratic People\'s Republic of',
    'Vietnam': 'Viet Nam',
    'Syria': 'Syrian Arab Republic',
    'Iran': 'Iran, Islamic Republic of',
    'Bolivia': 'Bolivia, Plurinational State of',
    'Tanzania': 'Tanzania, United Republic of',
    'Laos': 'Lao People\'s Democratic Republic',
    'Moldova': 'Moldova, Republic of',
    'Ivory Coast': 'Côte d\'Ivoire',
    'Czech Republic': 'Czechia',
    'Swaziland': 'Eswatini'
}

# Criar um DataFrame com os dados fornecidos
dados_homicidios = pd.DataFrame({
    'country': ['Brazil', 'United States', 'Canada', 'Mexico', 'Colombia', 'South Africa', 'Russia', 'India', 'China', 'Japan', 'Australia', 'Germany', 'France', 'United Kingdom', 'Argentina', 'Venezuela'],
    'homicide_rate': [27.4, 5.0, 1.8, 29.1, 25.3, 36.4, 8.2, 3.1, 0.5, 0.3, 1.0, 1.0, 1.2, 1.0, 5.3, 56.3]
})

# Corrigir possíveis nomes errados
dados_homicidios['country_corrigido'] = dados_homicidios['country'].replace(correcoes)

# Fazer o merge com o shapefile mundial
merged = world.merge(dados_homicidios[['country_corrigido', 'homicide_rate']], 
                     left_on='NAME_EN', right_on='country_corrigido', how='left')

# Adicionar a coluna 'taxa' para ser usada no mapa
merged['taxa'] = merged['homicide_rate']

# 6. Criar o gráfico
fig, ax = plt.subplots(figsize=(20, 12))

# Plotando com map.plot e definindo cores personalizadas
merged.plot(
    column="taxa",
    cmap="Reds",
    linewidth=0.8,
    ax=ax,
    edgecolor="0.8",
    legend=True,
    legend_kwds={'label': "Homicide rate per 100k inhabitants", 'orientation': "vertical"},
    missing_kwds={
        "color": "lightgrey",  # Definir a cor dos países sem dados
        "label": "No data",
        "edgecolor": "0.8",
        "linewidth": 0.8
    }
)

# Texto sobre o Brasil e países azuis
brasil_value = merged.loc[merged["NAME_EN"] == 'Brazil', 'homicide_rate'].values[0] if not merged.loc[merged["NAME_EN"] == 'Brazil', 'homicide_rate'].empty else None
azuis = merged[(merged['taxa'] <= brasil_value)]
soma_azuis = azuis['homicide_rate'].sum()

# Movendo o texto para abaixo do mapa

# Texto sobre a fonte dos dados e criador, abaixo do mapa
ax.text(-180, -150,
        "Data Source: World Bank, UNODC\n"
        "Creator: @reinanbr_ | Data Scientist\n"
        "Visualization by: @reinanbr_",
        fontsize=12, color='black', ha='left', bbox=dict(facecolor='white', alpha=0.7))

plt.axis('off')
plt.title("Homicídios no Mundo: Comparação com o Brasil", fontsize=18)
plt.savefig("homicidios_mundo_com_colormap_e_coresfaltantes_com_texto.png", dpi=300, bbox_inches='tight')
