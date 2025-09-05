import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import titulo_relatorio

st.set_page_config(
    layout="centered"
)
    
titulo_relatorio()
st.markdown("") 

st.markdown("""
    Este projeto representa uma evolução e ramificação de outros dois projetos focados na "Análise Descritiva e Preditiva da Gestão de Esgotos em Goiás" e no "Uso de Dados para Otimizar a Alocação de Recursos Públicos Destinados ao Saneamento Básico de Goiás". Esses trabalhos serviram como base para uma melhoria significativa, resultando nesse **spin-off técnico** com novas funcionalidades e uma abordagem mais ampla.


    ### Principais Melhorias e Migração

    Uma das principais mudanças técnicas foi a migração do **Banco de Dados do PostgreSQL** local para o **Banco de Dados do Azure para PostgreSQL**. Essa transição não apenas melhora a escalabilidade e a disponibilidade dos dados, mas também permite a criação de um **DataWarehouse** que otimiza o acesso e o desempenho.


    ### O Novo Relatório Interativo

    Esta nova versão do Relatório utiliza **Python**, com foco nas bibliotecas **Streamlit**, **Plotly** e **Geopandas**. Essa mudança permitiu a criação de um relatório mais **dinâmico**, que oferece uma visualização mais detalhada dos dados.

    O relatório está organizado em 4 seções, acessíveis pelo menu lateral esquerdo:

    * **Panorama de Goiás** 
    * **Panorama dos Municípios** 
    * **Rankeamento para Destinação de Recursos** 
    * **Projeções Estatísticas** 
            
    Este novo projeto além de aprimorar as visualizações, também integra a capacidade de fazer previsões, fornecendo uma ferramenta mais completa para o monitoramento quantitativo de efluentes em Goiás.
    """)

st.sidebar.title("Autor")
st.sidebar.markdown(
    """
    **Adenilson Silva**  
    [LinkedIn](https://www.linkedin.com/in/adenilson-silva/)
    """
)
