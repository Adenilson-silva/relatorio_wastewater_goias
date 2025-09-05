import streamlit as st

def aviso_horizontal_mobile(largura_limite=800, mensagem="📱 Para melhor visualização, vire seu celular para a horizontal!"):
    js_code = f"""
    <div id="mobile-warning" style="display:none; color:red; font-weight:bold; text-align:center;">
        {mensagem}
    </div>

    <script>
    (function() {{
        function checkWidth() {{
            var w = window.innerWidth;
            var warning = document.getElementById('mobile-warning');
            if (w < {largura_limite}) {{
                warning.style.display = "block";
            }} else {{
                warning.style.display = "none";
            }}
        }}

        // Executa a função na primeira vez
        checkWidth();

        // Monitora redimensionamentos da janela
        window.addEventListener('resize', checkWidth);

        // Usa MutationObserver para garantir que o script seja re-executado
        // se o Streamlit atualizar partes do DOM
        var observer = new MutationObserver(checkWidth);
        observer.observe(document.body, {{ childList: true, subtree: true }});
    }})();
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

def titulo_relatorio():
    aviso_horizontal_mobile()
    st.markdown(
        """
        <div style="
            padding: 2px;
            text-align: center;
            font-family: 'Cambria Math';">
            <h3>USO DE DADOS (QUANTITATIVOS) PARA OTIMIZAR A ALOCAÇÃO DE RECURSOS DESTINADOS AO SANEAMENTO BÁSICO DE GOIÁS</h3> 
        </div>
        """,
        unsafe_allow_html=True
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



