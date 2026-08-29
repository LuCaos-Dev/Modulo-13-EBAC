import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Carregar Dados
df = pd.read_csv("MODULO7_PROJETOFINAL_BASE_SUPERMERCADO.csv", delimiter=';')

# 2. Média e Mediana
stats_preco = df.groupby('Categoria')['Preco_Normal'].agg(['mean', 'median', 'std']).reset_index()

# 3. Gráfico Interativo: Média vs Mediana
fig1 = px.bar(
    stats_preco, 
    x='Categoria', 
    y=['mean', 'median'], 
    barmode='group',
    title='Média vs Mediana de Preço Normal por Categoria',
    labels={'value': 'Preço', 'variable': 'Métrica'}
)
fig1.show()

# 4. Boxplot Interativo para a Categoria de Maior Desvio (Lácteos)
df_lacteos = df[df['Categoria'] == 'lacteos']
fig2 = px.box(
    df_lacteos, 
    y='Preco_Normal', 
    points='outliers',
    title='Distribuição de Preço Normal - Lácteos (Maior Desvio Padrão)'
)
fig2.show()

# 5. Mapa Interativo (Treemap) por Categoria, Marca e Média de Desconto
df_treemap = df.groupby(['Categoria', 'Marca']).agg(
    Media_Desconto=('Desconto', 'mean'),
    Qtd_Produtos=('title', 'count')
).reset_index()

fig3 = px.treemap(
    df_treemap,
    path=['Categoria', 'Marca'],
    values='Qtd_Produtos',
    color='Media_Desconto',
    color_continuous_scale='Viridis',
    title='Mapa Interativo: Distribuição por Categoria, Marca e Desconto Médio'
)
fig3.show()
