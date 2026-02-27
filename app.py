import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SkyWars Stats", layout="wide")
st.title("📊 Hypixel SkyWars Stats Viewer")

# Entrée de la clé API
api_key = st.text_input("Entrez votre clé API Hypixel", type="password")

# Entrée du pseudo ou UUID
user_input = st.text_input("Entrez votre pseudo ou UUID Hypixel")

if api_key and user_input:
    # Appel API
    url = f"https://api.hypixel.net/v2/player?uuid={user_input}&key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Vérification si le joueur existe
        if not data.get("player"):
            st.warning("Joueur introuvable ou UUID invalide.")
        else:
            skywars = data["player"].get("SkyWars", {})
            
            if not skywars:
                st.info("Le joueur n'a pas encore joué à SkyWars.")
            else:
                # Sélection des stats pertinentes
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
                
                # Calcul ratios
                kd = stats["Kills"] / stats["Deaths"] if stats["Deaths"] else stats["Kills"]
                winrate = stats["Wins"] / stats["Games Played"] * 100 if stats["Games Played"] else 0
                st.metric("K/D Ratio", f"{kd:.2f}")
                st.metric("Win Rate", f"{winrate:.2f}%")
                
    except Exception as e:
        st.error(f"Erreur API : {e}")
