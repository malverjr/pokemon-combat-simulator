import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import random
import time

# Apply layout constraints
st.set_page_config(page_title="Pokemon Combat Simulator", page_icon="⚔️", layout="wide")

if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    splash_ph = st.empty()
    with splash_ph.container():
        st.markdown('''
        <style>
        div[data-testid="stVideo"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 999998 !important;
            pointer-events: none !important;
            background: black;
        }
        div[data-testid="stVideo"] video {
            object-fit: cover !important;
            width: 100% !important;
            height: 100% !important;
        }
        .splash-logo-container {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            z-index: 999999 !important;
            text-align: center !important;
            width: 100%;
            pointer-events: none;
        }
        .splash-logo-container img {
            width: 80vw;
            max-width: 700px;
            filter: drop-shadow(0px 0px 30px rgba(0,0,0,1));
            animation: pulse-splash 1.5s infinite ease-in-out;
        }
        @keyframes pulse-splash {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        header { display: none !important; }
        div[data-testid="stAppViewContainer"] {
            background-color: black !important;
        }
        </style>
        <div class="splash-logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pok%C3%A9mon_logo.svg">
        </div>
        ''', unsafe_allow_html=True)
        st.video("mylivewallpapers-com-Fire-Breathing-Charizard-3440x1440.mp4", autoplay=True, muted=True, loop=True)
    
    time.sleep(3.5)
    st.session_state.splash_shown = True
    st.rerun()

# Inject Custom "Apple Pro" Premium CSS
st.markdown("""
<style>
    /* Apple Pro Global Variables */
    :root {
        --apple-bg: #000000;
        --apple-card: #1c1c1e;
        --apple-border: rgba(255, 255, 255, 0.1);
    }
    
    .stApp {
        background-color: var(--apple-bg) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif !important;
    }
    
    header {visibility: hidden;}
    
    /* Desktop Title */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.015em !important;
        background: linear-gradient(180deg, #FFFFFF 0%, #A1A1A6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem !important;
        font-size: 3rem !important;
    }
    
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 980px !important; 
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: transform 0.2s ease, filter 0.2s ease !important;
        width: 100%;
        margin-top: 10px;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        filter: brightness(1.2);
    }
    
    /* Health Bars Override to Apple Green/Red based on level */
    .stProgress > div > div > div > div {
        background-color: #34C759 !important; 
        transition: width 0.4s ease-in-out !important;
    }
    
    /* Clean Images */
    img {
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
    }
    
    /* Battle Arena Background */
    .arena-container {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/e/e0/Placeholder_arena.jpg"); /* Temporary fallback */
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        padding: 40px 20px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
        border: 2px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
        position: relative;
    }
    
    .arena-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.4); /* Dark overlay to make sprites pop */
        border-radius: 15px;
        z-index: 0;
    }
    
    .sprite-wrapper {
        position: relative;
        z-index: 1;
    }
    /* Battle Animations */
    @keyframes attack-right {
        0% { transform: translateX(0); }
        50% { transform: translateX(30px) scale(1.1); }
        100% { transform: translateX(0); }
    }
    @keyframes attack-left {
        0% { transform: translateX(0); }
        50% { transform: translateX(-30px) scale(1.1); }
        100% { transform: translateX(0); }
    }
    @keyframes flash-hit {
        0% { filter: brightness(1) drop-shadow(0 10px 15px rgba(0,0,0,0.5)); }
        50% { filter: brightness(2) invert(0.2) drop-shadow(0 0px 20px rgba(255,0,0,0.8)); opacity: 0.7; }
        100% { filter: brightness(1) drop-shadow(0 10px 15px rgba(0,0,0,0.5)); }
    }
    
    .img-p1.attack { animation: attack-right 0.3s ease-in-out; }
    .img-p2.attack { animation: attack-left 0.3s ease-in-out; }
    .img.hit { animation: flash-hit 0.4s ease-in-out; }
</style>
""", unsafe_allow_html=True)

st.title("Pokemon Combat Simulator")

# API Functions
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

# Helpers
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

with col1:
    pkmn1_name = st.text_input("Player 1", value="pikachu")
with col2:
    pkmn2_name = st.text_input("Player 2", value="charizard")

data1_raw = fetch_pokemon(pkmn1_name)
data2_raw = fetch_pokemon(pkmn2_name)

