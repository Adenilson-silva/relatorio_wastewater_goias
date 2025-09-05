import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.querys import * 
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# PARA O STREAMLIT CLOUD
#user = st.secrets["postgres"]["user"]
#password = st.secrets["postgres"]["password"]
#host = st.secrets["postgres"]["host"]
#database = st.secrets["postgres"]["database"]
#port = st.secrets["postgres"]["port"]

#[postgres]
#user = "SEU_USUARIO"
#password = "SUA_SENHA"
#host = "seu_host.postgres.database.azure.com"
#database = "nome_banco"
#port = 5432

@st.cache_resource
def get_engine():
    user_azure = st.secrets["DB_USER"]#os.getenv("DB_USER")
    password_azure = st.secrets["DB_PASSWORD"]#os.getenv("DB_PASSWORD")
    host_azure = st.secrets["DB_HOST"]#os.getenv("DB_HOST")
    port_azure = st.secrets["DB_PORT"]#int(os.getenv("DB_PORT", 5432))
    dbname_azure = st.secrets["DB_NAME"]#os.getenv("DB_NAME")
    azure_engine = create_engine(f'postgresql://{user_azure}:{password_azure}@{host_azure}:{port_azure}/{dbname_azure}')
    return azure_engine

# Cache para consultas (boa prática no Streamlit)
@st.cache_data(ttl=600) 
def query_to_df(sql: str) -> pd.DataFrame:
    engine = get_engine()
    df = pd.read_sql(sql, engine)
    return df

@st.cache_data(ttl=600) 
def obter_volumes_anuais_goias() -> pd.DataFrame:
    df = query_to_df(QUERY_VIEW_VOLUME_ANUAL_GOIAS)
    return df

@st.cache_data(ttl=600) 
def obter_desempenho_municipios() -> pd.DataFrame:
    df = query_to_df(QUERY_VIEW_DESEMPENHO)
    return df

@st.cache_data(ttl=600) 
def obter_ranking_melhorias() -> pd.DataFrame:
    df = query_to_df(QUERY_VIEW_RANKING_MELHORIAS)
    return df

@st.cache_data(ttl=600) 
def obter_ranking_novas_obras() -> pd.DataFrame:
    df = query_to_df(QUERY_VIEW_RANKING_NOVAS_OBRAS)
    return df

@st.cache_data(ttl=600) 
def obter_municipios() -> pd.DataFrame:
    df = query_to_df(QUERY_MUNICIPIOS)
    return df

@st.cache_data(ttl=600) 
def obter_volumes_anuais_municipios() -> pd.DataFrame:
    df = query_to_df(QUERY_VOLUME_ANUAL_ESGOTO)
    return df


