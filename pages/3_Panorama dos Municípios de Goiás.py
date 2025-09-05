import streamlit as st
import plotly.express as px
from src.db import (
    obter_volumes_anuais_municipios,
    obter_municipios,
    obter_ranking_melhorias,
    obter_ranking_novas_obras,
    obter_desempenho_municipios
)
from src.utils import (
    criar_cards, titulo_relatorio, 
    formatar_numero_inteiro,
    formatar_numero_decimal,
    sobre_autor
)
from src.geodata_utils import carregar_municipios_goias_para_mapa

st.set_page_config(
    layout="wide"
)

df_volumes_anuais = obter_volumes_anuais_municipios().sort_values(by="Ano")
df_municipios = obter_municipios().sort_values(by="Nome do Município")
df_ranking_melhorias = obter_ranking_melhorias()
df_ranking_novas_obras = obter_ranking_novas_obras()
df_desempenho = obter_desempenho_municipios()

df_municipios["Município_Código"] = df_municipios["Nome do Município"] + " (" + df_municipios["Código IBGE"].astype(str) + ")"
municipios = df_municipios["Município_Código"].value_counts().index.tolist()
total_municipios = len(municipios)
anos = df_volumes_anuais["Ano"].value_counts().sort_index(ascending=False).index.tolist()


def sinc_municipio1():
    st.session_state.municipio2 = st.session_state.municipio1
def sinc_municipio2():
    st.session_state.municipio1 = st.session_state.municipio2

