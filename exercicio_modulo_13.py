# ============================================================
# MÓDULO 13 - PROJETO
# Fundamentos da Descoberta de Dados
# ============================================================

import pandas as pd
import plotly.express as px
from IPython.display import display, Markdown


# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

df = pd.read_csv(
    "MODULO7_PROJETOFINAL_BASE_SUPERMERCADO.csv",
    delimiter=";"
)

print(f"Quantidade de registros: {len(df)}")
print(f"Quantidade de categorias: {df['Categoria'].nunique()}")
print(f"Quantidade de marcas: {df['Marca'].nunique()}")

display(df.head())


# ============================================================
# 2. MÉDIA, MEDIANA E DESVIO PADRÃO DO PREÇO NORMAL
#    POR CATEGORIA
# ============================================================

stats_preco = (
    df.groupby("Categoria")["Preco_Normal"]
    .agg(
        Media="mean",
        Mediana="median",
        Desvio_Padrao="std"
    )
    .reset_index()
)

# Ordenação por desvio padrão, do maior para o menor
stats_preco = (
    stats_preco
    .sort_values(
        by="Desvio_Padrao",
        ascending=False
    )
    .reset_index(drop=True)
)

display(stats_preco)


# ============================================================
# 3. COMPARAÇÃO ENTRE MÉDIA E MEDIANA
# ============================================================

stats_preco["Comparacao"] = stats_preco.apply(
    lambda linha:
        "Média > Mediana"
        if linha["Media"] > linha["Mediana"]
        else (
            "Média < Mediana"
            if linha["Media"] < linha["Mediana"]
            else "Média = Mediana"
        ),
    axis=1
)

categorias_media_maior = stats_preco.loc[
    stats_preco["Media"] > stats_preco["Mediana"],
    "Categoria"
].tolist()

categorias_media_menor = stats_preco.loc[
    stats_preco["Media"] < stats_preco["Mediana"],
    "Categoria"
].tolist()

categorias_media_igual = stats_preco.loc[
    stats_preco["Media"] == stats_preco["Mediana"],
    "Categoria"
].tolist()


# ============================================================
# 4. GRÁFICO - MÉDIA VS. MEDIANA
# ============================================================

fig1 = px.bar(
    stats_preco.sort_values("Categoria"),
    x="Categoria",
    y=["Media", "Mediana"],
    barmode="group",
    title="Média vs. Mediana do Preço Normal por Categoria",
    labels={
        "Categoria": "Categoria",
        "value": "Preço Normal",
        "variable": "Métrica"
    }
)

fig1.update_layout(
    xaxis_title="Categoria",
    yaxis_title="Preço Normal",
    legend_title="Métrica",
    template="plotly_white"
)

fig1.show()


# ============================================================
# 5. ANÁLISE DA MÉDIA VS. MEDIANA
# ============================================================

texto_media_mediana = """
### Análise da média e mediana

A comparação entre a média e a mediana permite observar diferenças
na distribuição dos preços normais entre as categorias.
"""

if categorias_media_maior:
    texto_media_mediana += (
        "\n**Categorias em que a média é superior à mediana:** "
        + ", ".join(categorias_media_maior)
        + ".\n"
    )

if categorias_media_menor:
    texto_media_mediana += (
        "\n**Categorias em que a média é inferior à mediana:** "
        + ", ".join(categorias_media_menor)
        + ".\n"
    )

if categorias_media_igual:
    texto_media_mediana += (
        "\n**Categorias em que média e mediana são iguais:** "
        + ", ".join(categorias_media_igual)
        + ".\n"
    )

texto_media_mediana += """
\nQuando a média é superior à mediana, isso sugere que valores mais
elevados estão influenciando a média, indicando possível assimetria
positiva na distribuição.

Quando a média é inferior à mediana, isso sugere maior influência de
valores menores, indicando possível assimetria negativa.

A relação entre média e mediana deve ser interpretada em conjunto
com a dispersão dos dados e com o boxplot.
"""

display(Markdown(texto_media_mediana))


# ============================================================
# 6. IDENTIFICAÇÃO DA CATEGORIA COM MAIOR DESVIO PADRÃO
# ============================================================

