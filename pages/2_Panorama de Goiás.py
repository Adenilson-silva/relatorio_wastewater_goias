import streamlit as st
import plotly.express as px
from src.db import (
    obter_volumes_anuais_goias, 
    obter_desempenho_municipios
)
from src.utils import (
    criar_cards, 
    titulo_relatorio, 
    formatar_numero_inteiro,
    formatar_numero_decimal
)

st.set_page_config(
    layout="centered"
)

df_volumes_anuais_goias = obter_volumes_anuais_goias().sort_values(by="Ano")
df_desempenho_municipios = obter_desempenho_municipios().sort_values(by="Ano", ascending=False)
anos = df_desempenho_municipios["Ano"].value_counts().index.tolist()

titulo_relatorio()
st.markdown(
    f"""
    <div style="
        padding: 2px;
        text-align: center;
        font-family: 'Cambria Math';">
        <p style="font-size:25px; font-weight: bold;">Panorama de Goiás (1992 - 2021)</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("")


df_long_volume = df_volumes_anuais_goias.melt(
    id_vars="Ano",
    value_vars=["Volume produzido (1000 m³)", "Volume coletado (1000 m³)", "Volume tratado (1000 m³)"],
    var_name="Tipo Volume",
    value_name="Volume"
)
fig_volume = px.line(
    df_long_volume,
    x="Ano",
    y="Volume",
    color="Tipo Volume",
    markers=True,
    title="Volumes de Esgotos Tratados, Coletados e Produzidos",
    width=1000,
    height=400,
    color_discrete_map={
        "Volume produzido (1000 m³)": "#A0522D",  
        "Volume coletado (1000 m³)": "#D3DC5A",   
        "Volume tratado (1000 m³)": "#5DADE2",    
    }
)
fig_volume.update_xaxes(
    type="category",
    tickmode="array",
    tickvals=df_long_volume["Ano"].unique(),
    tickangle=-45
)
df_long_volume["Volume_fmt"] = df_long_volume["Volume"].apply(formatar_numero_decimal)
fig_volume.update_yaxes(autorange=True)
fig_volume.update_traces(
    customdata=df_long_volume["Volume_fmt"],
    hovertemplate='Ano: %{x}<br>Volume (em 1000 m³): %{customdata}'
)
fig_volume.update_layout(
    legend_title_text="",
    yaxis_title="Volume (1000 m³)",
    xaxis_title="Ano",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)
st.plotly_chart(fig_volume, use_container_width=True)


df_long_relacao = df_volumes_anuais_goias.melt(
    id_vars="Ano",
    value_vars=["Relação coletado/produzido", 
                "Relação tratado/coletado", 
                "Relação tratado/produzido"],
    var_name="Tipo Relação",
    value_name="Relação"
)
fig_relacao = px.bar(
    df_long_relacao,
    x="Ano",
    y="Relação",
    color="Tipo Relação",
    barmode="group",
    title="Eficiência (Quantitativa) dos Serviços de Tratamento de Esgotos",
    width=1000,
    height=500,
    color_discrete_map={
        "Relação tratado/produzido": "#1F77B4",  
        "Relação tratado/coletado": "#2CA02C",   
        "Relação coletado/produzido": "#FF7F0E",    
    }
)
fig_relacao.update_xaxes(
    type="category", 
    tickmode="array",
    tickvals=df_long_relacao["Ano"].unique(),
    tickangle=-45
)
fig_relacao.update_yaxes(
    range=[0, 1.1],         
    tickformat=".0%"      
)
fig_relacao.update_traces(
    hovertemplate='Ano : %{x}<br>Percentual %{y:.2%}'
)
fig_relacao.update_layout(
    legend_title_text="",
    yaxis_title="Relação (%)",
    xaxis_title="Ano",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)
st.plotly_chart(fig_relacao, use_container_width=True)

ano_selecionados = st.multiselect(
        "Selecione o(s) Ano(s) de Referência",
        anos,
        anos[0]
    )
if len(ano_selecionados) < 1:
        st.warning("Selecione o(s) Ano(s) de Referência.")

for ano_selecionado in ano_selecionados:
    df_desempenho_municipios_filtrado_por_ano = df_desempenho_municipios[df_desempenho_municipios["Ano"] == ano_selecionado]
    df_desempenho_municipios_filtrado_por_ano_e_agregado = df_desempenho_municipios_filtrado_por_ano.groupby(by="Desempenho geral").size().reset_index(name="Quantidade de municípios").sort_values(by="Quantidade de municípios")
    total_populacao = df_desempenho_municipios_filtrado_por_ano["População total urbana"].sum()
    cards_linha2 = [
        {
            "titulo": f"População Total Urbana em {ano_selecionado}",
            "%cor": "#424242",              
            "valor": formatar_numero_inteiro(total_populacao),
            "bg": "#E0E0E0"                
        }
    ]
    criar_cards(cards_linha2, 1)
    fig_desempenho = px.bar(
        df_desempenho_municipios_filtrado_por_ano_e_agregado,
        x="Desempenho geral",
        y="Quantidade de municípios",
        text="Quantidade de municípios",
        category_orders={ 
            "Desempenho geral": ["Ótimo", "Bom", "Regular", "Ruim", "Indefinido"]
        },
        title=f"Desempenho (Quantitativo) dos Serviços de Tratamento de Esgotos no Estado de Goiás em {ano_selecionado}",
        width=300,
        height=500
    )
    fig_volume.update_yaxes(autorange=True)
    fig_desempenho.update_traces(
        hovertemplate='Desempenho: %{x}<br>Quantidade de Minicípios: %{y}',
        marker_color="#686868"
    )
    fig_desempenho.update_layout(
        legend_title_text="",
        yaxis_title="Quantidade de municípios",
        xaxis_title="Desempenho",
        showlegend=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_desempenho, use_container_width=True)

st.sidebar.title("Informações")
st.sidebar.markdown(
    """
    Esta página apresenta um panorama geral dos serviços de esgotamento sanitário no estado de Goiás.  
    
    Primeiro, mostra a **evolução dos volumes produzidos, coletados e tratados de esgoto**, permitindo visualizar de forma comparativa 
    o crescimento e as diferenças entre essas etapas ao longo do tempo. Em seguida, apresenta a **eficiência dos serviços** por meio de indicadores de relação 
    (quanto foi coletado em relação ao produzido, quanto foi tratado em relação ao coletado e ao produzido), sempre em percentual para facilitar a interpretação.

    Além da visão histórica, o usuário pode **selecionar anos específicos** e ver um resumo da situação dos municípios nesse período.  
    O relatório exibe a **população urbana total** e classifica os municípios em categorias de desempenho (**Ótimo**, **Bom**, **Regular**, **Ruim** e **Indefinido**), 
    indicando quantos municípios estão em cada faixa.  

    Assim, é possível avaliar tanto a evolução do estado ao longo das décadas quanto a distribuição da qualidade do serviço em um ano específico.
    """
)