if not data1_raw or not data2_raw:
    st.error("Could not fetch data for one or both Pokemon. Please check the names and try again.")
    st.stop()

pkmn1 = extract_pokemon_data(data1_raw)
pkmn2 = extract_pokemon_data(data2_raw)

# -----------------
# 2 & 3. Display & Moves
# -----------------
st.header("2. Analysis & Moves")
col1, col2 = st.columns(2)

def render_pokemon_card(pkmn, key_prefix):
    with st.container():
        st.subheader(pkmn["name"].capitalize())
        
        # Display the sprite/GIF with some centered spacing using native HTML to force GIF animations to play
        col_space1, col_img, col_space2 = st.columns([1,2,1])
        if pkmn["sprite"]:
            with col_img:
                st.markdown(f'<img src="{pkmn["sprite"]}" style="width:100%; max-width:150px; display:block; margin:auto;" />', unsafe_allow_html=True)
        
        # Apple pro style tags could go here but plain text is clean
        st.caption(f"**Types**: {', '.join(pkmn['types']).title()}")
        st.caption(f"**HP** {pkmn['stats']['hp']} · **ATT** {pkmn['stats']['attack']} · **DEF** {pkmn['stats']['defense']} · **SPA** {pkmn['stats']['special-attack']} · **SPD** {pkmn['stats']['special-defense']} · **SPE** {pkmn['stats']['speed']}")
        
        # Filter valid damaging moves using user selection
        selected_move_name = st.selectbox("Assign Move", pkmn["moves"], key=f"{key_prefix}_move")
        move_data = fetch_move(selected_move_name)
        
        if move_data:
            power = move_data.get("power")
            accuracy = move_data.get("accuracy")
            move_type = move_data["type"]["name"]
            damage_class = move_data["damage_class"]["name"]
            
            # Verify it's a damaging move
            if power is None or power == 0:
                st.warning(f"Status moves (0 damage) cannot be used in this simulator. Please choose a damaging attack.")
                return None
                
            st.markdown(f"> **{power} Pw** | **{accuracy if accuracy else '100'}% Acc** | {move_type.capitalize()} Type ({damage_class.capitalize()})")
            
            return {
                "name": selected_move_name,
                "power": power,
                "accuracy": accuracy if accuracy else 100,
                "type": move_type,
                "damage_class": damage_class
            }
        return None

with col1:
    move1_info = render_pokemon_card(pkmn1, "p1")
with col2:
    move2_info = render_pokemon_card(pkmn2, "p2")

# -----------------
# 4. Stat Comparison
# -----------------
st.header("4. Head-to-Head Comparison")
stat_df = pd.DataFrame([
    {"pokemon": pkmn1["name"].capitalize(), **pkmn1["stats"]},
    {"pokemon": pkmn2["name"].capitalize(), **pkmn2["stats"]}
])
melted_stats = stat_df.melt(id_vars="pokemon", var_name="stat", value_name="value")

# Theming Plotly to match Apple dark aesthetics
fig_stats = px.bar(
    melted_stats, 
    x="stat", y="value", color="pokemon", barmode="group",
    color_discrete_sequence=["#0A84FF", "#FF453A"] # Apple blue and red
)
fig_stats.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#F5F5F7",
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_stats, use_container_width=True)

