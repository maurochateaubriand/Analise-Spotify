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
2. Crie o ambiente virtual:
uv venv
3. Ative o ambiente:
.venv\Scripts\activate
4. Instale as dependências:
uv pip install -r requirements.txt
5. Crie um arquivo `.env` na pasta do projeto com o seguinte conteúdo:
SPOTIPY_CLIENT_ID=seu_client_id_aqui
SPOTIPY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIPY_REDIRECT_URI=https://open.spotify.com
> Para obter as credenciais, crie um app gratuito em [developer.spotify.com](https://developer.spotify.com) e adicione `https://open.spotify.com` como Redirect URI nas configurações do app.

> Na primeira execução o terminal vai pedir para você colar uma URL. Cole a URL que apareceu na barra do navegador após autorizar o app.

6. Rode:
python main.py