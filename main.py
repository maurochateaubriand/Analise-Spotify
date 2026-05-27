import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# Autenticação
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read",
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
))

# Top Artistas
top_artistas = sp.current_user_top_artists(limit=10, time_range="long_term")

artistas = []
for item in top_artistas["items"]:
    artistas.append({
        "artista": item["name"]
    })

df_artistas = pd.DataFrame(artistas)

# Top Musicas
top_musicas = sp.current_user_top_tracks(limit=10, time_range="long_term")

musicas = []
for item in top_musicas["items"]:
    musicas.append({
        "musica": item["name"],
        "artista": item["artists"][0]["name"],
    })

df_musicas = pd.DataFrame(musicas)

# Graficos
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("🎵 Minha Análise Musical - Spotify", fontsize=16, fontweight="bold")

# Adiciona coluna de posição
df_artistas["posicao"] = range(len(df_artistas), 0, -1)
df_musicas["posicao"] = range(len(df_musicas), 0, -1)
df_musicas["musicaeartista"] = df_musicas["musica"] + " - " + df_musicas["artista"]

# Grafico 1 - Top Artistas
sns.barplot(data=df_artistas, x="posicao", y="artista", ax=axes[0], palette="viridis")
axes[0].set_title("Top 10 Artistas Mais Ouvidos")
axes[0].set_xlabel("")
axes[0].set_ylabel("")

# Grafico 2 - Top Músicas
sns.barplot(data=df_musicas, x="posicao", y="musicaeartista", ax=axes[1], palette="magma")
axes[1].set_title("Top 10 Músicas Mais Ouvidas")
axes[1].set_xlabel("")
axes[1].set_ylabel("")

plt.tight_layout()
plt.savefig("analise_spotify.png", dpi=150)
plt.show()
print("Gráfico salvo como analise_spotify.png")

# Prints
print("\n🎤 TOP 10 ARTISTAS:")
print(df_artistas.to_string(index=False))

print("\n🎵 TOP 10 MÚSICAS:")
print(df_musicas.to_string(index=False))