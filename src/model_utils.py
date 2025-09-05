import streamlit as st
import joblib
from pathlib import Path

MODEL_DIR = Path("models")

@st.cache_resource(ttl=600)
def carregar_modelo_produzido():
    modelo_poli_produzido, feature_poli_produzido = joblib.load(
        MODEL_DIR / "modelo_poli_produzido.pkl")
    return modelo_poli_produzido, feature_poli_produzido


@st.cache_resource(ttl=600)
def carregar_modelo_coletado():
    modelo_poli_coletado, feature_poli_coletado = joblib.load(
        MODEL_DIR / "modelo_poli_coletado.pkl"
    )
    return modelo_poli_coletado, feature_poli_coletado


@st.cache_resource(ttl=600)
def carregar_modelo_tratado():
    modelo_poli_tratado, feature_poli_tratado = joblib.load(
        MODEL_DIR / "modelo_poli_tratado.pkl"
    )
    return modelo_poli_tratado, feature_poli_tratado


@st.cache_resource(ttl=600)
def carregar_todos_modelos():
    modelo_poli_produzido, feature_poli_produzido = carregar_modelo_produzido()
    modelo_poli_coletado, feature_poli_coletado = carregar_modelo_coletado()
    modelo_poli_tratado, feature_poli_tratado = carregar_modelo_tratado()
    return (
        (modelo_poli_produzido, feature_poli_produzido),
        (modelo_poli_coletado, feature_poli_coletado),
        (modelo_poli_tratado, feature_poli_tratado),
    )