import streamlit as st
from datetime import datetime
import random

# Initialisierung Session State
if 'players' not in st.session_state:
    st.session_state.players = {
        'Max Mustermann': {'level': 5, 'xp': 250, 'checkin': False, 'wins': 3, 'matches': 8},
        'Lisa Schmidt': {'level': 8, 'xp': 780, 'checkin': False, 'wins': 12, 'matches': 15},
        'Tom Wagner': {'level': 3, 'xp': 120, 'checkin': False, 'wins': 1, 'matches': 4},
    }

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'role' not in st.session_state:
    st.session_state.role = None

if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = None

if 'match_state' not in st.session_state:
    st.session_state.match_state = {'p1': 0, 'p2': 0, 'set': 1}

# Übungskatalog
EXERCISES = {
    'Beinarbeit': [
        {'name': 'Seitwärts-Shuffle', 'desc': '10x von Vorhand zu Rückhand gleiten', 'xp': 15},
        {'name': 'Kreuzschritt', 'desc': '15 Wiederholungen pro Seite', 'xp': 20},
        {'name': 'Stern-Übung', 'desc': 'Aus Tischmitte zu allen 4 Ecken', 'xp': 25},
    ],
    'Technik': [
        {'name': 'Vorhand Topspin', 'desc': '20 Bälle diagonal spielen', 'xp': 20},
        {'name': 'Rückhand Block', 'desc': '30 Ballwechsel halten', 'xp': 15},
        {'name': 'Schupf-Serie', 'desc': '15 präzise Schüsse auf Markierung', 'xp': 25},
    ],
    'Aufschlag': [
        {'name': 'Pendel-Aufschlag', 'desc': '10 Aufschläge mit Seitenrotation', 'xp': 15},
        {'name': 'Tomahawk', 'desc': '8 erfolgreiche Aufschläge', 'xp': 30},
        {'name': 'Kurz-Kurz', 'desc': '12 Aufschläge die 2x das Netz berühren', 'xp': 20},
    ],
    'Taktik': [
        {'name': 'Winner-Drill', 'desc': 'Aufbau -> Eröffnung -> Abschluss (5x)', 'xp': 35},
        {'name': 'Anti-Topspin', 'desc': 'Blockieren und kontern (3 Minuten)', 'xp': 25},
    ]
}

BADGES = {
    'first_checkin': '🎯 Willkommen',
    'level_10': '⭐ Level 10 erreicht',
    'streak_10': '🔥 10 Trainings in Folge',
    'first_win': '🏆 Erster Sieg',
}

# Funktionen
def award_xp(player_name, xp_amount):
    player = st.session_state.players[player_name]
    player['xp'] += xp_amount
    while player['xp'] >= 100:
        player['xp'] -= 100
        player['level'] += 1
        st.balloons()
        st.success(f"🎉 Level Up! Du bist jetzt Level {player['level']}!")

def get_random_exercise(player_level):
    category = random.choice(list(EXERCISES.keys()))
    exercises = EXERCISES[category]
    return random.choice(exercises), category

def calculate_handicap(level1, level2):
    diff = abs(level1 - level2)
    if diff <= 2:
        return 0, 0
    handicap = min(diff - 2, 5)
    if level1 > level2:
        return 0, handicap
    else:
        return handicap, 0

# UI Start
st.title("🏓 TT-Pro Vereins-App")

# Rollen-Auswahl
if st.session_state.role is None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 Spieler Login", use_container_width=True):
            st.session_state.role = 'player'
            st.rerun()
    with col2:
        if st.button("🎓 Trainer Login", use_container_width=True):
            st.session_state.role = 'trainer'
            st.rerun()
    st.stop()

# Zurück Button
if st.button("← Zurück zur Startseite"):
    st.session_state.role = None
    st.session_state.current_user = None
    st.rerun()