titulo_relatorio()
st.markdown(
    f"""
    <div style="
        padding: 2px;
        text-align: center;
        font-family: 'Cambria Math';">
        <p style="font-size:25px; font-weight: bold;">Panorama dos Municípios de Goiás (1992 - 2021)</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("")

opcoes = ["Gráficos", "Mapa"]
tipo = st.radio(
    "Escolha um tipo de visualização",
    opcoes,
    index=0,
    horizontal=True
)
st.write("")
if tipo == opcoes[0]:
    municipio_selecionado = st.multiselect(
        "Selecione o Município",
        municipios,
        key="municipio1",
        on_change = sinc_municipio1,
        placeholder='Municípios'
    )
    if len(municipio_selecionado) > 1:
        st.warning("Selecione apenas um município.")
        municipio_selecionado = municipio_selecionado[:1]
    elif len(municipio_selecionado) == 0:
        st.warning("Selecione um município.")
    else:
        id_municipio = df_municipios[df_municipios["Município_Código"].isin(municipio_selecionado)]["id"].values[0]
        df_ranking_melhorias_filtrado = df_ranking_melhorias[df_ranking_melhorias["id_municipio"] == id_municipio]["Posição"].values[0]
        df_ranking_novas_obras_filtrado = df_ranking_novas_obras[df_ranking_novas_obras["id_municipio"] == id_municipio]["Posição"].values[0]
        cards_linha2 = [
            {
                "titulo": "Prioridade: Obras de Melhorias", 
                "%cor": "#424242", 
                "valor": f"{df_ranking_melhorias_filtrado}º de {total_municipios}", 
                "bg": "#E0E0E0"
            },
            {
                "titulo": "Prioridade: Novas Obras", 
                "%cor": "#424242", 
                "valor": f"{df_ranking_novas_obras_filtrado}º de {total_municipios}", 
                "bg": "#E0E0E0"
            },    
        ]
        criar_cards(cards_linha2, 2)
        
        df_volumes_anuais = df_volumes_anuais[df_volumes_anuais["id_municipio"] == id_municipio]
        df_long_volume = df_volumes_anuais.melt(
            id_vars="Ano",
            value_vars=["Volume produzido (1000 m³)", "Volume coletado (1000 m³)", "Volume tratado (1000 m³)"],
            var_name="Tipo Volume",
            value_name="Volume"
        )
        df_long_volume["Volume_fmt"] = df_long_volume["Volume"].apply(formatar_numero_decimal)
        fig_volume = px.line(
            df_long_volume,
            x="Ano",
            y="Volume",
            color="Tipo Volume",
            hover_data={"Volume_fmt": True, "Volume": False},
            markers=True,
            title=f"Volumes de Esgotos Tratados, Coletados e Produzidos em {municipio_selecionado[0]}",
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
        fig_volume.update_yaxes(autorange=True)
        fig_volume.update_traces(
            hovertemplate='Ano: %{x}<br>Volume (em 1000 m³): %{customdata[0]}'
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

        df_long_relacao = df_volumes_anuais.melt(
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
            title=f"Eficiência (Quantitativa) dos Serviços de Tratamento de Esgotos em {municipio_selecionado[0]}",
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
        
        col_ano, col_municipio = st.columns(2)
        with col_ano:
            ano_selecionado = st.selectbox(
                "Selecione o Ano de Referência",
                anos,
                index=0
            )
        with col_municipio:
            st.multiselect(
            "Município Selecionado",
            municipios,
            key="municipio2",
            on_change = sinc_municipio2,
            placeholder='Municípios'
        )
        if st.session_state.municipio1 != st.session_state.municipio2:
            st.session_state.municipio1 = st.session_state.municipio2
        if len(municipio_selecionado) > 1:
            st.warning("Selecione apenas 1 município.")
            municipio_selecionado = municipio_selecionado[:1]
        elif len(municipio_selecionado) == 0:
            st.warning("Selecione 1 município.")
        else:
            df_volumes_anuais = df_volumes_anuais[df_volumes_anuais["Ano"] == ano_selecionado]
            df_desempenho_filtrado = df_desempenho[df_desempenho["id_municipio"] == id_municipio]
            df_desempenho_filtrado = df_desempenho_filtrado[df_desempenho_filtrado["Ano"] == ano_selecionado]
            total_habitantes = df_desempenho_filtrado["População total urbana"].values[0]
            desempenho = df_desempenho_filtrado["Desempenho geral"].values[0]
            cores_desempenho = {
                "Ótimo": "#1B5E20",
                "Bom": "#66BB6A",
                "Regular": "#FBC02D",
                "Ruim": "#C62828",
                "Indefinido": "#9E9E9E"
            }
            bg_desempenho = {
                "Ótimo": "#C8E6C9", 
                "Bom": "#E8F5E9", 
                "Regular": "#FFF9C4", 
                "Ruim": "#FFCDD2",
                "Indefinido": "#E0E0E0"
            }
            cards_linha1 = [
                {"titulo": f"Habitantes em {municipio_selecionado[0]} - {ano_selecionado}", "%cor": cores_desempenho.get(desempenho, "#000000"), "valor": formatar_numero_inteiro(total_habitantes), "bg": bg_desempenho.get(desempenho, "#FFFFFF")},       # verde escuro no texto, fundo verde claro
            ]
            cards_linha2 = [
                {"titulo": f"Desempenho Anual em {municipio_selecionado[0]} - {ano_selecionado}", "%cor": cores_desempenho.get(desempenho, "#000000"), "valor": desempenho, "bg": bg_desempenho.get(desempenho, "#FFFFFF")},     # mesma paleta
            ]
            criar_cards(cards_linha1, 1)
            st.write("")
            criar_cards(cards_linha2, 1)
            st.write("")

if tipo == opcoes[1]:
    anos_opcoes = [""] + anos
    ano_selecionado2 = st.selectbox(
                "Selecione o Ano de Referência",
                anos_opcoes,
                index=0
            )
    if ano_selecionado2 == "":
        st.warning("Selecione um ano para visualizar o mapa.")
    else:
        with st.spinner("Carregando o mapa, isso pode levar alguns segundos... Por favor, aguarde!"):
            gdf = carregar_municipios_goias_para_mapa()
            df_desempenho_filtrado = df_desempenho[df_desempenho["Ano"] == ano_selecionado2]
            gdf = gdf.merge(df_desempenho_filtrado, left_on="id_municipio", right_on="id_municipio").\
            drop(columns=["CD_MUN","id_municipio"]) 
            gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.002)
            for col in [
                "Relação coletado/produzido",
                "Relação tratado/coletado",
                "Relação tratado/produzido"
            ]:
                gdf[col + " (%)"] = (gdf[col] * 100).round(2).astype(str) + "%"
            gdf_proj = gdf.to_crs(epsg=31982)
            gdf_proj = gdf.to_crs(epsg=31982)
            gdf["lon"] = gdf_proj.geometry.centroid.x.apply(lambda x: formatar_numero_decimal(x, 4))
            gdf["lat"] = gdf_proj.geometry.centroid.y.apply(lambda y: formatar_numero_decimal(y, 4))
            gdf["População total urbana"] = gdf["População total urbana"].apply(lambda x: formatar_numero_inteiro(x))
            fig = px.choropleth( 
                gdf, 
                geojson=gdf.geometry,
                locations=gdf.index,
                color="Desempenho geral",
                hover_name="Nome do município",
                hover_data=[
                    "Ranking Melhorias", 
                    "Ranking Novas Obras", 
                    "Código IBGE",
                    "População total urbana",
                    "Volume produzido (1000 m³)",
                    "Volume coletado (1000 m³)",
                    "Volume tratado (1000 m³)",
                    "Relação coletado/produzido (%)",
                    "Relação tratado/coletado (%)",
                    "Relação tratado/produzido (%)",
                    "Ano",
                    "lon",
                    "lat"
                ], 
                projection="mercator",
                color_discrete_map={
                    "Ótimo": "#1B5E20",
                    "Bom": "#66BB6A",
                    "Regular": "#FBC02D",
                    "Ruim": "#C62828",
                    "Indefinido": "#9E9E9E"
                },
            )
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Ano: %{customdata[10]}",
                    "Código IBGE: %{customdata[2]}",
                    "Município: %{hovertext}",
                    "Ranking Melhorias: %{customdata[0]}",
                    "Ranking Novas Obras: %{customdata[1]}",
                    "População urbana: %{customdata[3]}",
                    "Volume produzido (1000 m³): %{customdata[4]}",
                    "Volume coletado (1000 m³): %{customdata[5]}",
                    "Volume tratado (1000 m³): %{customdata[6]}",
                    "Relação coletado/produzido: %{customdata[7]}",
                    "Relação tratado/coletado: %{customdata[8]}",
                    "Relação tratado/produzido: %{customdata[9]}",
                    "Longitude: %{customdata[11]}",
                    "Latitude: %{customdata[12]}",
                    "<extra></extra>",
                ]),
            )
            fig.update_geos(fitbounds="locations", visible=False) 
            fig.update_layout(
                title=dict(
                    text=f"Desempenho dos Municípios de Goiás em {ano_selecionado2}",
                    x=0.5,
                    xanchor="center",
                    yanchor="top"
                ),
                height=700,
                margin={"r":20,"t":60,"l":20,"b":60},  # espaço extra pro título e legenda
                paper_bgcolor="white",
                plot_bgcolor="white",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,         # coloca legenda fora do gráfico
                    xanchor="center",
                    x=0.5
                ),
                shapes=[
                    dict(
                        type="rect",
                        xref="paper", yref="paper",
                        x0=-0.001, y0=-0.001, x1=1.001, y1=1.001,  # ligeiro ajuste
                        line=dict(color="black", width=0.5),
                        fillcolor="rgba(0,0,0,0)"
                    )
                ]
            ) 
            st.plotly_chart(fig, use_container_width=True)


st.sidebar.title("Informações")
st.sidebar.markdown(
    """
    Esta página permite explorar informações detalhadas sobre os municípios de Goiás, de 1992 a 2021. Você pode escolher um município e um ano para ver dados específicos.  

    É possível acompanhar os volumes de esgoto **produzidos, coletados e tratados** ao longo do tempo e entender a **eficiência do serviço** através de relações percentuais entre essas etapas. Também são mostradas as **prioridades do município** para novas obras e obras de melhorias, e o **desempenho geral** do município naquele ano.  

    Um **mapa interativo** permite ver todos os municípios de Goiás de forma visual, com cores que indicam o desempenho e informações detalhadas ao passar o mouse, incluindo população, volumes de esgoto e rankings. Assim, é fácil comparar municípios e acompanhar a evolução dos serviços de saneamento.
    """
)

sobre_autor()



