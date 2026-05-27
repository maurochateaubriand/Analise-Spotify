# Análise Musical - Spotify

Projeto de análise de dados usando Python e a API do Spotify.

## O que o projeto faz
- Busca os 10 artistas e músicas mais ouvidos 
- Gera gráficos visuais com os dados

## Tecnologias usadas
- Python
- Spotipy
- Pandas
- Matplotlib / Seaborn

## Como rodar
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` na pasta do projeto com o conteúdo:
    SPOTIPY_CLIENT_ID=seu_client_id_aqui
    SPOTIPY_CLIENT_SECRET=seu_client_secret_aqui
    SPOTIPY_REDIRECT_URI=https://open.spotify.com
    > Para obter as credenciais, crie um app gratuito em [developer.spotify.com](https://developer.spotify.com)
4. Rode: `python main.py`