# ===== SPIELER BEREICH =====
if st.session_state.role == 'player':
    if st.session_state.current_user is None:
        st.header("Check-In")
        st.write("Wähle deinen Namen aus:")
        for name in st.session_state.players.keys():
            if st.button(f"✅ {name}", key=f"checkin_{name}", use_container_width=True):
                st.session_state.players[name]['checkin'] = True
                st.session_state.current_user = name
                st.rerun()
    else:
        user = st.session_state.current_user
        player = st.session_state.players[user]
        
        st.success(f"Eingeloggt als: **{user}**")
        st.metric("Level", player['level'])
        st.progress(player['xp'] / 100)
        st.caption(f"{player['xp']}/100 XP bis zum nächsten Level")
        
        # Tabs für Module
        tab1, tab2, tab3 = st.tabs(["🎯 Training", "⚔️ Wettkampf", "👤 Profil"])
        
        with tab1:
            st.subheader("Digitaler Coach")
            if st.session_state.current_exercise is None:
                if st.button("🎲 Neue Übung generieren", use_container_width=True):
                    exercise, category = get_random_exercise(player['level'])
                    st.session_state.current_exercise = {'ex': exercise, 'cat': category}
                    st.rerun()
            else:
                ex = st.session_state.current_exercise['ex']
                cat = st.session_state.current_exercise['cat']
                
                st.info(f"**Kategorie:** {cat}")
                st.markdown(f"### {ex['name']}")
                st.write(ex['desc'])
                st.caption(f"Belohnung: {ex['xp']} XP")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Übung abgeschlossen", use_container_width=True):
                        award_xp(user, ex['xp'])
                        st.session_state.current_exercise = None
                        st.rerun()
                with col2:
                    if st.button("🔄 Andere Übung", use_container_width=True):
                        st.session_state.current_exercise = None
                        st.rerun()
        
        with tab2:
            st.subheader("Battle Zone")
            match = st.session_state.match_state
            
            opponent = st.selectbox("Gegner wählen:", 
                                   [n for n in st.session_state.players.keys() if n != user])
            
            mode = st.radio("Spielmodus:", ["Standard (bis 11)", "Handicap", "Druck (9:9)"])
            
            if mode == "Handicap" and opponent:
                h1, h2 = calculate_handicap(player['level'], 
                                           st.session_state.players[opponent]['level'])
                st.info(f"Handicap: {user} startet bei {h1} - {opponent} bei {h2}")
            
            col1, col2, col3 = st.columns([2,1,2])
            with col1:
                st.markdown(f"### {user}")
                st.markdown(f"# {match['p1']}")
                if st.button("➕ Punkt", key="p1", use_container_width=True):
                    match['p1'] += 1
            with col2:
                st.markdown("### vs")
                st.caption(f"Satz {match['set']}")
            with col3:
                st.markdown(f"### {opponent}")
                st.markdown(f"# {match['p2']}")
                if st.button("➕ Punkt", key="p2", use_container_width=True):
                    match['p2'] += 1
            
            if st.button("🔄 Spiel zurücksetzen", use_container_width=True):
                st.session_state.match_state = {'p1': 0, 'p2': 0, 'set': 1}
                st.rerun()
        
        with tab3:
            st.subheader("Mein Profil")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Level", player['level'])
            with col2:
                st.metric("Siege", player['wins'])
            with col3:
                winrate = int((player['wins']/player['matches']*100)) if player['matches'] > 0 else 0
                st.metric("Siegquote", f"{winrate}%")
            
            st.divider()
            st.write("**Errungene Badges:**")
            st.write("🎯 Willkommen")
            if player['level'] >= 10:
                st.write("⭐ Level 10 erreicht")
            if player['wins'] > 0:
                st.write("🏆 Erster Sieg")

# ===== TRAINER BEREICH =====
elif st.session_state.role == 'trainer':
    password = st.text_input("Trainer-Passwort:", type="password")
    if password != "trainer123":  # In Produktion sicher speichern!
        st.warning("Falsches Passwort")
        st.stop()
    
    st.header("🎓 Trainer Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📊 Live-Monitoring", "👥 Spielerverwaltung", "📥 Export"])
    
    with tab1:
        st.subheader("Anwesenheit")
        checked_in = [name for name, data in st.session_state.players.items() if data['checkin']]
        st.write(f"**Eingecheckt:** {len(checked_in)} von {len(st.session_state.players)}")
        
        for name in checked_in:
            st.success(f"✅ {name}")
        
        not_checked = [name for name, data in st.session_state.players.items() if not data['checkin']]
        for name in not_checked:
            st.error(f"❌ {name}")
    
    with tab2:
        st.subheader("Spieler verwalten")
        
        for name, data in st.session_state.players.items():
            with st.expander(f"{name} - Level {data['level']}"):
                col1, col2 = st.columns(2)
                with col1:
                    new_xp = st.number_input("XP", value=data['xp'], key=f"xp_{name}")
                    data['xp'] = new_xp
                with col2:
                    new_level = st.number_input("Level", value=data['level'], key=f"lvl_{name}")
                    data['level'] = new_level
                
                if st.button(f"🗑️ {name} löschen", key=f"del_{name}"):
                    del st.session_state.players[name]
                    st.rerun()
        
        st.divider()
        with st.form("new_player"):
            st.write("**Neuer Spieler**")
            new_name = st.text_input("Name")
            if st.form_submit_button("Hinzufügen"):
                if new_name and new_name not in st.session_state.players:
                    st.session_state.players[new_name] = {
                        'level': 1, 'xp': 0, 'checkin': False, 'wins': 0, 'matches': 0
                    }
                    st.success(f"{new_name} hinzugefügt!")
                    st.rerun()
    
    with tab3:
        st.subheader("Anwesenheitsliste exportieren")
        st.write(f"Datum: {datetime.now().strftime('%d.%m.%Y')}")
        
        export_data = "Name,Level,Anwesend\n"
        for name, data in st.session_state.players.items():
            status = "Ja" if data['checkin'] else "Nein"
            export_data += f"{name},{data['level']},{status}\n"
        
        st.download_button(
            label="📥 CSV herunterladen",
            data=export_data,
            file_name=f"anwesenheit_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        if st.button("🔄 Alle Spieler auschecken"):
            for player in st.session_state.players.values():
                player['checkin'] = False
            st.success("Alle Spieler ausgecheckt!")
            st.rerun()