import streamlit as st

st.set_page_config(
    page_title="Vikiphone OS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# FUTURISTISCHES CSS DESIGN
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

/* GLOBALER HINTERGRUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #010b1f 0%, #020d2e 50%, #050520 100%);
    color: #e0f0ff;
    font-family: 'Rajdhani', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020c28 0%, #010817 100%) !important;
    border-right: 1px solid #1a3a6e;
    box-shadow: 4px 0 30px rgba(0, 120, 255, 0.15);
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, #7b2fff, transparent);
}

/* SIDEBAR RADIO BUTTONS */
[data-testid="stSidebar"] .stRadio label {
    color: #8ab4d4 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    padding: 8px 12px !important;
    border-radius: 4px !important;
    transition: all 0.3s !important;
    border-left: 2px solid transparent !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: #00d4ff !important;
    border-left: 2px solid #00d4ff !important;
    background: rgba(0, 212, 255, 0.05) !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #0a1628, #0d1f3c) !important;
    color: #00d4ff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 4px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 8px 20px !important;
    transition: all 0.3s !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
}

.stButton > button:hover {
    background: rgba(0, 212, 255, 0.1) !important;
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.5) !important;
    transform: translateY(-1px) !important;
}

/* INPUT FELDER */
.stTextInput > div > div > input {
    background: rgba(0, 20, 60, 0.8) !important;
    border: 1px solid #1a3a6e !important;
    border-radius: 4px !important;
    color: #e0f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
}

.stTextInput label {
    color: #8ab4d4 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
}

/* INFO / ALERT BOXEN */
.stAlert {
    background: rgba(0, 212, 255, 0.05) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    border-radius: 4px !important;
    color: #8ab4d4 !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #010b1f; }
::-webkit-scrollbar-thumb { background: #1a3a6e; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00d4ff; }

/* METRIC KARTEN */
.metric-card {
    background: linear-gradient(135deg, rgba(0,30,80,0.8), rgba(0,15,50,0.9));
    border: 1px solid #1a3a6e;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00d4ff, #7b2fff);
}

.metric-card:hover {
    border-color: #00d4ff;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    transform: translateY(-2px);
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #00d4ff;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
}

.metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 11px;
    color: #8ab4d4;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

.metric-trend {
    font-size: 12px;
    color: #00ff88;
    margin-top: 6px;
}

/* MODULE KARTEN */
.module-card {
    background: linear-gradient(135deg, rgba(0,25,70,0.7), rgba(0,10,40,0.9));
    border: 1px solid #1a3a6e;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}

.module-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #7b2fff, transparent);
}

.module-card:hover {
    border-color: rgba(123, 47, 255, 0.5);
    box-shadow: 0 0 25px rgba(123, 47, 255, 0.15);
}

/* SECTION TITEL */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    color: #00d4ff;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.page-title {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
    margin-bottom: 4px;
}

/* STATUS BADGE */
.status-badge {
    display: inline-block;
    background: rgba(0, 255, 136, 0.1);
    border: 1px solid #00ff88;
    color: #00ff88;
    font-family: 'Rajdhani', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 3px 10px;
    border-radius: 2px;
    text-transform: uppercase;
}

/* DIVIDER */
.cyber-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1a3a6e, #00d4ff, #1a3a6e, transparent);
    margin: 20px 0;
}

/* AGENT KARTE */
.agent-card {
    background: rgba(0, 20, 60, 0.5);
    border: 1px solid #1a3a6e;
    border-left: 3px solid #7b2fff;
    border-radius: 4px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: all 0.3s;
}

.agent-card:hover {
    border-left-color: #00d4ff;
    background: rgba(0, 212, 255, 0.03);
    box-shadow: -4px 0 15px rgba(123, 47, 255, 0.2);
}

.agent-name {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}

.agent-status {
    font-size: 11px;
    color: #8ab4d4;
    letter-spacing: 1px;
}

/* LOGIN SPEZIFISCH */
.login-container {
    background: linear-gradient(135deg, rgba(0,20,60,0.9), rgba(0,8,30,0.95));
    border: 1px solid #1a3a6e;
    border-radius: 8px;
    padding: 48px 40px;
    position: relative;
    overflow: hidden;
}

