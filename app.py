import streamlit as st
import requests

st.set_page_config(page_title="Stats SkyWars Hypixel", layout="centered")
st.title("Hypixel SkyWars Stats")

# --- Inputs utilisateur ---
api_key = st.text_input("Entrez votre clé API Hypixel")
user_input = st.text_input("Entrez votre pseudo ou UUID Minecraft")

if api_key and user_input:
    # --- Vérifier si c'est un pseudo ou UUID ---
    if len(user_input) <= 16:  # probablement un pseudo
        mojang_resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user_input}")
        if mojang_resp.status_code != 200:
            st.error("Pseudo invalide !")
        else:
            uuid = mojang_resp.json()["id"]
    else:
        uuid = user_input

    # --- Appel à l'API Hypixel ---
    url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
    resp = requests.get(url)
    
    if resp.status_code != 200:
        st.error(f"Erreur API Hypixel : {resp.status_code}")
    else:
        data = resp.json()
        player_data = data.get("player")
        if not player_data:
            st.warning("Joueur non trouvé ou jamais joué sur Hypixel.")
        else:
            # --- Nouvelle structure : stats sous player['stats']['SkyWars'] ---
            skywars = player_data.get("stats", {}).get("SkyWars")
            if not skywars:
                st.warning("Aucune stats SkyWars pour ce joueur.")
            else:
                st.subheader(f"Stats SkyWars pour {user_input}")
                st.write(f"**Wins:** {skywars.get('wins', 0)}")
                st.write(f"**Losses:** {skywars.get('losses', 0)}")
                st.write(f"**Kills:** {skywars.get('kills', 0)}")
                st.write(f"**Deaths:** {skywars.get('deaths', 0)}")
                st.write(f"**Coins:** {skywars.get('coins', 0)}")
                st.write(f"**Win Streak:** {skywars.get('win_streak', 0)}")
