-- DATABASES

CREATE DATABASE weather_db;
CREATE DATABASE newsletter_db;

-- -- Switch to newsletter_db and create table 'users'
-- \c newsletter_db

-- -- Tabela 'users'
-- CREATE TABLE public.users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(254) UNIQUE NOT NULL,
--     frequency VARCHAR(10) NOT NULL
-- );

-- -- Switch to weather_db and create tables 'localizacao' and 'condicoes_climaticas'
-- \c weather_db

-- -- Tabela 'localizacao'
-- CREATE TABLE public.localizacao (
--     id SERIAL PRIMARY KEY,
--     nome VARCHAR(255) NOT NULL,
--     latitude DOUBLE PRECISION NOT NULL,
--     longitude DOUBLE PRECISION NOT NULL
-- );

-- -- Tabela 'condicoes_climaticas'
-- CREATE TABLE public.condicoes_climaticas (
--     id SERIAL PRIMARY KEY,
--     localizacao_id INTEGER REFERENCES localizacao(id) ON DELETE CASCADE,
--     data_hora TIMESTAMP WITHOUT TIME ZONE NOT NULL,
--     descricao_weather VARCHAR(255) NOT NULL,
--     temperatura_atual DOUBLE PRECISION NOT NULL,
--     temperatura_max DOUBLE PRECISION NOT NULL,
--     temperatura_min DOUBLE PRECISION NOT NULL,
--     umidade DOUBLE PRECISION NOT NULL,
--     velocidade_vento DOUBLE PRECISION NOT NULL,
--     direcao_vento DOUBLE PRECISION NOT NULL,
--     rajada_vento DOUBLE PRECISION
-- );

-- -- Inserir dados de teste na tabela users
-- INSERT INTO users (email, frequency) VALUES
-- ('kae.budke@gmail.com', 'weekly'),
-- ('kae.budke@ufms.br', 'biweekly');