categoria_maior_desvio = stats_preco.loc[
    stats_preco["Desvio_Padrao"].idxmax(),
    "Categoria"
]

maior_desvio = stats_preco.loc[
    stats_preco["Desvio_Padrao"].idxmax()
]

print("Categoria com maior desvio padrão:")
print(categoria_maior_desvio)

print(f"\nMédia: {maior_desvio['Media']:.2f}")
print(f"Mediana: {maior_desvio['Mediana']:.2f}")
print(f"Desvio padrão: {maior_desvio['Desvio_Padrao']:.2f}")


# ============================================================
# 7. ANÁLISE DA CATEGORIA COM MAIOR DESVIO PADRÃO
# ============================================================

if maior_desvio["Media"] > maior_desvio["Mediana"]:

    comportamento_maior_desvio = (
        "A média é superior à mediana, sugerindo que valores mais "
        "elevados estão influenciando a média e indicando possível "
        "assimetria positiva na distribuição."
    )

elif maior_desvio["Media"] < maior_desvio["Mediana"]:

    comportamento_maior_desvio = (
        "A média é inferior à mediana, sugerindo que valores menores "
        "estão influenciando a média e indicando possível assimetria "
        "negativa na distribuição."
    )

else:

    comportamento_maior_desvio = (
        "A média e a mediana apresentam o mesmo valor, indicando que "
        "não há diferença entre essas duas medidas de tendência central."
    )


texto_maior_desvio = f"""
### Análise da categoria com maior desvio padrão

A categoria que apresentou o maior desvio padrão foi
**{categoria_maior_desvio}**.

- **Média:** {maior_desvio['Media']:.2f}
- **Mediana:** {maior_desvio['Mediana']:.2f}
- **Desvio padrão:** {maior_desvio['Desvio_Padrao']:.2f}

{comportamento_maior_desvio}

O maior desvio padrão indica que essa categoria apresenta maior
dispersão dos preços normais em relação à média, quando comparada
às demais categorias.
"""

display(Markdown(texto_maior_desvio))


# ============================================================
# 8. BOXPLOT DA CATEGORIA COM MAIOR DESVIO PADRÃO
# ============================================================

df_maior_desvio = df[
    df["Categoria"] == categoria_maior_desvio
].copy()

fig2 = px.box(
    df_maior_desvio,
    y="Preco_Normal",
    points="outliers",
    title=(
        f"Distribuição do Preço Normal - "
        f"{categoria_maior_desvio}"
    ),
    labels={
        "Preco_Normal": "Preço Normal"
    }
)

fig2.update_layout(
    yaxis_title="Preço Normal",
    xaxis_title="",
    template="plotly_white"
)

fig2.show()


# ============================================================
# 9. IDENTIFICAÇÃO QUANTITATIVA DOS OUTLIERS
#    MÉTODO DO INTERVALO INTERQUARTIL (IQR)
# ============================================================

Q1 = df_maior_desvio["Preco_Normal"].quantile(0.25)
Q3 = df_maior_desvio["Preco_Normal"].quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df_maior_desvio[
    (df_maior_desvio["Preco_Normal"] < limite_inferior)
    |
    (df_maior_desvio["Preco_Normal"] > limite_superior)
].copy()

print("ANÁLISE DOS OUTLIERS")
print("--------------------")
print(f"Q1: {Q1:.2f}")
print(f"Q3: {Q3:.2f}")
print(f"IQR: {IQR:.2f}")
print(f"Limite inferior: {limite_inferior:.2f}")
print(f"Limite superior: {limite_superior:.2f}")
print(f"Quantidade de outliers: {len(outliers)}")


# ============================================================
# 10. LISTAGEM DOS OUTLIERS
# ============================================================

if len(outliers) > 0:

    print("\nProdutos identificados como outliers:")

    colunas_outliers = [
        "title",
        "Marca",
        "Preco_Normal",
        "Categoria"
    ]

    display(
        outliers[
            colunas_outliers
        ].sort_values(
            "Preco_Normal",
            ascending=False
        )
    )

else:

    print(
        "\nNão foram identificados outliers pelo método do IQR."
    )


# ============================================================
# 11. INTERPRETAÇÃO DO BOXPLOT
# ============================================================

