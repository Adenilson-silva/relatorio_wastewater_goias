-- Criar um schema para organizar o DW
CREATE SCHEMA IF NOT EXISTS gestao_esgotos_goias;

SET search_path TO gestao_esgotos_goias;

-- Criar tabela de Municípios
CREATE TABLE municipio (
	id_municipio SERIAL PRIMARY KEY,
    codigo_ibge VARCHAR(50) NOT NULL,
	nome VARCHAR(255) NOT NULL
);

COMMENT ON TABLE municipio IS 'Tabela que armazena informações sobre os municípios.';

COMMENT ON COLUMN municipio.id_municipio IS 'Identificador único do município.';
COMMENT ON COLUMN municipio.codigo_ibge IS 'Código IBGE único para cada município.';
COMMENT ON COLUMN municipio.nome IS 'Nome oficial do município.';

-- Criar tabela de Volumes Anuais de Esgotos
CREATE TABLE volume_anual_esgotos (
	id SERIAL PRIMARY KEY,
	populacao_total_urbana INTEGER NOT NULL,
	volume_produzido_m3 REAL NOT NULL,
    volume_coletado_m3 REAL NOT NULL,
    volume_tratado_m3 REAL NOT NULL,

    -- Indicadores calculados automaticamente
    relacao_tratado_produzido NUMERIC(10, 2) GENERATED ALWAYS AS (
        COALESCE(volume_tratado_m3 / NULLIF(volume_produzido_m3, 0), 0)
	) STORED,

	relacao_coletado_produzido NUMERIC(10, 2) GENERATED ALWAYS AS (
        COALESCE(volume_coletado_m3 / NULLIF(volume_produzido_m3, 0), 0)
	) STORED,

	relacao_tratado_coletado NUMERIC(10, 2) GENERATED ALWAYS AS (
        COALESCE(volume_tratado_m3 / NULLIF(volume_coletado_m3, 0), 0)
	) STORED,

    ano_referencia INTEGER NOT NULL,
	possui_dado_interpolado BOOLEAN NOT NULL DEFAULT FALSE, 

    id_municipio INTEGER NOT NULL REFERENCES municipio(id_municipio)
);

COMMENT ON TABLE volume_anual_esgotos IS 'Tabela que armazena os volumes anuais de esgoto dos municípios.';

COMMENT ON COLUMN volume_anual_esgotos.id IS 'Identificador único da entrada de volume de esgoto.';
COMMENT ON COLUMN volume_anual_esgotos.populacao_total_urbana IS 'Número total de habitantes em áreas urbanas.';
COMMENT ON COLUMN volume_anual_esgotos.volume_produzido_m3 IS 'Quantidade de esgoto produzido (em 1.000 metros cúbicos).';
COMMENT ON COLUMN volume_anual_esgotos.volume_coletado_m3 IS 'Quantidade de esgoto coletado (em 1.000 metros cúbicos).';
COMMENT ON COLUMN volume_anual_esgotos.volume_tratado_m3 IS 'Quantidade de esgoto tratado (em 1.000 metros cúbicos).';
COMMENT ON COLUMN volume_anual_esgotos.relacao_tratado_produzido IS 'Relação entre volume tratado e produzido (tratado/produzido).';
COMMENT ON COLUMN volume_anual_esgotos.relacao_coletado_produzido IS 'Relação entre volume coletado e produzido (coletado/produzido).';
COMMENT ON COLUMN volume_anual_esgotos.relacao_tratado_coletado IS 'Relação entre volume tratado e coletado (tratado/coletado).';
COMMENT ON COLUMN volume_anual_esgotos.ano_referencia IS 'Ano de Referência do registro.';
COMMENT ON COLUMN volume_anual_esgotos.id_municipio IS 'Identificador do município ao qual o volume de esgoto pertence.';

create
view view_desempenho as
with parametros as (
select
	3 as rtp, -- peso da relação tratado/produzido
	2 as rtc, -- peso da relação tratado/coletado
	1 as rcp -- peso da relação coletado/produzido
),
desempenho_calc as (
select
	vae.id_municipio,
	vae.ano_referencia,
	((p.rtp * vae.relacao_tratado_produzido) + 
         (p.rtc * vae.relacao_tratado_coletado) + 
         (p.rcp * vae.relacao_coletado_produzido)) / 6 as desempenho
from
	volume_anual_esgotos vae
cross join parametros p
)
select
	mun.nome,
	mun.codigo_ibge,
	vae.populacao_total_urbana,
	vae.volume_produzido_m3,
	vae.volume_coletado_m3,
	vae.volume_tratado_m3,
	vae.relacao_coletado_produzido,
	vae.relacao_tratado_coletado,
	vae.relacao_tratado_produzido,
	vae.ano_referencia,
	vae.possui_dado_interpolado,
	case
		when d.desempenho between 0 and 0.25 and vae.populacao_total_urbana > 0 then 'Ruim'
		when d.desempenho between 0.25 and 0.5 and vae.populacao_total_urbana > 0 then 'Regular'
		when d.desempenho between 0.5 and 0.75 and vae.populacao_total_urbana > 0 then 'Bom'
		when d.desempenho >= 0.75 and vae.populacao_total_urbana > 0 then 'Ótimo'
		else 'Indefinido'
	end as desempenho_geral
from
	desempenho_calc d
inner join municipio mun on
	d.id_municipio = mun.id_municipio
inner join volume_anual_esgotos vae on
	d.id_municipio = vae.id_municipio and d.ano_referencia = vae.ano_referencia
order by vae.ano_referencia desc, mun.nome asc;

create
view view_ranking_melhorias as
with ano_base as (
select
	2021 as ano
)
select
	row_number() over (
	order by vae.relacao_coletado_produzido,
	vae.relacao_tratado_produzido,
	vae.relacao_tratado_coletado asc,
        vae.populacao_total_urbana desc) posicao,
	mun.nome,
	mun.codigo_ibge
from
	volume_anual_esgotos vae
inner join municipio mun on
	vae.id_municipio = mun.id_municipio
inner join ano_base ab on
	vae.ano_referencia = ab.ano;

create
view view_ranking_novas_obras as
with ano_base as (
select
	2021 as ano
)
select
	row_number() over (
	order by vae.relacao_tratado_coletado,
	vae.relacao_coletado_produzido,
	vae.relacao_tratado_produzido asc,
	vae.populacao_total_urbana desc) posicao,
	mun.nome,
	mun.codigo_ibge
from
	volume_anual_esgotos vae
inner join municipio mun on
	vae.id_municipio = mun.id_municipio
inner join ano_base ab on
	vae.ano_referencia = ab.ano;



