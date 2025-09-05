import streamlit as st
from src.db import (
    obter_ranking_melhorias, 
    obter_ranking_novas_obras
)
from src.utils import (
    titulo_relatorio,
    sobre_autor
)

st.set_page_config(
    layout="wide"
)

df_ranking_melhorias = obter_ranking_melhorias().sort_values(by="Posição")
df_ranking_novas_obras = obter_ranking_novas_obras().sort_values(by="Posição")
min_valor_faixa = 0
max_valor_faixa = len(df_ranking_melhorias)

def atualizar_slider1():
    st.session_state.slider1 = (st.session_state.min1, st.session_state.max1)

def atualizar_numbers1():
    st.session_state.min1, st.session_state.max1 = st.session_state.slider1

def atualizar_slider2():
    st.session_state.slider2 = (st.session_state.min2, st.session_state.max2)

def atualizar_numbers2():
    st.session_state.min2, st.session_state.max2 = st.session_state.slider2

titulo_relatorio()
st.markdown(
    f"""
    <div style="
        padding: 2px;
        text-align: center;
        font-family: 'Cambria Math';">
        <p style="font-size:25px; font-weight: bold;">Rankeamento para Destinação de Recursos </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("") 


col1, col2 = st.columns(2)
with col1:
    st.subheader("Novas Obras")
    st.slider(
        "Selecione o Intervalo de Posição",
        min_valor_faixa, max_valor_faixa,
        value=(min_valor_faixa, max_valor_faixa),
        key="slider1",
        on_change=atualizar_numbers1
    )
    st.number_input(
        "Mínimo",
        value=min_valor_faixa,
        min_value=min_valor_faixa,
        max_value=max_valor_faixa,
        key="min1",
        on_change=atualizar_slider1
    )
    st.number_input(
        "Máximo",
        value=max_valor_faixa,
        min_value=min_valor_faixa,
        max_value=max_valor_faixa,
        key="max1",
        on_change=atualizar_slider1
    )

    intervalo1 = (st.session_state.min1, st.session_state.max1)

    df = df_ranking_novas_obras[
    df_ranking_novas_obras["Posição"].between(*intervalo1)
    ].copy()
    df["Posição"] = df["Posição"].astype(str) + "º"
    df["Município"] = df["Nome do município"] + " (" + df["Código IBGE"].astype(str) + ")"
    df = df[["Posição", "Município"]].set_index("Posição")
    linhas = len(df)
    altura_linha = 35
    cabecalho_linha = 50
    altura_dinamica = cabecalho_linha + linhas * altura_linha
    st.dataframe(df, height=altura_dinamica)


with col2:
    st.subheader("Obras de Melhorias")
    st.slider(
        "Selecione o Intervalo de Posição",
        min_valor_faixa, max_valor_faixa,
        value=(min_valor_faixa, max_valor_faixa),
        key="slider2",
        on_change=atualizar_numbers2
    )

    st.number_input(
        "Mínimo",
        value=min_valor_faixa,
        min_value=min_valor_faixa,
        max_value=max_valor_faixa,
        key="min2",
        on_change=atualizar_slider2
    )
    st.number_input(
        "Máximo",
        value=max_valor_faixa,
        min_value=min_valor_faixa,
        max_value=max_valor_faixa,
        key="max2",
        on_change=atualizar_slider2
    )

    intervalo2 = (st.session_state.min2, st.session_state.max2)
    df = df_ranking_melhorias[
    df_ranking_melhorias["Posição"].between(*intervalo2)
    ].copy()
    df["Posição"] = df["Posição"].astype(str) + "º"
    df["Município"] = df["Nome do município"] + " (" + df["Código IBGE"].astype(str) + ")"
    df = df[["Posição", "Município"]].set_index("Posição")
    linhas = len(df)
    altura_linha = 35 
    cabecalho_linha = 50
    altura_dinamica = cabecalho_linha + linhas * altura_linha
    st.dataframe(df, height=altura_dinamica)

st.sidebar.title("Informações")
st.sidebar.markdown(
    """
    Esta página apresenta o **ranking dos municípios de Goiás** em duas categorias: **Novas Obras** e **Obras de Melhorias**.  
    
    Cada tabela mostra o **nome do município, código IBGE e sua posição no ranking**, permitindo identificar quais municípios têm maior prioridade para alocação de recursos.

    O interessado pode **filtrar o intervalo de posições** usando sliders e campos numéricos, tornando possível visualizar apenas os municípios de interesse.  
    """
)

sobre_autor()


