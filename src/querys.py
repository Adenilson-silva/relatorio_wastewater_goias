# Aqui você organiza suas consultas
QUERY_VOLUME_ANUAL_ESGOTO = """
    SELECT 
        id_municipio as "id_municipio",
        populacao_total_urbana as "População total urbana",
        volume_produzido_m3 as "Volume produzido (1000 m³)",
        volume_coletado_m3 as "Volume coletado (1000 m³)",
        volume_tratado_m3 as "Volume tratado (1000 m³)",
        relacao_coletado_produzido as "Relação coletado/produzido",
        relacao_tratado_coletado as "Relação tratado/coletado",
        relacao_tratado_produzido as "Relação tratado/produzido", 
        ano_referencia as "Ano",
        possui_dado_interpolado as "Possui dado interpolado"
    FROM
        dw_gestao_esgotos_goias.fato_volume_anual_esgotos
    ;
"""

QUERY_MUNICIPIOS = """
    SELECT 
        id_municipio as "id",
        codigo_ibge as "Código IBGE",
        nome as "Nome do Município"
    FROM
        dw_gestao_esgotos_goias.dim_municipio
    ;
"""

QUERY_VIEW_DESEMPENHO = """
    SELECT
        id_municipio as "id_municipio",
        populacao_total_urbana as "População total urbana",
        volume_produzido_m3 as "Volume produzido (1000 m³)",
        volume_coletado_m3 as "Volume coletado (1000 m³)",
        volume_tratado_m3 as "Volume tratado (1000 m³)",
        relacao_coletado_produzido as "Relação coletado/produzido",
        relacao_tratado_coletado as "Relação tratado/coletado",
        relacao_tratado_produzido as "Relação tratado/produzido", 
        ano_referencia as "Ano",
        possui_dado_interpolado as "Possui dado interpolado", 
        desempenho_geral as "Desempenho geral"
    FROM
        dw_gestao_esgotos_goias.view_desempenho
    ;
"""

QUERY_VIEW_RANKING_MELHORIAS = """
    SELECT
        posicao as "Posição",
        id_municipio as "id_municipio",
        nome as "Nome do município",
        codigo_ibge as "Código IBGE"
    FROM  
        dw_gestao_esgotos_goias.view_ranking_melhorias
    ;
"""

QUERY_VIEW_RANKING_NOVAS_OBRAS = """
    SELECT
        posicao as "Posição",
        id_municipio as "id_municipio",
        nome as "Nome do município",
        codigo_ibge as "Código IBGE"
    FROM   
        dw_gestao_esgotos_goias.view_ranking_novas_obras
    ;
"""

QUERY_VIEW_VOLUME_ANUAL_GOIAS = """
    SELECT
        populacao_total_urbana as "População ubana total",
        volume_produzido_m3 as "Volume produzido (1000 m³)",
        volume_coletado_m3 as "Volume coletado (1000 m³)",
        volume_tratado_m3 as "Volume tratado (1000 m³)",
        relacao_coletado_produzido as "Relação coletado/produzido",
        relacao_tratado_coletado as "Relação tratado/coletado",
        relacao_tratado_produzido as "Relação tratado/produzido",
        ano_referencia as "Ano"
    FROM   
        dw_gestao_esgotos_goias.view_volume_anual_goias
    ;
"""
