import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import random
import time

# Apply layout constraints
st.set_page_config(
    page_title="Pokemon Combat Simulator | Group 7", 
    page_icon="⚔️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Explicitly override metadata to fix cached social media previews (WhatsApp)
st.markdown("""
<head>
    <meta name="description" content="Pokemon Combat Simulator developed by Group 7. A full-featured battle engine with API integration and stat visualization.">
    <meta property="og:title" content="Pokemon Combat Simulator | Group 7">
    <meta property="og:description" content="A full-featured battle engine with API integration and stat visualization. Final Academic Submission.">
</head>
""", unsafe_allow_html=True)

if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False
if "battle_active" not in st.session_state:
    st.session_state.battle_active = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False

if not st.session_state.splash_shown:
    splash_ph = st.empty()
    with splash_ph.container():
        st.markdown('''
        <style>
        .splash-container {
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 999998 !important;
            background: black !important;
            overflow: hidden !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .splash-video {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            object-fit: cover !important;
            object-position: center 0% !important;
            pointer-events: none !important;
        }
        header { display: none !important; }
        div[data-testid="stAppViewContainer"] {
            background-color: black !important;
        }
        </style>
        <div class="splash-container">
            <video class="splash-video" autoplay loop muted playsinline>
                <source src="https://github.com/malverjr/pokemon-combat-simulator/raw/main/mylivewallpapers-com-Fire-Breathing-Charizard-3440x1440.mp4" type="video/mp4">
            </video>
        </div>
        ''', unsafe_allow_html=True)
    
    time.sleep(3.5)
    st.session_state.splash_shown = True
    st.rerun()

# Inject Custom "Apple Pro" Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap');

    /* Nintendo Switch Game Global Variables */
    :root {
        --nintendo-bg: #e8f4f8; 
        --nintendo-card: #ffffff;
        --nintendo-border: #2a2a2a;
        --nintendo-text: #2b2b2b;
    }
    
    .stApp {
        background-color: var(--nintendo-bg) !important;
        background-image: none !important;
        font-family: 'Nunito', sans-serif !important;
        color: var(--nintendo-text);
    }
    
    header {visibility: hidden;}
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6, p, span, div {
        font-family: 'Nunito', sans-serif !important;
        color: var(--nintendo-text);
    }
    
    /* Desktop Title */
    h1 {
        font-weight: 900 !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px !important;
        margin-bottom: 2rem !important;
        font-size: 3rem !important;
        color: var(--nintendo-text) !important;
        text-shadow: 2px 2px 0px white;
    }
    
    h2, h3 {
        font-weight: 800 !important;
        color: var(--nintendo-text) !important;
        letter-spacing: 0px !important;
        text-shadow: none !important;
        border-bottom: none !important;
    }
    
    /* Clean up the native columns to not be glassmorphic anymore */
    [data-testid="column"] {
        background: transparent !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        margin-bottom: 0rem !important;
        transition: none !important;
    }
    
    [data-testid="column"]:hover {
        transform: none;
        box-shadow: none !important;
        border-color: transparent !important;
    }
    
    /* Inputs (Selectbox) */
    div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 3px solid var(--nintendo-border) !important;
        border-radius: 8px !important;
        color: var(--nintendo-text) !important;
        font-weight: 800;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.1) !important;
        transition: all 0.2s ease;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #0A84FF !important;
    }
    div[data-baseweb="select"] * { color: var(--nintendo-text) !important; }
    
    /* Big Action Buttons Base */
    .stButton > button {
        background: white !important;
        color: var(--nintendo-text) !important;
        border: 4px solid var(--nintendo-border) !important;
        border-radius: 12px !important; 
        padding: 15px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-transform: capitalize;
        letter-spacing: 0px;
        box-shadow: 2px 4px 0px rgba(0,0,0,0.2), inset 0 0 0 3px white !important;
        transition: all 0.1s !important;
        width: 100%;
        margin-top: 10px;
    }
    .stButton > button:active, .stButton > button:hover {
        transform: translateY(4px);
        box-shadow: 0px 0px 0px rgba(0,0,0,0.2), inset 0 0 0 3px white !important;
        filter: brightness(0.9);
    }
    
    /* Removed rigid Switch button colors here in favor of dynamic API Type injection logic further down */
    /* Clean Images */
    img { filter: drop-shadow(0 0px 0px transparent); }
    
    /* Epic AAA Anime Vector Battle Arena */
    .arena-container {
        height: 640px; /* Just the battle scene — control panel is a separate element below */
        border: 8px solid white;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15), inset 0 0 15px rgba(0,0,0,0.1);
        margin-bottom: 8px; /* Small gap between arena and control panel */
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    @keyframes faint {
        0% { opacity: 1; transform: translateY(0); filter: grayscale(0); }
        100% { opacity: 0; transform: translateY(120px) scale(0.85); filter: grayscale(1); }
    }
    .faint {
        animation: faint 0.9s ease-in forwards !important;
        pointer-events: none !important;
    }
    .faint img, .faint .shadow {
        filter: grayscale(1) brightness(0.5);
        opacity: 0 !important;
        transition: opacity 1s ease-in !important;
    }
    
    .sprite-player, .sprite-opponent {
        transition: transform 0.3s ease-out, opacity 0.3s ease-out; /* Smooth transitions for non-faint movements */
    }
    
    /* Force overlapping layout z-index priority */
    [data-testid="stHorizontalBlock"] { position: relative; z-index: 50; }
    
    /* HP Overlay Cards precisely mirroring Switch layouts */
    .hp-box {
        position: absolute;
        background: white;
        border: 3px solid var(--nintendo-border);
        border-radius: 12px 0 12px 0;
        padding: 8px 12px 8px 15px;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.15);
        z-index: 10;
        min-width: 240px;
        /* Blur background slightly so it doesn't clash with the hyper-detailed AI art */
        backdrop-filter: blur(5px);
        background: rgba(255,255,255,0.95);
    }
    .player-hp { bottom: 30px; right: 30px; }
    .enemy-hp { top: 30px; left: 30px; }
    
    .hp-header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #eee; margin-bottom: 8px; padding-bottom: 2px; }
    .pkmn-name { font-weight: 900; font-size: 1.15rem; text-transform: capitalize; color: var(--nintendo-text); }
    .pkmn-level { font-weight: 800; font-size: 0.9rem; color: #555;}
    
    .hp-bar-container { display: flex; align-items: center; background: #555; border-radius: 10px; padding: 2px; border: 2px solid white; box-shadow: 0 0 0 2px var(--nintendo-border); }
    .hp-text { background: #ff9800; color: white; font-size: 0.7rem; font-weight: 900; padding: 0 5px; border-radius: 8px 0 0 8px; margin-right: 4px; }
    .hp-bar-track { flex-grow: 1; background: #444; height: 10px; border-radius: 5px; position: relative; overflow: hidden; margin-right: 2px;}
    .hp-bar-fill { height: 100%; transition: width 0.4s cubic-bezier(0.1, 0.7, 0.1, 1), background-color 0.4s; }
    .hp-numerical { text-align: right; font-weight: 800; font-size: 1.05rem; margin-top: 5px; letter-spacing: 0.5px; color: var(--nintendo-text); }

    /* Constrain the 3D layer to exactly lap over the grass (620px), so bottom-anchored shadows and sprites don't drift into the 180px HUD tray below! */
    .sprites-layer { position: absolute; width: 100%; height: 620px; top: 0; left: 0; z-index: 5; pointer-events: none;}
    
    /* Enemy stands far back ATOP the Pokeball ring */
    .sprite-opponent { position: absolute; top: 230px; right: 260px; z-index: 4; transform: scale(1.25); transform-origin: bottom center; }
    
    /* Player stands giant in the foreground ATOP the Pokeball ring */
    .sprite-player { position: absolute; bottom: 50px; left: 210px; z-index: 6; transform: scale(1.4); transform-origin: bottom center; }
    
    /* Realistic compressed shadow on the grass */
    .shadow { 
        position: absolute;
        bottom: -10px;
        left: 50%;
        width: 190px; height: 50px; 
        background: radial-gradient(ellipse at center, rgba(10, 30, 8, 0.85) 0%, rgba(15, 45, 12, 0.45) 40%, transparent 70%);
        border-radius: 50%; 
        transform: translateX(-50%) scaleY(0.4); 
        mix-blend-mode: multiply; 
        filter: blur(1px); 
        z-index: -1;
    }
    
    /* Battle Animations */
    @keyframes attack-right {
        0% { transform: translateX(0); }
        50% { transform: translateX(50px); }
        100% { transform: translateX(0); }
    }
    @keyframes attack-left {
        0% { transform: translateX(0) scaleX(-1); }
        50% { transform: translateX(-50px) scaleX(-1); }
        100% { transform: translateX(0) scaleX(-1); }
    }
    @keyframes flash-hit {
        0% { filter: brightness(1); transform: translateX(0); }
        25% { filter: brightness(2) drop-shadow(0 0px 20px rgba(255,0,0,1)); opacity: 0.6; transform: translateX(-5px); }
        50% { filter: brightness(1); transform: translateX(5px); }
        75% { filter: brightness(2) drop-shadow(0 0px 20px rgba(255,0,0,1)); opacity: 0.6; transform: translateX(-5px); }
        100% { filter: brightness(1); transform: translateX(0); }
    }
    
    .img-p1.attack { animation: attack-right 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .img-p2.attack { animation: attack-left 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .img.hit { animation: flash-hit 0.5s ease-in-out; }
    
    /* Game Dialogue Box for Action Log */
    [data-testid="stNotification"] {
        background: white !important;
        border: 4px solid var(--nintendo-border) !important;
        border-radius: 12px !important;
        color: var(--nintendo-text) !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800;
        font-size: 1.2rem !important;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.15) !important;
        padding: 15px 20px !important;
    }
    [data-testid="stNotification"] svg { display: none !important; }
    
    /* Aggressively destroy Streamlit's native loading-state component dimming during intense animation executions */
    div, span, [data-testid="stVerticalBlock"], [class*="st-emotion-cache"] {
        opacity: 1 !important;
        transition: none !important;
    }
    .stApp [data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.title("Pokemon Combat Simulator")

# API Functions
@st.cache_data
def fetch_pokemon_list():
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1500")
        response.raise_for_status()
        return [p["name"].capitalize() for p in response.json()["results"]]
    except requests.exceptions.RequestException:
        return ["Pikachu", "Charizard", "Bulbasaur", "Squirtle", "Mewtwo"]

@st.cache_data
def fetch_pokemon(name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

@st.cache_data
def fetch_move(name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/move/{name.lower()}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

@st.cache_data
def fetch_type(name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/type/{name.lower()}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

@st.cache_data
def get_hd_sprite(name):
    # Retrieve beautiful 3D model GIFs provided by the user's requested repository
    url = f"https://raw.githubusercontent.com/Nackha1/Hd-sprites/master/{name.capitalize()}.gif"
    try:
        if requests.head(url).status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None

import random

@st.cache_data
def get_four_damaging_moves(pokemon_moves):
    valid = []
    # shuffle moves to get random 4
    shuffled = random.sample(pokemon_moves, min(len(pokemon_moves), 40))
    for m_name in shuffled:
        m_data = fetch_move(m_name)
        if m_data and m_data.get("power") and m_data["power"] > 0:
            type_rel = fetch_type(m_data["type"]["name"])
            if type_rel:
                valid.append({
                    "name": m_data["name"],
                    "power": m_data["power"],
                    "accuracy": m_data.get("accuracy") if m_data.get("accuracy") is not None else 100,
                    "type": m_data["type"]["name"],
                    "damage_class": m_data["damage_class"]["name"],
                    "damage_relations": type_rel["damage_relations"]
                })
        if len(valid) == 4:
            break
    return valid

def get_base64_image(file_path):
    import base64
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception:
        return None

# Render Logo at the very top
logo_b64 = get_base64_image("logo.png")
if logo_b64:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: -20px; padding-top: 10px;">
            <img src="data:image/png;base64,{logo_b64}" width="400">
        </div>
        """,
        unsafe_allow_html=True
    )
# Helpers
# ---------
TYPE_COLORS = {
    "normal": "#A8A77A", "fire": "#EE8130", "water": "#6390F0",
    "electric": "#F7D02C", "grass": "#7AC74C", "ice": "#96D9D6",
    "fighting": "#C22E28", "poison": "#A33EA1", "ground": "#E2BF65",
    "flying": "#A98FF3", "psychic": "#F95587", "bug": "#A6B91A",
    "rock": "#B6A136", "ghost": "#735797", "dragon": "#6F35FC",
    "dark": "#705898", "steel": "#B7B7CE", "fairy": "#D685AD"
}

def get_type_badge(type_name):
    color = TYPE_COLORS.get(type_name.lower(), "#777")
    return f'<span class="type-badge" style="background-color: {color}; box-shadow: 0 0 10px {color}80;">{type_name.upper()}</span>'

def extract_pokemon_data(data):
    if not data:
        return None
        
    hd_sprite = get_hd_sprite(data["name"])
    
    # Attempt to get the 3D HD GIF, fallback to official PokeAPI animated GIF, final fallback to static
    if hd_sprite:
        sprite_front = hd_sprite
    else:
        try:
            sprite_front = data["sprites"]["other"]["showdown"]["front_default"]
        except KeyError:
            sprite_front = data["sprites"]["front_default"]
        
    return {
        "name": data["name"],
        "sprite": sprite_front,
        "types": [t["type"]["name"] for t in data["types"]],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
        "moves": [m["move"]["name"] for m in data["moves"]]
    }

# -----------------
# 1. Selection
# -----------------
st.header("1. Choose Your Pokemon")
col1, col2 = st.columns(2)

pokemon_list = fetch_pokemon_list()
p1_idx = pokemon_list.index("Mewtwo") if "Mewtwo" in pokemon_list else 0
p2_idx = pokemon_list.index("Venusaur") if "Venusaur" in pokemon_list else 1

with col1:
    pkmn1_name = st.selectbox("Player 1", options=pokemon_list, index=p1_idx)
with col2:
    pkmn2_name = st.selectbox("Player 2", options=pokemon_list, index=p2_idx)

# Always fetch and extract data for current selections
data1_raw = fetch_pokemon(pkmn1_name)
data2_raw = fetch_pokemon(pkmn2_name)

if not data1_raw or not data2_raw:
    st.error("Could not fetch data for one or both Pokemon. Please check the names and try again.")
    st.stop()

pkmn1 = extract_pokemon_data(data1_raw)
pkmn2 = extract_pokemon_data(data2_raw)

# -----------------
# 2. Display Stats
# -----------------
st.header("2. Pokémon Stats")
scol1, scol2 = st.columns(2)

def render_pokemon_card(pkmn):
    with st.container():
        st.subheader(pkmn["name"].capitalize())
        col_space1, col_img, col_space2 = st.columns([1,2,1])
        if pkmn["sprite"]:
            with col_img:
                st.markdown(f'<img src="{pkmn["sprite"]}" style="width:100%; max-width:150px; display:block; margin:auto;" />', unsafe_allow_html=True)
        badges_html = " ".join([get_type_badge(t) for t in pkmn['types']])
        st.markdown(f"**Types:** {badges_html}", unsafe_allow_html=True)
        st.caption(f"**HP** {pkmn['stats']['hp']} · **ATT** {pkmn['stats']['attack']} · **DEF** {pkmn['stats']['defense']} · **SPA** {pkmn['stats']['special-attack']} · **SPD** {pkmn['stats']['special-defense']} · **SPE** {pkmn['stats']['speed']}")

with scol1:
    render_pokemon_card(pkmn1)
with scol2:
    render_pokemon_card(pkmn2)

# -----------------
# 4. Stat Comparison
# -----------------
st.header("4. Head-to-Head Comparison")
stat_df = pd.DataFrame([
    {"pokemon": pkmn1["name"].capitalize(), **pkmn1["stats"]},
    {"pokemon": pkmn2["name"].capitalize(), **pkmn2["stats"]}
])
melted_stats = stat_df.melt(id_vars="pokemon", var_name="stat", value_name="value")
fig_stats = px.bar(
    melted_stats,
    x="stat", y="value", color="pokemon", barmode="group",
    color_discrete_sequence=["#0A84FF", "#FF453A"]
)
fig_stats.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font_color="#F5F5F7", margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_stats, use_container_width=True)

if not st.session_state.battle_active:
    if st.button("🚀 INITIATE COMBAT", type="primary", use_container_width=True):
        st.session_state.battle_active = True
        st.rerun()

st.markdown("---")

def init_battle(p1, p2):
    """Initialize or reset battle state for the given Pokémon."""
    st.session_state.battle_active = True
    st.session_state.hp1 = p1["stats"]["hp"] * 3
    st.session_state.hp2 = p2["stats"]["hp"] * 3
    st.session_state.max_hp1 = p1["stats"]["hp"] * 3
    st.session_state.max_hp2 = p2["stats"]["hp"] * 3
    st.session_state.p1_moves = get_four_damaging_moves(p1["moves"])
    st.session_state.p2_moves = get_four_damaging_moves(p2["moves"])
    st.session_state.game_over = False
    st.session_state.battle_log = []
    st.session_state.round_num = 1
    st.session_state.latest_action = f"A wild {p2['name'].capitalize()} appeared! What will {p1['name'].capitalize()} do?"
    st.session_state.active_p1_name = p1["name"]
    st.session_state.active_p2_name = p2["name"]
    # Tidy format history for Criterion 2 & 3
    st.session_state.hp_history = [
        {"Round": 0, "Pokemon": p1["name"].capitalize(), "HP": st.session_state.hp1},
        {"Round": 0, "Pokemon": p2["name"].capitalize(), "HP": st.session_state.hp2}
    ]

try:
    # Auto-start: initialize on first load, or reset when Pokémon selection changes
    pkmn_changed = (
        st.session_state.get("active_p1_name") != pkmn1["name"] or
        st.session_state.get("active_p2_name") != pkmn2["name"]
    )

    if "battle_active" not in st.session_state or pkmn_changed:
        init_battle(pkmn1, pkmn2)
        st.rerun()
except Exception as e:
    import traceback
    st.error(f"Error evaluating auto-start: {e}")
    st.code(traceback.format_exc())

# st.success("DEBUG: Reached section 5 start")

st.header("5. Battle Arena")

import base64
import os
bg_path = "arena_bg.jpg" # Using relative path for Streamlit Cloud compatibility
bg_inline = ""
if os.path.exists(bg_path):
    with open(bg_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    bg_inline = f"background-image: url('data:image/jpeg;base64,{encoded_string}'); background-size: 100% 100%; background-repeat: no-repeat; background-position: top center;"
else:
    bg_inline = "background-color: #a8d8a8;"

def get_arena_html(curr_hp1, curr_hp2, p1_cls="img-p1", p2_cls="img-p2"):
    f1 = max(0.0, min(1.0, curr_hp1 / st.session_state.max_hp1))
    f2 = max(0.0, min(1.0, curr_hp2 / st.session_state.max_hp2))
    
    c1 = '#4CAF50' if f1 > 0.5 else ('#FFC107' if f1 > 0.2 else '#F44336')
    c2 = '#4CAF50' if f2 > 0.5 else ('#FFC107' if f2 > 0.2 else '#F44336')
    
    # Check for faint animation classes
    p1_anim = "faint" if curr_hp1 <= 0 else ""
    p2_anim = "faint" if curr_hp2 <= 0 else ""
    
    p1_h = f'<div class="sprite-player {p1_anim}"><img src="{pkmn1["sprite"]}" class="{p1_cls}" style="width:180px; transform: scaleX(-1);" /><div class="shadow"></div></div>' if pkmn1.get('sprite') else ""
    p2_h = f'<div class="sprite-opponent {p2_anim}"><img src="{pkmn2["sprite"]}" class="{p2_cls}" style="width:180px;" /><div class="shadow"></div></div>' if pkmn2.get('sprite') else ""
    
    return f"""<div class="arena-container" style="{bg_inline}">
<div class="hp-box player-hp">
<div class="hp-header">
    <span class="pkmn-name">{pkmn1['name'].capitalize()}</span>
    <span class="pkmn-level">Lv. 50</span>
</div>
<div class="hp-bar-container">
    <div class="hp-text">HP</div>
    <div class="hp-bar-track">
        <div class="hp-bar-fill" style="width: {f1*100}%; background-color: {c1};"></div>
    </div>
</div>
<div class="hp-numerical">{int(curr_hp1)} / {int(st.session_state.max_hp1)}</div>
</div>

<div class="hp-box enemy-hp">
<div class="hp-header">
    <span class="pkmn-name">{pkmn2['name'].capitalize()}</span>
    <span class="pkmn-level">Lv. 50</span>
</div>
<div class="hp-bar-container">
    <div class="hp-text">HP</div>
    <div class="hp-bar-track">
        <div class="hp-bar-fill" style="width: {f2*100}%; background-color: {c2};"></div>
    </div>
</div>
</div>

<div class="sprites-layer">
{p2_h}
{p1_h}
</div>
</div>"""

# Define the dialogue helper
def get_dialogue_html(msg):
    return f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f9fbfe 100%);
        border: 1.5px solid #d1d9e0;
        border-top: 2px solid #ffffff;
        border-radius: 14px;
        padding: 22px 28px;
        margin: 0;
        height: 130px;
        box-shadow: 
            0 8px 24px rgba(0,0,0,0.03), 
            inset 0 1px 3px rgba(0,0,0,0.05),
            inset 0 -2px 0 rgba(0,0,0,0.02);
        display: flex;
        align-items: center;
        position: relative;
        box-sizing: border-box;
        width: 100%;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: rgba(255,255,255,0.8);
        "></div>
        <div style="font-family: 'Inter', 'Helvetica Neue', sans-serif; font-size: 18px; font-weight: 700; color: #34495e; line-height: 1.4; letter-spacing: -0.2px;">
            {msg}
        </div>
        <span style="position: absolute; bottom: 16px; right: 20px; color: #3498db; font-size: 20px; animation: bounce 1.5s infinite; filter: drop-shadow(0 2px 4px rgba(52,152,219,0.3));">▼</span>
    </div>
    """

# -------------------------------------------------------
# Control Panel: separate styled grey container below arena
# -------------------------------------------------------
# Inject the panel CSS — targets the stHorizontalBlock that contains .hud-sentinel
st.markdown("""
<style>
/* CONTROL PANEL CONTAINER */
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) {
    background: #f0f3f7 !important;
    border: 2px solid #d8dde3 !important;
    border-radius: 20px !important;
    padding: 30px 48px !important; /* Fixed, stable padding for symmetry */
    box-sizing: border-box !important;
    align-items: center !important;
    overflow: hidden !important;
    min-height: 190px !important; /* 30+30+130 = 190 exactly */
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.02) !important;
}
.hud-sentinel { display: none !important; }

/* Left column padding */
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) > div[data-testid="column"] {
    padding: 0 !important;
    margin: 0 !important;
}
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) > div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 20px 20px !important; /* Match vertical gap to padding logic */
    padding: 0 !important;
    margin: 0 !important;
    box-sizing: border-box !important;
    width: 100% !important;
    overflow: hidden !important;
}
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) > div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    width: 100% !important;
    min-width: 0 !important;
    flex: 1 1 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
}
/* BUTTONS */
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) button {
    width: 100% !important;
    height: 55px !important;
    min-width: 0 !important;
    background: linear-gradient(180deg, #ffffff 0%, #f7f9fa 100%) !important;
    border: 1.5px solid #d8dde3 !important;
    border-top: 1px solid #ffffff !important;
    border-radius: 12px !important;
    box-shadow: 
        0 4px 6px rgba(0,0,0,0.04), 
        0 2px 4px rgba(0,0,0,0.02),
        inset 0 1px 0 rgba(255,255,255,0.9) !important;
    box-sizing: border-box !important;
    padding: 0 4px !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    transition: all 0.15s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) button:hover {
    border-color: #c0c9d1 !important;
    background: linear-gradient(180deg, #ffffff 0%, #edf2f5 100%) !important;
    box-shadow: 
        0 8px 15px rgba(0,0,0,0.06), 
        0 3px 6px rgba(0,0,0,0.03),
        inset 0 1px 0 rgba(255,255,255,1) !important;
    transform: translateY(-3px) !important;
}
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) button:focus,
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) button:active,
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) [data-testid="stButton"]:focus-within button {
    outline: none !important;
    border-color: #3296ff !important;
    box-shadow: 
        0 0 0 3px rgba(50, 150, 255, 0.15),
        0 8px 20px rgba(50, 150, 255, 0.1),
        inset 0 1px 0 rgba(255,255,255,1) !important;
    background: linear-gradient(180deg, #ffffff 0%, #f0f7ff 100%) !important;
}
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) button p {
    white-space: pre-line !important;
    word-break: break-word !important;
    text-align: center !important;
    margin: 0 !important;
    line-height: 1.15 !important;
    font-family: 'Inter', 'Helvetica Neue', sans-serif !important;
    color: #8a96a3 !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    transition: color 0.15s ease !important;
}
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) button:hover p {
    color: #7b8691 !important;
}
div[data-testid="stHorizontalBlock"]:has(.hud-sentinel) button p::first-line {
    font-size: 13px !important;
    font-weight: 800 !important;
    color: #34495e !important;
}
</style>
""", unsafe_allow_html=True)
# --- BATTLE AREA (ARENA + HUD) ---
# @st.fragment ensures only this section reruns on button press — sections 1-4 stay frozen
@st.fragment
def battle_section():
    if not st.session_state.battle_active:
        return

    if not st.session_state.game_over:
        # Render directly — no outer st.empty() wrapper that could flash blank
        arena_view = st.empty()
        arena_view.markdown(get_arena_html(st.session_state.hp1, st.session_state.hp2), unsafe_allow_html=True)
        
        hud_cols = st.columns([1.5, 1])
        with hud_cols[0]:
            st.markdown('<div class="hud-sentinel"></div>', unsafe_allow_html=True)
            notification_box = st.empty()
            notification_box.markdown(get_dialogue_html(st.session_state.latest_action), unsafe_allow_html=True)
            
        move_btn_ph = hud_cols[1].empty()
        def execute_move(p1_move):
            import time
            if not st.session_state.p2_moves: return
            p2_move = random.choice(st.session_state.p2_moves)
            
            speed1 = pkmn1["stats"]["speed"]
            speed2 = pkmn2["stats"]["speed"]
            if speed1 > speed2 or (speed1 == speed2 and random.choice([True, False])):
                turn_order = [(1, pkmn1, pkmn2, p1_move), (2, pkmn2, pkmn1, p2_move)]
            else:
                turn_order = [(2, pkmn2, pkmn1, p2_move), (1, pkmn1, pkmn2, p1_move)]
                
            curr_hp1, curr_hp2 = st.session_state.hp1, st.session_state.hp2
            
            for idx, attacker, defender, move in turn_order:
                if (idx == 1 and curr_hp1 <= 0) or (idx == 2 and curr_hp2 <= 0):
                    continue
                
                dr = move["damage_relations"]
                eff = 1.0
                for t in defender["types"]:
                    if t in [x["name"] for x in dr["double_damage_to"]]: eff *= 2.0
                    elif t in [x["name"] for x in dr["half_damage_to"]]: eff *= 0.5
                    elif t in [x["name"] for x in dr["no_damage_to"]]: eff *= 0.0
                
                att_val = attacker["stats"]["attack"] if move["damage_class"] == "physical" else attacker["stats"]["special-attack"]
                def_val = defender["stats"]["defense"] if move["damage_class"] == "physical" else defender["stats"]["special-defense"]
                
                dmg = 0
                if random.random() < (move["accuracy"] / 100.0):
                    dmg = max(1, int(((2 * 50 / 5 + 2) * move["power"] * (att_val / def_val) / 50 + 2) * eff))
                
                prefix = "Enemy " if idx == 2 else ""
                msg = f"{prefix}**{attacker['name'].capitalize()}** used {move['name'].capitalize()}! "
                if dmg == 0: msg += "It missed!"
                else:
                    if eff > 1: msg += "It's super effective!"
                    elif eff < 1 and eff > 0: msg += "It's not very effective..."
                    elif eff == 0: msg += "It had no effect!"
                
                notification_box.markdown(get_dialogue_html(msg), unsafe_allow_html=True)
                p1_c, p2_c = ("img-p1 attack", "img-p2") if idx == 1 else ("img-p1", "img-p2 attack")
                arena_view.markdown(get_arena_html(curr_hp1, curr_hp2, p1_cls=p1_c, p2_cls=p2_c), unsafe_allow_html=True)
                time.sleep(0.4)
                
                if idx == 1:
                    curr_hp2 = max(0, curr_hp2 - dmg)
                    if dmg > 0: arena_view.markdown(get_arena_html(curr_hp1, curr_hp2, p1_cls="img-p1", p2_cls="img-p2 hit"), unsafe_allow_html=True)
                else:
                    curr_hp1 = max(0, curr_hp1 - dmg)
                    if dmg > 0: arena_view.markdown(get_arena_html(curr_hp1, curr_hp2, p1_cls="img-p1 hit", p2_cls="img-p2"), unsafe_allow_html=True)
                time.sleep(0.5)
                
                arena_view.markdown(get_arena_html(curr_hp1, curr_hp2), unsafe_allow_html=True)
                time.sleep(0.5)
                
                st.session_state.battle_log.append({"round": st.session_state.round_num,"attacker": attacker["name"].capitalize(),"move": move["name"].capitalize(),"damage": dmg})
                
                if curr_hp1 <= 0 or curr_hp2 <= 0:
                    st.session_state.game_over = True
                    break
                    
            st.session_state.hp1, st.session_state.hp2 = curr_hp1, curr_hp2
            st.session_state.hp_history.append({"Round": st.session_state.round_num, "Pokemon": pkmn1["name"].capitalize(), "HP": curr_hp1})
            st.session_state.hp_history.append({"Round": st.session_state.round_num, "Pokemon": pkmn2["name"].capitalize(), "HP": curr_hp2})
            st.session_state.round_num += 1
            
            if st.session_state.game_over:
                if curr_hp1 <= 0 and curr_hp2 <= 0: final_msg = "**It's a draw!**"
                elif curr_hp1 <= 0: final_msg = f"**Your {pkmn1['name'].capitalize()} fainted! You blacked out!**"
                else: final_msg = f"**Enemy {pkmn2['name'].capitalize()} fainted! You won!**"
                st.session_state.latest_action = final_msg
                notification_box.markdown(get_dialogue_html(final_msg), unsafe_allow_html=True)
                time.sleep(1.2)
                st.rerun()
            else:
                st.session_state.latest_action = f"What will {pkmn1['name'].capitalize()} do?"
                notification_box.markdown(get_dialogue_html(st.session_state.latest_action), unsafe_allow_html=True)

        with move_btn_ph.container():
            btn_cols = st.columns(2)
            for i, move in enumerate(st.session_state.p1_moves):
                col = btn_cols[i % 2]
                with col:
                    m_type = move['type'].lower()
                    m_color = TYPE_COLORS.get(m_type, "#d8dde3")
                    st.markdown(f"""
<style>
div[data-testid="column"]:nth-child(2) button:has(p:contains("{move['name'].capitalize()}")) {{
    border-left: 8px solid {m_color} !important;
}}
</style>
""", unsafe_allow_html=True)
                    btn_label = f"{move['name'].upper()}\n{move['type'].capitalize()} • {move['power']} Pw"
                    if st.button(btn_label, key=f"btn_m_{i}", use_container_width=True):
                        execute_move(move)


    else:
        st.markdown("### Battle Log Output")
        col_reset, col_spacer = st.columns([1, 4])
        with col_reset:
            if st.button("Reset Battle", type="primary", use_container_width=True, key="reset_btn_final"):
                if "battle_active" in st.session_state:
                    del st.session_state["battle_active"]
                st.rerun()
                
        if st.session_state.battle_log:
            st.subheader("📝 Battle Results & Analysis")
            log_col, chart_col = st.columns([1, 1])
            with log_col:
                st.markdown("**Battle Log**")
                log_df = pd.DataFrame(st.session_state.battle_log)
                st.dataframe(log_df, use_container_width=True)
            with chart_col:
                st.markdown("**HP Progression (Tidy Format)**")
                hp_df = pd.DataFrame(st.session_state.hp_history)
                fig_hp = px.line(hp_df, x="Round", y="HP", color="Pokemon", markers=True,
                                 title="HP Drainage Over Time",
                                 color_discrete_map={pkmn1["name"].capitalize(): "#3296ff", pkmn2["name"].capitalize(): "#ff4b4b"})
                fig_hp.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_hp, use_container_width=True)

battle_section()
