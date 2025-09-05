import geopandas as gpd
from pathlib import Path
import streamlit as st
from src.db import (
    obter_ranking_melhorias,
    obter_ranking_novas_obras
)

@st.cache_data(ttl=600)
def carregar_shapefile(nome_arquivo: str, pasta: str = "geodata"):
    caminho = Path(pasta) / nome_arquivo
    gdf = gpd.read_file(caminho)
    return gdf

@st.cache_data(ttl=600) 
def carregar_municipios_goias() -> gpd.GeoDataFrame:
    nome_arquivo = "GO/GO_Municipios_2024.shp"
    nome_arquivo
    gdf = carregar_shapefile(nome_arquivo)
    return gdf[['CD_MUN','geometry']]

@st.cache_data(ttl=600) 
def carregar_municipios_goias_para_mapa() -> gpd.GeoDataFrame:
    df_ranking_melhorias = obter_ranking_melhorias()
    df_ranking_novas_obras = obter_ranking_novas_obras()
    gdf = carregar_municipios_goias()
    gdf = gdf.merge(df_ranking_melhorias, left_on="CD_MUN", right_on="Código IBGE").\
    drop(columns=["Código IBGE", "id_municipio","Nome do município"]).\
    rename(columns={"Posição":"Ranking Melhorias"})
    gdf = gdf.merge(df_ranking_novas_obras, left_on="CD_MUN", right_on="Código IBGE").\
    rename(columns={"Posição":"Ranking Novas Obras"})
    return gdf



