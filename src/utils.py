import streamlit as st

def aviso_horizontal_mobile(largura_limite=600, mensagem="📱 Para melhor visualização dos Gráficos e Mapas, deixe o seu dispositivo na horizontal!"):
    st.markdown(f"""
    <style>
    .mobile-warning {{
        display: none;
        color: red;
        font-weight: bold;
        text-align: center;
    }}

    @media (max-width: {largura_limite}px) {{
        .mobile-warning {{
            display: block;
        }}
    }}
    </style>
    <div class="mobile-warning">
    {mensagem}
    </div>
    """, unsafe_allow_html=True)

def titulo_relatorio():
    aviso_horizontal_mobile()
    st.markdown(
        """
        <div style="
            padding: 2px;
            text-align: center;
            font-family: 'Cambria Math';">
            <h3>USO DE DADOS (VOLUMÉTRICOS) PARA OTIMIZAR A ALOCAÇÃO DE RECURSOS DESTINADOS AO SANEAMENTO BÁSICO DE GOIÁS</h3> 
        </div>
        """,
        unsafe_allow_html=True
    )

def sobre_autor():
    st.sidebar.title("Autor")
    st.sidebar.markdown(
        """
        **[Adenilson Silva](https://www.linkedin.com/in/adenilson-silva/)**
        """
    )

def criar_cards(cards, n_colunas):
        cols = st.columns(n_colunas)
        for col, card in zip(cols, cards):
            col.markdown(
                f"""
                <div style="
                    background-color:{card['bg']};
                    padding:10px 15px;
                    border-radius:10px;
                    text-align:center;">
                    <h7>{card['titulo']}</h7>
                    <p style="font-size:18px;font-weight:bold;color:{card['%cor']};">{card['valor']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

def formatar_numero_inteiro(numero):
    numero_formatado = f"{numero:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return numero_formatado

def formatar_numero_decimal(numero, casas=2):
    formato = f"{{:,.{casas}f}}"   
    numero_formatado = formato.format(numero)
    numero_formatado = numero_formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    return numero_formatado

def formatar_numero_percentual(numero, casas=2):
    formato = f"{{:,.{casas}f}}"  
    numero_formatado = formato.format(numero*100)
    numero_formatado = f"{numero_formatado.replace(",", "X").replace(".", ",").replace("X", ".")}%"
    return numero_formatado