if len(outliers) > 0:

    conclusao_outliers = (
        f"Foram identificados **{len(outliers)} outliers** pelo "
        "método do intervalo interquartil (IQR). Esses valores "
        "estão fora dos limites considerados esperados para a "
        "distribuição e podem contribuir para o aumento da dispersão "
        "observada."
    )

else:

    conclusao_outliers = (
        "Não foram identificados outliers pelo método do intervalo "
        "interquartil (IQR)."
    )


texto_boxplot = f"""
### Análise do boxplot

O boxplot apresenta a distribuição do **Preço Normal** da categoria
**{categoria_maior_desvio}**, que foi a categoria com maior desvio padrão.

O intervalo entre o primeiro e o terceiro quartil representa a
concentração central dos dados. A posição da mediana dentro da caixa
permite observar a distribuição dos valores, enquanto os pontos
localizados fora dos limites do boxplot representam possíveis valores
discrepantes.

{conclusao_outliers}

Portanto, o boxplot complementa a análise do desvio padrão,
permitindo visualizar a dispersão e os valores discrepantes presentes
na categoria analisada.
"""

display(Markdown(texto_boxplot))


# ============================================================
# 12. MÉDIA DE DESCONTO POR CATEGORIA
# ============================================================

media_desconto_categoria = (
    df.groupby("Categoria")["Desconto"]
    .mean()
    .sort_values(ascending=False)
    .reset_index(name="Media_Desconto")
)

display(media_desconto_categoria)


# ============================================================
# 13. GRÁFICO DE BARRAS - MÉDIA DE DESCONTO POR CATEGORIA
# ============================================================

fig3 = px.bar(
    media_desconto_categoria,
    x="Categoria",
    y="Media_Desconto",
    text="Media_Desconto",
    title="Média de Desconto por Categoria",
    labels={
        "Categoria": "Categoria",
        "Media_Desconto": "Média de Desconto"
    }
)

fig3.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig3.update_layout(
    xaxis_title="Categoria",
    yaxis_title="Média de Desconto",
    template="plotly_white"
)

fig3.show()


# ============================================================
# 14. ANÁLISE DA MÉDIA DE DESCONTO
# ============================================================

categoria_maior_desconto = media_desconto_categoria.iloc[0]

categoria_menor_desconto = media_desconto_categoria.iloc[-1]

texto_desconto = f"""
### Análise da média de desconto por categoria

A categoria com a **maior média de desconto** foi
**{categoria_maior_desconto['Categoria']}**, com média de
**{categoria_maior_desconto['Media_Desconto']:.2f}**.

Já a categoria com a **menor média de desconto** foi
**{categoria_menor_desconto['Categoria']}**, com média de
**{categoria_menor_desconto['Media_Desconto']:.2f}**.

O gráfico permite comparar diretamente o nível médio de desconto
praticado entre as diferentes categorias de produtos.
"""

display(Markdown(texto_desconto))


# ============================================================
# 15. TREEMAP
#     CATEGORIA + MARCA + MÉDIA DE DESCONTO
# ============================================================

df_treemap = (
    df.groupby(["Categoria", "Marca"])
    .agg(
        Media_Desconto=("Desconto", "mean"),
        Qtd_Produtos=("title", "count")
    )
    .reset_index()
)


# ============================================================
# 16. MAPA INTERATIVO - TREEMAP
# ============================================================

fig4 = px.treemap(
    df_treemap,
    path=["Categoria", "Marca"],
    values="Qtd_Produtos",
    color="Media_Desconto",
    color_continuous_scale="Viridis",
    title=(
        "Mapa Interativo por Categoria e Marca "
        "com Média de Desconto"
    ),
    labels={
        "Qtd_Produtos": "Quantidade de Produtos",
        "Media_Desconto": "Média de Desconto",
        "Categoria": "Categoria",
        "Marca": "Marca"
    }
)

fig4.update_layout(
    template="plotly_white"
)

fig4.show()


# ============================================================
# 17. SALVAR O TREEMAP COMO HTML
# ============================================================

fig4.write_html(
    "grafico4_mapa_interativo.html"
)

print(
    "\nTreemap salvo como: grafico4_mapa_interativo.html"
)
