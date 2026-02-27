import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SkyWars Stats", layout="wide")
st.title("📊 Hypixel SkyWars Stats Viewer")

api_key = st.text_input("Entrez votre clé API Hypixel", type="password")
user_input = st.text_input("Entrez votre pseudo ou UUID Hypixel")

if api_key and user_input:
    
    # Vérifier si c'est un pseudo et récupérer UUID
    if len(user_input) <= 16:  # pseudo max 16 caractères
        mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{user_input}"
        mojang_resp = requests.get(mojang_url)
        if mojang_resp.status_code == 200:
            user_input = mojang_resp.json()["id"]
        else:
            st.warning("Pseudo invalide.")
    
    url = f"https://api.hypixel.net/v2/player?uuid={user_input}&key={api_key}"
    try:
        resp = requests.get(url)
        data = resp.json()
        if not data.get("player"):
            st.warning("Joueur introuvable.")
        else:
            skywars = data["player"].get("SkyWars", {})
            if not skywars:
                st.info("Le joueur n'a pas encore joué à SkyWars.")
            else:
                stats = {
                    "Wins": skywars.get("wins", 0),
                    "Losses": skywars.get("losses", 0),
                    "Kills": skywars.get("kills", 0),
                    "Deaths": skywars.get("deaths", 0),
                    "Win Streak": skywars.get("win_streak", 0),
                    "Games Played": skywars.get("games", 0),
                    "Coins": skywars.get("coins", 0),
                    "Souls": skywars.get("souls", 0),
                }
                df = pd.DataFrame(stats.items(), columns=["Stat", "Value"])
                st.subheader(f"SkyWars Stats pour {user_input}")
                st.table(df)
                kd = stats["Kills"] / stats["Deaths"] if stats["Deaths"] else stats["Kills"]
                winrate = stats["Wins"] / stats["Games Played"] * 100 if stats["Games Played"] else 0
                st.metric("K/D Ratio", f"{kd:.2f}")
                st.metric("Win Rate", f"{winrate:.2f}%")
    except Exception as e:
        st.error(f"Erreur API : {e}")
