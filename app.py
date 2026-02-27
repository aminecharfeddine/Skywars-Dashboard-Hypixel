import streamlit as st
import requests
import math

API_KEY = "TA_CLE_HYPIXEL_ICI"

st.set_page_config(page_title="SkyWars Stats", layout="wide")

st.title("🔥 SkyWars Stats Viewer")
st.markdown("Entrez un pseudo Minecraft ou un UUID")

# ----------- INPUT -----------
username = st.text_input("Pseudo ou UUID")

# ----------- UTILS -----------

def get_uuid_from_username(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["id"]
    return None

def get_player_data(uuid):
    url = f"https://api.hypixel.net/v2/player?uuid={uuid}"
    headers = {"API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def safe_div(a, b):
    return round(a / b, 2) if b != 0 else 0

# ----------- MAIN -----------

if username:
    uuid = username

    # Si ce n’est pas un UUID → on convertit
    if "-" not in username and len(username) <= 16:
        uuid = get_uuid_from_username(username)
        if not uuid:
            st.error("Pseudo introuvable.")
            st.stop()

    data = get_player_data(uuid)

    if not data.get("success"):
        st.error("Erreur API Hypixel")
        st.stop()

    player = data.get("player")
    if not player or "stats" not in player:
        st.error("Aucune donnée trouvée.")
        st.stop()

    skywars = player["stats"].get("SkyWars", {})

    # ----------- GLOBAL -----------
    wins = skywars.get("wins", 0)
    losses = skywars.get("losses", 0)
    kills = skywars.get("kills", 0)
    deaths = skywars.get("deaths", 0)
    coins = skywars.get("coins", 0)
    winstreak = skywars.get("winstreak", 0)
    highest_ws = skywars.get("highestWinstreak", 0)

    kd = safe_div(kills, deaths)
    wl = safe_div(wins, losses)

    st.header("📊 Global Stats")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Wins", wins)
    col2.metric("Kills", kills)
    col3.metric("K/D", kd)
    col4.metric("W/L", wl)

    col5, col6, col7 = st.columns(3)
    col5.metric("Coins", coins)
    col6.metric("Win Streak", winstreak)
    col7.metric("Highest WS", highest_ws)

    # ----------- SOLO -----------
    st.header("⚔️ Solo")

    wins_solo = skywars.get("wins_solo", 0)
    losses_solo = skywars.get("losses_solo", 0)
    kills_solo = skywars.get("kills_solo", 0)
    deaths_solo = skywars.get("deaths_solo", 0)

    kd_solo = safe_div(kills_solo, deaths_solo)
    wl_solo = safe_div(wins_solo, losses_solo)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Wins Solo", wins_solo)
    col2.metric("Kills Solo", kills_solo)
    col3.metric("K/D Solo", kd_solo)
    col4.metric("W/L Solo", wl_solo)

    # ----------- TEAM -----------
    st.header("👥 Team")

    wins_team = skywars.get("wins_team", 0)
    losses_team = skywars.get("losses_team", 0)
    kills_team = skywars.get("kills_team", 0)
    deaths_team = skywars.get("deaths_team", 0)

    kd_team = safe_div(kills_team, deaths_team)
    wl_team = safe_div(wins_team, losses_team)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Wins Team", wins_team)
    col2.metric("Kills Team", kills_team)
    col3.metric("K/D Team", kd_team)
    col4.metric("W/L Team", wl_team)

    st.success("Stats chargées avec succès 🔥")