# -----------------
# 5. Combat Engine
# -----------------
if move1_info and move2_info:
    st.markdown("---")
    st.header("5. Battle Arena")
    
    if st.button("Battle!", type="primary"):
        st.subheader("Live Combat")
        
        import base64
        import os
        
        # We use a single empty container to inject the full HTML block so we can animate it easily
        arena_view = st.empty()
        
        bg_css = ""
        bg_path = "arena_bg.png"
        if os.path.exists(bg_path):
            with open(bg_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            bg_css = f"background-image: url('data:image/png;base64,{encoded_string}');"
        else:
            bg_css = 'background-color: #333;'
            
        def render_arena_clean(p1_img_src, p2_img_src, p1_cls="img-p1", p2_cls="img-p2"):
            p1_html = f'<img src="{p1_img_src}" class="{p1_cls}" style="width:150px; display:block; margin:auto; transform: scaleX(-1);" />' if p1_img_src else ""
            p2_html = f'<img src="{p2_img_src}" class="{p2_cls}" style="width:150px; display:block; margin:auto;" />' if p2_img_src else ""
            
            arena_html = f"""
            <div class="arena-container" style="{bg_css}">
                <div style="display: flex; justify-content: space-around; align-items: flex-end; height: 200px; position:relative; z-index:1;">
                    <div style="text-align:center; text-shadow: 2px 2px 4px #000;">
                        <h3 style="color:white; margin-bottom:10px;">{pkmn1['name'].capitalize()}</h3>
                        {p1_html}
                    </div>
                    <div style="text-align:center; text-shadow: 2px 2px 4px #000;">
                        <h3 style="color:white; margin-bottom:10px;">{pkmn2['name'].capitalize()}</h3>
                        {p2_html}
                    </div>
                </div>
            </div>
            """
            arena_view.markdown(arena_html, unsafe_allow_html=True)
            
        render_arena_clean(pkmn1.get('sprite'), pkmn2.get('sprite'))
        
        
        hp_col1, hp_col2 = st.columns(2)
        with hp_col1:
            p1_bar = st.empty()
        with hp_col2:
            p2_bar = st.empty()
            
        action_log = st.empty()
        
        # Pre-calc Effectiveness
        type_data_1 = fetch_type(move1_info["type"])
        type_data_2 = fetch_type(move2_info["type"])
        
        def calculate_effectiveness(move_type_data, defender_types):
            dr = move_type_data["damage_relations"]
            double_damage = [t["name"] for t in dr["double_damage_to"]]
            half_damage = [t["name"] for t in dr["half_damage_to"]]
            no_damage = [t["name"] for t in dr["no_damage_to"]]
            
            effectiveness = 1.0
            for t in defender_types:
                if t in double_damage:
                    effectiveness *= 2.0
                elif t in half_damage:
                    effectiveness *= 0.5
                elif t in no_damage:
                    effectiveness *= 0.0
            return effectiveness
        
        eff1 = calculate_effectiveness(type_data_1, pkmn2["types"])
        eff2 = calculate_effectiveness(type_data_2, pkmn1["types"])
        
        level = 50
        def calculate_damage(attacker, defender, move, effectiveness):
            if move["damage_class"] == "physical":
                att_stat = attacker["stats"]["attack"]
                def_stat = defender["stats"]["defense"]
            else:
                att_stat = attacker["stats"]["special-attack"]
                def_stat = defender["stats"]["special-defense"]
                
            if random.random() < (move["accuracy"] / 100.0):
                damage = int(((2 * level / 5 + 2) * move["power"] * (att_stat / def_stat) / 50 + 2) * effectiveness)
                return max(1, damage)
            return 0 
            
        # In real pokemon games, Base HP is scaled heavily by level (Base * 2 + Level + 10) compared to raw attack damage.
        # We multiply the raw parsed Base HP by 3 to simulate a proper battle duration without altering the strict rubric damage formula.
        hp1 = max_hp1 = pkmn1["stats"]["hp"] * 3
        hp2 = max_hp2 = pkmn2["stats"]["hp"] * 3
        
        speed1 = pkmn1["stats"]["speed"]
        speed2 = pkmn2["stats"]["speed"]
        
        battle_log = []
        hp_history = [
            {"round": 0, "pokemon": pkmn1["name"].capitalize(), "hp": hp1},
            {"round": 0, "pokemon": pkmn2["name"].capitalize(), "hp": hp2}
        ]
        
        round_num = 1
        
        if speed1 > speed2:
            turn_order = [(1, pkmn1, pkmn2, move1_info, eff1), (2, pkmn2, pkmn1, move2_info, eff2)]
        elif speed2 > speed1:
            turn_order = [(2, pkmn2, pkmn1, move2_info, eff2), (1, pkmn1, pkmn2, move1_info, eff1)]
        else:
            if random.choice([True, False]):
                turn_order = [(1, pkmn1, pkmn2, move1_info, eff1), (2, pkmn2, pkmn1, move2_info, eff2)]
            else:
                turn_order = [(2, pkmn2, pkmn1, move2_info, eff2), (1, pkmn1, pkmn2, move1_info, eff1)]
                
        # Generate entire simulation strictly beforehand to satisfy assignment DataFrame requirement cleanly
        while hp1 > 0 and hp2 > 0 and round_num <= 100:
            for index, attacker, defender, move, eff in turn_order:
                if index == 1 and hp1 <= 0: continue
                if index == 2 and hp2 <= 0: continue
                
                dmg = calculate_damage(attacker, defender, move, eff)
                
                if index == 1:
                    hp2 = max(0, hp2 - dmg)
                    def_hp = hp2
                else:
                    hp1 = max(0, hp1 - dmg)
                    def_hp = hp1
                    
                msg = f"**{attacker['name'].capitalize()}** used {move['name'].capitalize()}! "
                if dmg == 0:
                    msg += "It missed!"
                else:
                    msg += f"Dealt {dmg} dmg. "
                    if eff > 1: msg += "Super effective!"
                    elif eff < 1 and eff > 0: msg += "Not very effective..."
                    elif eff == 0: msg += "No effect!"
                    
                battle_log.append({
                    "round": round_num,
                    "attacker": attacker["name"].capitalize(),
                    "move": move["name"].capitalize(),
                    "damage": dmg,
                    "defender_hp": def_hp,
                    "message": msg,
                    "hp1_current": hp1,
                    "hp2_current": hp2
                })
                
                if hp1 <= 0 or hp2 <= 0:
                    break
                    
            hp_history.append({"round": round_num, "pokemon": pkmn1["name"].capitalize(), "hp": hp1})
            hp_history.append({"round": round_num, "pokemon": pkmn2["name"].capitalize(), "hp": hp2})
            round_num += 1
            
        # UI Animation Loop
        st.caption("Simulation rendering...")
        p1_bar.progress(1.0, text=f"HP: {max_hp1}/{max_hp1}")
        p2_bar.progress(1.0, text=f"HP: {max_hp2}/{max_hp2}")
        
        for action in battle_log:
            time.sleep(0.3)
            action_log.info(action["message"], icon="⚡")
            
            attacker_is_p1 = (action["attacker"] == pkmn1["name"].capitalize())
            
            if attacker_is_p1:
                render_arena_clean(pkmn1.get('sprite'), pkmn2.get('sprite'), p1_cls="img-p1 attack", p2_cls="img-p2")
                time.sleep(0.15)
                if action["damage"] > 0:
                    render_arena_clean(pkmn1.get('sprite'), pkmn2.get('sprite'), p1_cls="img-p1", p2_cls="img-p2 hit")
            else:
                render_arena_clean(pkmn1.get('sprite'), pkmn2.get('sprite'), p1_cls="img-p1", p2_cls="img-p2 attack")
                time.sleep(0.15)
                if action["damage"] > 0:
                    render_arena_clean(pkmn1.get('sprite'), pkmn2.get('sprite'), p1_cls="img-p1 hit", p2_cls="img-p2")
                    
            time.sleep(0.3)
            # Reset
            render_arena_clean(pkmn1.get('sprite'), pkmn2.get('sprite'))

            # Animate HP bars
            frac1 = max(0.0, min(1.0, action["hp1_current"] / max_hp1))
            frac2 = max(0.0, min(1.0, action["hp2_current"] / max_hp2))
            
            p1_bar.progress(frac1, text=f"HP: {action['hp1_current']}/{max_hp1}")
            p2_bar.progress(frac2, text=f"HP: {action['hp2_current']}/{max_hp2}")
            
        action_log.empty() # Clear transient messages
        
        # Winner declaration without balloons 
        if hp1 <= 0 and hp2 <= 0:
            st.success("⚔️ It's a draw!")
        elif hp1 <= 0:
            st.success(f"🏆 {pkmn2['name'].capitalize()} wins the battle!")
        elif hp2 <= 0:
            st.success(f"🏆 {pkmn1['name'].capitalize()} wins the battle!")
            
        # Show Full Log DataFrame
        st.markdown("### Battle Log Output")
        log_df = pd.DataFrame([{k: v for k, v in row.items() if k not in ("hp1_current", "hp2_current")} for row in battle_log])
        st.dataframe(log_df, use_container_width=True)
        
        # -----------------
        # 6. HP Chart
        # -----------------
        st.header("6. Timeline")
        hp_df = pd.DataFrame(hp_history)
        fig_hp = px.line(hp_df, x="round", y="hp", color="pokemon", markers=True, color_discrete_sequence=["#0A84FF", "#FF453A"])
        fig_hp.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#F5F5F7"
        )
        st.plotly_chart(fig_hp, use_container_width=True)

else:
    st.info("Please select a valid damaging move for both combatants to initiate the sequence.")
