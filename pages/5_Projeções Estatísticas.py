import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.db import obter_volumes_anuais_goias
from src.model_utils import carregar_todos_modelos
from src.utils import (
    criar_cards, 
    titulo_relatorio,
    formatar_numero_decimal,
    formatar_numero_percentual
)

st.set_page_config(
    layout="centered"
)

(modelo_poli_produzido, feature_poli_produzido), \
(modelo_poli_coletado, feature_poli_coletado), \
(modelo_poli_tratado, feature_poli_tratado) = carregar_todos_modelos()

df_volumes_anuais_goias = obter_volumes_anuais_goias().sort_values(by="Ano")
max_ano = df_volumes_anuais_goias["Ano"].max()
anos = list(range(max_ano+1,max_ano+12))

titulo_relatorio()
st.markdown(
    f"""
    <div style="
        padding: 2px;
        text-align: center;
        font-family: 'Cambria Math';">
        <p style="font-size:25px; font-weight: bold;">Projeções Estatísticas dos Volumes de Esgotos em Goiás (2022–2032)</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("")

opcoes = ["Geral", "Específico (por ano)"]
tipo = st.radio(
    "Escolha um tipo de visualização",
    opcoes,
    index=0,
    horizontal=True
)
st.write("")
if tipo == opcoes[0]:
    intervalo_anos = st.slider(
    "Selecione um intervalo de tempo",
    min_value=min(anos),
    max_value=max(anos),
    value=(min(anos), max(anos))
    )

    anos_selecionados = list(range(intervalo_anos[0], intervalo_anos[1]+1))

    y_produzido = []
    y_coletado = []
    y_tratado = []

    for ano in anos_selecionados:
        X_ano = np.array([[ano]])
        
        X_poly = feature_poli_produzido.transform(X_ano)
        y_produzido.append(modelo_poli_produzido.predict(X_poly)[0])
        
        X_poly = feature_poli_coletado.transform(X_ano)
        y_coletado.append(modelo_poli_coletado.predict(X_poly)[0])
        
        X_poly = feature_poli_tratado.transform(X_ano)
        y_tratado.append(modelo_poli_tratado.predict(X_poly)[0])

    df_volumes = pd.DataFrame({
        "Ano": anos_selecionados,
        "Volume produzido (1000 m³)": y_produzido,
        "Volume coletado (1000 m³)": y_coletado,
        "Volume tratado (1000 m³)": y_tratado
    })

    df_long_volume = df_volumes.melt(
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
        height=500,
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
    fig_volume.update_yaxes(
        range=[df_long_volume["Volume"].min()*0.7, df_long_volume["Volume"].max()*1.1],  
    )
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

    df_volumes["Relação coletado/produzido"] = df_volumes["Volume coletado (1000 m³)"] / df_volumes["Volume produzido (1000 m³)"]
    df_volumes["Relação tratado/coletado"] = df_volumes["Volume tratado (1000 m³)"] / df_volumes["Volume coletado (1000 m³)"]
    df_volumes["Relação tratado/produzido"] = df_volumes["Volume tratado (1000 m³)"] / df_volumes["Volume produzido (1000 m³)"]

    df_long_relacao = df_volumes.melt(
        id_vars="Ano",
        value_vars=["Relação coletado/produzido", "Relação tratado/coletado", "Relação tratado/produzido"],
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
        tickvals=df_long_relacao["Ano"].unique()
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

if tipo == opcoes[1]:
    ano_selecionado = st.selectbox(
        "Selecione o Ano de Referência",
        anos,
        index=0
    )
    ano_produzido = feature_poli_produzido.transform(np.array([[ano_selecionado]]))
    y_pred_produzido = modelo_poli_produzido.predict(ano_produzido)[0]

    ano_coletado = feature_poli_coletado.transform(np.array([[ano_selecionado]]))
    y_pred_coletado = modelo_poli_coletado.predict(ano_coletado)[0]

    ano_tratado = feature_poli_tratado.transform(np.array([[ano_selecionado]]))
    y_pred_tratado = modelo_poli_tratado.predict(ano_tratado)[0]

    rel_coletado_produzido=y_pred_coletado/y_pred_produzido
    rel_tratado_coletado=y_pred_tratado/y_pred_coletado
    rel_tratado_produzido=y_pred_tratado/y_pred_produzido

    cards_linha1 = [
        {
            "titulo": "Volume Produzido (1000 m³)",
            "%cor": "#333333", 
            "valor": formatar_numero_decimal(y_pred_produzido),
            "bg": "#F5F5F5",
        },
        {
            "titulo": "Volume Coletado (1000 m³)",
            "%cor": "#333333",
            "valor": formatar_numero_decimal(y_pred_coletado),
            "bg": "#F5F5F5",
        },
        {
            "titulo": "Volume Tratado (1000 m³)",
            "%cor": "#333333",
            "valor": formatar_numero_decimal(y_pred_tratado),
            "bg": "#F5F5F5",
        },
    ]
    cards_linha2 = [
        {
            "titulo": "Relação Coletado/Produzido",
            "%cor": "#333333",
            "valor": formatar_numero_percentual(rel_coletado_produzido),
            "bg": "#F5F5F5",
        },
        {
            "titulo": "Relação Tratado/Coletado",
            "%cor": "#333333",
            "valor": formatar_numero_percentual(rel_tratado_coletado),
            "bg": "#F5F5F5",
        },
        {
            "titulo": "Relação Tratado/Produzido",
            "%cor": "#0D47A1",
            "valor": formatar_numero_percentual(rel_tratado_produzido),
            "bg": "#E3F2FD",
        },
    ]
    criar_cards(cards_linha1, 3)
    st.write("")
    criar_cards(cards_linha2, 3)

st.sidebar.title("Informações")
st.sidebar.markdown(
    """
    Esta página apresenta projeções dos volumes de esgoto **produzidos, coletados e tratados** para os próximos anos, utilizando modelos polinomiais ajustados com os dados históricos do estado.  
    Os gráficos permitem acompanhar a **evolução esperada** e comparar os volumes entre as três etapas, fornecendo uma visão da tendência futura.

    Além disso, a página mostra indicadores de **eficiência quantitativa dos serviços**, como a relação entre coletado e produzido, tratado e coletado, e tratado e produzido, permitindo entender o desempenho esperado dos sistemas de saneamento. 
     
    O usuário pode escolher entre uma visão **geral por intervalo de anos** ou uma **análise específica por ano**, visualizando os dados de forma agregada ou detalhada para cada período.
    """
)



