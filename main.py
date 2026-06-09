import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from dotenv import load_dotenv
import musicbrainzngs
import pylast

# Carrega o .env
load_dotenv()

# Autenticação
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read",
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
))

network = pylast.LastFMNetwork(
    api_key=os.getenv("LASTFM_API_KEY"),
    api_secret=os.getenv("LASTFM_API_SECRET"),
    username=os.getenv("LASTFM_USERNAME")
)

usuario = network.get_user(os.getenv("LASTFM_USERNAME"))

top_tracks_lastfm = usuario.get_top_tracks(limit=10, period=pylast.PERIOD_OVERALL)
top_artistas_lastfm = usuario.get_top_artists(limit=10, period=pylast.PERIOD_OVERALL)


# Top Artistas
musicbrainzngs.set_useragent("AnáliseSpotify", "1.0", "seu_email@gmail.com")

##Generos via musicbrainz
def buscar_genero(nome_artista):
    try:
        resultado = musicbrainzngs.search_artists(artist=nome_artista, limit=1)
        artista = resultado["artist-list"][0]
        tags = artista.get("tag-list", [])
        if tags:
            tags_ordenadas = sorted(tags, key=lambda x: int(x["count"]), reverse=True)
            return ", ".join([t["name"] for t in tags_ordenadas[:1]])
        return "N/A"
    except:
        return "N/A"
    
## Generos Via LastFM
def buscar_genero_lastfm(nome_artista):
    try:
        artista = network.get_artist(nome_artista)
        tags = artista.get_top_tags(limit=1)
        if tags:
            return tags[0].item.name
        return "N/A"
    except:
        return "N/A"

top_artistas = sp.current_user_top_artists(limit=10, time_range="long_term")

artistas = []
for item in top_artistas["items"]:
    nome = item["name"]
    artistas.append({
        "artista": nome,
        "generos": buscar_genero_lastfm(nome)
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

# Plays LastFM
## Musicas
lastfm_musicas = []
for item in top_tracks_lastfm:
    lastfm_musicas.append({
        "musica": item.item.title,
        "artista": item.item.artist.name,
        "plays": item.weight
    })

df_lastfm = pd.DataFrame(lastfm_musicas)
print(df_lastfm)

## Artista

lastfm_artistas = []
for item in top_artistas_lastfm:
    lastfm_artistas.append({
        "artista": item.item.name,
        "plays": item.weight
    })

df_artistas_lastfm = pd.DataFrame(lastfm_artistas)

#df_lastfm["artista"] = lastfm_artistas["artista"]
df_lastfm["musica-artista"] = df_lastfm["musica"] + " - " + df_lastfm["artista"]

# Gêneros
todos_generos = []
for genero in df_artistas["generos"]:
    if genero != "N/A":
        todos_generos.extend(genero.split(", "))

df_generos = pd.DataFrame(todos_generos, columns=["genero"])
contagem_generos = df_generos["genero"].value_counts()

# Adiciona coluna de posição
df_artistas["posicao"] = range(len(df_artistas), 0, -1)
df_musicas["posicao"] = range(len(df_musicas), 0, -1)
df_musicas["musicaeartista"] = df_musicas["musica"] + " - " + df_musicas["artista"]

# Visual
plt.rcParams.update({
    "figure.facecolor": "#0f0f0f",
    "axes.facecolor": "#1a1a1a",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "text.color": "white",
    "grid.color": "#2a2a2a",
    "font.family": "sans-serif",
})

fig, axes = plt.subplots(2, 2, figsize=(22, 7))
fig.suptitle("🎵 Minha Análise Musical - Spotify", 
             fontsize=18, fontweight="bold", color="white", y=1.02)
fig.patch.set_facecolor("#0f0f0f")

# Grafico 1 - Top Artistas
sns.barplot(data=df_artistas, x="posicao", y="artista", 
            ax=axes[0,0], palette="viridis", linewidth=0)
axes[0,0].set_title("Top 10 Artistas Mais Ouvidos", 
                  fontsize=13, fontweight="bold", pad=12)
axes[0,0].set_xlabel("")
axes[0,0].set_ylabel("")
axes[0,0].tick_params(axis="y", labelsize=10)
axes[0,0].xaxis.set_visible(False)
axes[0,0].spines[["top", "right", "left", "bottom"]].set_visible(False)

# Grafico 2 - Top Músicas
sns.barplot(data=df_musicas, x="posicao", y="musicaeartista", 
            ax=axes[0,1], palette="magma", linewidth=0)
axes[0,1].set_title("Top 10 Músicas Mais Ouvidas", 
                  fontsize=13, fontweight="bold", pad=12)
axes[0,1].set_xlabel("")
axes[0,1].set_ylabel("")
axes[0,1].tick_params(axis="y", labelsize=10)
axes[0,1].xaxis.set_visible(False)
axes[0,1].spines[["top", "right", "left", "bottom"]].set_visible(False)

# Gráfico 3 - Gêneros
sns.barplot(data=contagem_generos.reset_index(), 
            x="count", y="genero", ax=axes[1,0], palette="rocket", linewidth=0)
axes[1,0].set_title("Gêneros Mais Ouvidos", 
                  fontsize=13, fontweight="bold", pad=12)
axes[1,0].set_xlabel("")
axes[1,0].set_ylabel("")
axes[1,0].tick_params(axis="y", labelsize=10)
axes[1,0].xaxis.set_visible(False)
axes[1,0].spines[["top", "right", "left", "bottom"]].set_visible(False)

# Grafico 4 - Qtd Plays

sns.barplot(data=df_lastfm, 
            x="plays", y="musica-artista", ax=axes[1,1], palette="rocket", linewidth=0)
for container in axes[1,1].containers:
    axes[1,1].bar_label(container, fontsize=9, color="white", padding=3)
axes[1,1].set_title("Musicas Mais Ouvidas", 
                  fontsize=13, fontweight="bold", pad=12)
axes[1,1].set_xlabel("")
axes[1,1].set_ylabel("")
axes[1,1].tick_params(axis="y", labelsize=10)
axes[1,1].xaxis.set_visible(False)
axes[1,1].spines[["top", "right", "left", "bottom"]].set_visible(False)

plt.tight_layout()
plt.savefig("analise_spotify.png", dpi=150, bbox_inches="tight", 
            facecolor="#0f0f0f")
plt.show()
print("Gráfico salvo como analise_spotify.png")

# Prints
print("\n🎤 TOP 10 ARTISTAS:")
print(df_artistas.to_string(index=False))

print("\n🎵 TOP 10 MÚSICAS:")
print(df_musicas.to_string(index=False))