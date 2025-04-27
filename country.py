import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import pycountry

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



# Agora pode fazer o merge
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

# Verifique se houve algum país que não foi mapeado corretamente no merge


merged.to_excel('data/merged_homicides.xlsx', index=False)
print(list(merged['homicide_rate']))
# 6. Cores baseadas no valor de homicídios
brasil_value = merged.loc[merged["NAME_EN"] == 'Brazil', 'homicide_rate'].values[0] if not merged.loc[merged["NAME_EN"] == 'Brazil', 'homicide_rate'].empty else None
print(brasil_value)

def define_cor(row):
    if pd.isna(row['homicide_rate']):
        return 'lightgrey'
    elif row['NAME_EN'] == 'Brazil':
        return 'red'
    elif row['homicide_rate'] <= brasil_value:
        return 'blue'
    else:
        return 'lightgrey'

merged['color'] = merged.apply(define_cor, axis=1)

# 7. Recalcular a soma apenas dos azuis
azuis = merged[(merged['color'] == 'blue')]
soma_azuis = azuis['homicide_rate'].sum()

# 8. Plotar
fig, ax = plt.subplots(figsize=(20, 12))
world.plot(ax=ax, color='lightgrey', edgecolor='black')
merged.plot(ax=ax, color=merged['color'], edgecolor='black', linewidth=0.5)

# 9. Texto
ax.text(-130, -30,
        f"Brazil had more total homicides\nthan all the blue countries combined\n\n"
        f"Brazil: {int(brasil_value):,} homicides\n"
        f"Blue Countries: {int(soma_azuis):,} homicides",
        fontsize=14, color='black', bbox=dict(facecolor='white', alpha=0.7))

plt.axis('off')
plt.title("Homicídios no Mundo: Comparação com o Brasil", fontsize=18)
plt.savefig("homicidios_mundo.png", dpi=300, bbox_inches='tight')