.login-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7b2fff, #00d4ff, #7b2fff);
}

.login-logo {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #7b2fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 4px;
}

.login-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 12px;
    color: #8ab4d4;
    letter-spacing: 4px;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 32px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

USERS = {"admin": "admin123"}

def check_login(username, password):
    return username in USERS and USERS[username] == password

# ============================================================
# LOGIN SCREEN
# ============================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">VIKIPHONE OS</div>
            <div class="login-sub">Autonomes KI · Command Center</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        username = st.text_input("BENUTZERNAME")
        password = st.text_input("PASSWORT", type="password")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("⟶  ZUGANG ANFORDERN", use_container_width=True):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("⚠  ZUGANG VERWEIGERT — Ungültige Zugangsdaten")

        st.markdown("""
        <div style='text-align:center; margin-top:24px;'>
            <span style='font-family: Rajdhani; font-size:11px; color:#1a3a6e; letter-spacing:2px;'>
            STANDARD: admin / admin123
            </span>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================
else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("""
        <div style='padding: 20px 0 10px 0;'>
            <div style='font-family: Orbitron; font-size: 18px; font-weight: 900;
                        background: linear-gradient(135deg, #00d4ff, #7b2fff);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        margin-bottom: 2px;'>VIKIPHONE OS</div>
            <div style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e;
                        letter-spacing: 3px; text-transform: uppercase;'>Command Center v1.0</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='font-family: Rajdhani; font-size: 12px; color: #8ab4d4;
                    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;'>
            Operator
        </div>
        <div style='font-family: Orbitron; font-size: 14px; color: #ffffff; margin-bottom: 16px;'>
            {st.session_state.username.upper()}
        </div>
        <span class='status-badge'>● SYSTEM ONLINE</span>
        """, unsafe_allow_html=True)

        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e;
                    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;'>
            Module
        </div>
        """, unsafe_allow_html=True)

        seite = st.radio(
            "Navigation",
            ["📡  MARKETING", "🎯  VERTRIEB", "🛰  SUPPORT", "🗄  BACKOFFICE", "👾  HR"],
            label_visibility="collapsed"
        )

        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

        if st.button("⏻  LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- HAUPTBEREICH ---
    seite_clean = seite.split("  ")[1] if "  " in seite else seite

    # HEADER
    st.markdown(f"""
    <div class='section-title'>VIKIPHONE OS · MODUL</div>
    <div class='page-title'>{seite_clean}</div>
    <div class='cyber-divider'></div>
    """, unsafe_allow_html=True)

    # MARKETING MODULE
    if "MARKETING" in seite:
        # Metriken
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            ("0", "CONTENT HEUTE", "▲ Bereit"),
            ("0", "LEADS PIPELINE", "— Warten"),
            ("0", "SEO ARTIKEL", "— Warten"),
            ("0", "NISCHEN POSTS", "— Warten"),
        ]
        for col, (val, label, trend) in zip([col1, col2, col3, col4], metrics):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{val}</div>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-trend'>{trend}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # Agenten Status
        st.markdown("<div class='section-title'>AGENTEN · STATUS</div>", unsafe_allow_html=True)

        agents = [
            ("🔭", "SCOUT", "Scannt täglich News & Konkurrenz (Parloa, VITAS, Cognigy)", "COMING SOON"),
            ("🧠", "GROWTH HACKER", "Analysiert virale Trends & entwickelt Kampagnen-Strategien", "COMING SOON"),
            ("✍️", "CREATOR", "Schreibt Posts, Newsletter & Blogartikel für Vikiphone", "COMING SOON"),
            ("🏥", "NISCHEN-SPEZIALIST", "Erstellt Content für Arztpraxen, Handwerker, Kanzleien", "COMING SOON"),
            ("🔍", "SEO-ARCHITEKT", "Keyword-Research & SEO-Artikel für organischen Traffic", "COMING SOON"),
        ]

        for icon, name, desc, status in agents:
            st.markdown(f"""
            <div class='agent-card'>
                <div class='agent-name'>{icon}  {name}</div>
                <div class='agent-status' style='margin-top:6px; color:#4a7a9b;'>{desc}</div>
                <div style='margin-top:8px;'>
                    <span style='font-family: Rajdhani; font-size:10px; color:#1a3a6e;
                                letter-spacing:2px; text-transform:uppercase;
                                border: 1px solid #1a3a6e; padding: 2px 8px; border-radius:2px;'>
                        {status}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # VERTRIEB MODULE
    elif "VERTRIEB" in seite:
        col1, col2, col3 = st.columns(3)
        for col, (val, label) in zip([col1, col2, col3], [("0", "NEUE LEADS"), ("0", "DEMOS GEPLANT"), ("0", "OUTREACH HEUTE")]):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>AGENTEN · STATUS</div>", unsafe_allow_html=True)

        for icon, name, desc in [
            ("🎯", "DEMO-HUNTER", "Findet & kontaktiert potenzielle Vikiphone-Kunden automatisch"),
            ("📬", "LEAD-HUNTER", "Personalisierte Outreach-E-Mails für Inbound-Leads"),
        ]:
            st.markdown(f"""
            <div class='agent-card'>
                <div class='agent-name'>{icon}  {name}</div>
                <div class='agent-status' style='margin-top:6px; color:#4a7a9b;'>{desc}</div>
                <div style='margin-top:8px;'>
                    <span style='font-family: Rajdhani; font-size:10px; color:#1a3a6e;
                                letter-spacing:2px; border: 1px solid #1a3a6e;
                                padding: 2px 8px; border-radius:2px;'>COMING SOON</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # SUPPORT MODULE
    elif "SUPPORT" in seite:
        st.markdown("""
        <div class='module-card'>
            <div class='agent-name'>🛰  TICKET-MASTER</div>
            <div class='agent-status' style='margin-top:8px; color:#4a7a9b;'>
                Liest Support-E-Mails via IMAP, analysiert Sentiment und erstellt Antwort-Entwürfe
            </div>
            <div style='margin-top:12px;'>
                <span style='font-family: Rajdhani; font-size:10px; color:#1a3a6e;
                            letter-spacing:2px; border: 1px solid #1a3a6e;
                            padding: 2px 8px; border-radius:2px;'>COMING SOON · PHASE 4</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # BACKOFFICE MODULE
    elif "BACKOFFICE" in seite:
        st.markdown("""
        <div class='module-card'>
            <div class='agent-name'>🗄  BELEG-NERD</div>
            <div class='agent-status' style='margin-top:8px; color:#4a7a9b;'>
                OCR-Extraktion aus PDF-Rechnungen → automatische CSV-Tabelle in SQLite
            </div>
            <div style='margin-top:12px;'>
                <span style='font-family: Rajdhani; font-size:10px; color:#1a3a6e;
                            letter-spacing:2px; border: 1px solid #1a3a6e;
                            padding: 2px 8px; border-radius:2px;'>COMING SOON · PHASE 3</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # HR MODULE
    elif "HR" in seite:
        st.markdown("""
        <div class='module-card'>
            <div class='agent-name'>👾  CV-SCANNER</div>
            <div class='agent-status' style='margin-top:8px; color:#4a7a9b;'>
                Gleicht Lebensläufe mit Stellenbeschreibung ab & berechnet Matching-Score
            </div>
            <div style='margin-top:12px;'>
                <span style='font-family: Rajdhani; font-size:10px; color:#1a3a6e;
                            letter-spacing:2px; border: 1px solid #1a3a6e;
                            padding: 2px 8px; border-radius:2px;'>COMING SOON · PHASE 3</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <div style='position: fixed; bottom: 0; left: 0; right: 0; padding: 8px 24px;
                background: rgba(1,11,31,0.95);
                border-top: 1px solid #0a1628;
                display: flex; justify-content: space-between; align-items: center;'>
        <span style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e; letter-spacing: 2px;'>
            VIKIPHONE OS · v1.0.0
        </span>
        <span style='font-family: Orbitron; font-size: 10px; color: #1a3a6e;'>
            ● ALL SYSTEMS OPERATIONAL
        </span>
    </div>
    """, unsafe_allow_html=True)
