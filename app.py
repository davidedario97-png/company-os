import streamlit as st
import anthropic
import json
import sqlite3
import os
from datetime import datetime
import urllib.request
import urllib.parse

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="VIKIphone OS",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS DESIGN
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #010b1f 0%, #020d2e 50%, #050520 100%);
    color: #e0f0ff;
    font-family: 'Rajdhani', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020c28 0%, #010817 100%) !important;
    border-right: 1px solid #1a3a6e;
    box-shadow: 4px 0 30px rgba(0,120,255,0.15);
}
.stButton > button {
    background: linear-gradient(135deg, #0a1628, #0d1f3c) !important;
    color: #00d4ff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 4px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    transition: all 0.3s !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.2) !important;
}
.stButton > button:hover {
    background: rgba(0,212,255,0.1) !important;
    box-shadow: 0 0 25px rgba(0,212,255,0.5) !important;
}
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: rgba(0,20,60,0.8) !important;
    border: 1px solid #1a3a6e !important;
    border-radius: 4px !important;
    color: #e0f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.3) !important;
}
.stTextInput label, .stTextArea label, .stMultiSelect label, .stSelectbox label {
    color: #8ab4d4 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #8ab4d4 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}
.cyber-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1a3a6e, #00d4ff, #1a3a6e, transparent);
    margin: 16px 0;
}
.metric-card {
    background: linear-gradient(135deg, rgba(0,30,80,0.8), rgba(0,15,50,0.9));
    border: 1px solid #1a3a6e;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00d4ff, #7b2fff);
}
.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #00d4ff;
    text-shadow: 0 0 20px rgba(0,212,255,0.5);
}
.metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 11px;
    color: #8ab4d4;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}
.config-box {
    background: rgba(0,20,60,0.5);
    border: 1px solid #1a3a6e;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 16px;
}
.config-box-title {
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    color: #00d4ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.result-card {
    background: rgba(0,15,40,0.8);
    border: 1px solid #1a3a6e;
    border-left: 3px solid #00d4ff;
    border-radius: 4px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.result-title {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    color: #ffffff;
    margin-bottom: 6px;
}
.result-source {
    font-size: 11px;
    color: #4a7a9b;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.result-summary {
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
    color: #8ab4d4;
    line-height: 1.5;
}
.agent-card {
    background: rgba(0,20,60,0.5);
    border: 1px solid #1a3a6e;
    border-left: 3px solid #7b2fff;
    border-radius: 4px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.page-title {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0 0 30px rgba(0,212,255,0.4);
}
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    color: #00d4ff;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #010b1f; }
::-webkit-scrollbar-thumb { background: #1a3a6e; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================
def init_db():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    # Scout Config
    c.execute("""CREATE TABLE IF NOT EXISTS scout_config (
        id INTEGER PRIMARY KEY,
        keywords TEXT,
        competitors TEXT,
        language TEXT DEFAULT 'de',
        updated_at TEXT
    )""")
    # Scout Results
    c.execute("""CREATE TABLE IF NOT EXISTS scout_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        title TEXT,
        source TEXT,
        summary TEXT,
        relevance TEXT,
        created_at TEXT
    )""")
    # Default config
    c.execute("SELECT COUNT(*) FROM scout_config")
    if c.fetchone()[0] == 0:
        default_keywords = json.dumps([
            "KI Telefonassistent", "Voice AI DACH", "KI Telefon Arztpraxis",
            "Telefonassistent SaaS", "VIKIphone", "KI Rezeption",
            "AI phone assistant Germany", "verpasste Anrufe Lösung"
        ])
        default_competitors = json.dumps([
            "fonio.ai", "VITAS Telefonassistent", "HalloPetra",
            "heykiki", "Parloa", "Cognigy", "voiceOne", "Aaron.ai",
            "Synthflow", "smao.ai", "Safina AI", "RufLab"
        ])
        c.execute("INSERT INTO scout_config (keywords, competitors, language, updated_at) VALUES (?,?,?,?)",
                  (default_keywords, default_competitors, "de", datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_scout_config():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT keywords, competitors, language FROM scout_config WHERE id=1")
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0]), json.loads(row[1]), row[2]
    return [], [], "de"

def save_scout_config(keywords, competitors, language):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("UPDATE scout_config SET keywords=?, competitors=?, language=?, updated_at=? WHERE id=1",
              (json.dumps(keywords), json.dumps(competitors), language, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_scout_results(results):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    for r in results:
        c.execute("INSERT INTO scout_results (type, title, source, summary, relevance, created_at) VALUES (?,?,?,?,?,?)",
                  (r.get("type",""), r.get("title",""), r.get("source",""),
                   r.get("summary",""), r.get("relevance",""), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_scout_results(limit=20):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT type, title, source, summary, relevance, created_at FROM scout_results ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_result_count():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM scout_results")
    count = c.fetchone()[0]
    conn.close()
    return count

init_db()

# ============================================================
# SESSION STATE
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_agent" not in st.session_state:
    st.session_state.current_agent = None

USERS = {"admin": "admin123"}

def check_login(u, p):
    return u in USERS and USERS[u] == p

# ============================================================
# SCOUT AGENT LOGIK
# ============================================================
def run_scout_agent(keywords, competitors, language):
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
    if not api_key:
        st.error("⚠ ANTHROPIC_API_KEY nicht gefunden!")
        return []

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Du bist der Scout-Agent für VIKIphone (KI-Telefonassistenz SaaS von Rynon).

Deine Aufgabe: Analysiere den Markt für KI-Telefonassistenten im DACH-Raum und erstelle einen Marktbericht.

KEYWORDS ZU ÜBERWACHEN: {', '.join(keywords)}
KONKURRENTEN ZU ANALYSIEREN: {', '.join(competitors)}
SPRACHE: {language}

Erstelle einen detaillierten Marktbericht mit folgenden Abschnitten und gib die Antwort als JSON-Array zurück:

[
  {{
    "type": "TREND",
    "title": "Titel des Trends",
    "source": "Marktbeobachtung DACH 2026",
    "summary": "Detaillierte Beschreibung des Trends (2-3 Sätze) und warum er für VIKIphone relevant ist",
    "relevance": "HOCH / MITTEL / NIEDRIG"
  }},
  {{
    "type": "KONKURRENZ",
    "title": "Konkurrent: [Name]",
    "source": "Wettbewerbsanalyse",
    "summary": "Was macht dieser Konkurrent? Stärken/Schwächen vs VIKIphone? Preismodell?",
    "relevance": "HOCH / MITTEL / NIEDRIG"
  }},
  {{
    "type": "CHANCE",
    "title": "Marktchance: [Beschreibung]",
    "source": "Strategische Analyse",
    "summary": "Welche konkrete Chance gibt es für VIKIphone? Wie kann VIKIphone profitieren?",
    "relevance": "HOCH / MITTEL / NIEDRIG"
  }}
]

Erstelle mindestens:
- 3 aktuelle TREND Einträge (KI-Telefonie Markt DACH 2026)
- 4 KONKURRENZ Analysen (fokus auf fonio.ai, VITAS, HalloPetra, voiceOne)
- 3 CHANCE Einträge (spezifisch für VIKIphone USPs: Zero-Latency, DSGVO-Medical-Mode, Webhook-API)

VIKIphone USPs (nutze diese für die Analyse):
- Zero-Latency Konversation (kein Gedenksekunden)
- DSGVO Medical Mode (Arztpraxen)
- 24/7 Telefonassistenz
- Dedizierte Festnetz-Rufnummer
- Webhook API für CRM-Integration
- Automatischer 30-Tage DSGVO-Datenlöschung

Antworte NUR mit dem JSON-Array, kein anderer Text."""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = message.content[0].text.strip()
        # JSON extrahieren
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        results = json.loads(response_text)
        return results
    except Exception as e:
        st.error(f"⚠ Fehler beim Scout: {str(e)}")
        return []

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0,20,60,0.9), rgba(0,8,30,0.95));
                    border: 1px solid #1a3a6e; border-radius: 8px; padding: 48px 40px;
                    position: relative; overflow: hidden;'>
            <div style='position:absolute; top:0; left:0; right:0; height:2px;
                        background: linear-gradient(90deg, #7b2fff, #00d4ff, #7b2fff);'></div>
            <div style='font-family: Orbitron; font-size: 28px; font-weight: 900;
                        background: linear-gradient(135deg, #00d4ff, #7b2fff);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        text-align: center; margin-bottom: 4px;'>VIKIphone OS</div>
            <div style='font-family: Rajdhani; font-size: 12px; color: #8ab4d4;
                        letter-spacing: 4px; text-transform: uppercase; text-align: center;
                        margin-bottom: 32px;'>Autonomes KI · Command Center</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        username = st.text_input("BENUTZERNAME")
        password = st.text_input("PASSWORT", type="password")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("⟶  ZUGANG ANFORDERN", use_container_width=True):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("⚠  ZUGANG VERWEIGERT")
        st.markdown("""
        <div style='text-align:center; margin-top:16px;'>
            <span style='font-family: Rajdhani; font-size:11px; color:#1a3a6e; letter-spacing:2px;'>
            STANDARD: admin / admin123
            </span>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================
else:
    # SIDEBAR
    with st.sidebar:
        st.markdown("""
        <div style='padding: 20px 0 10px 0;'>
            <div style='font-family: Orbitron; font-size: 18px; font-weight: 900;
                        background: linear-gradient(135deg, #00d4ff, #7b2fff);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                VIKIphone OS</div>
            <div style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e;
                        letter-spacing: 3px;'>Command Center v1.1</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='font-family: Rajdhani; font-size: 12px; color: #8ab4d4; letter-spacing: 2px; text-transform: uppercase;'>Operator</div>
        <div style='font-family: Orbitron; font-size: 14px; color: #fff; margin-bottom: 12px;'>{st.session_state.username.upper()}</div>
        <span style='background: rgba(0,255,136,0.1); border: 1px solid #00ff88; color: #00ff88;
                     font-family: Rajdhani; font-size: 11px; font-weight: 600; letter-spacing: 2px;
                     padding: 3px 10px; border-radius: 2px;'>● SYSTEM ONLINE</span>
        """, unsafe_allow_html=True)
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        seite = st.radio("Navigation", [
            "📡  MARKETING", "🎯  VERTRIEB", "🛰  SUPPORT", "🗄  BACKOFFICE", "👾  HR"
        ], label_visibility="collapsed")
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        if st.button("⏻  LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # MARKETING MODULE
    if "MARKETING" in seite:
        st.markdown("<div class='section-title'>VIKIphone OS · MODUL</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-title'>📡 MARKETING ZENTRALE</div>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

        # Metriken
        result_count = get_result_count()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{result_count}</div><div class='metric-label'>SCOUT ERGEBNISSE</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-card'><div class='metric-value'>12</div><div class='metric-label'>KONKURRENTEN</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='metric-card'><div class='metric-value'>0</div><div class='metric-label'>POSTS BEREIT</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='metric-card'><div class='metric-value'>0</div><div class='metric-label'>SEO ARTIKEL</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # AGENT AUSWAHL
        agent_tab = st.radio("Agent auswählen:", [
            "🔭 SCOUT", "🧠 GROWTH HACKER", "✍️ CREATOR",
            "🏥 NISCHEN-SPEZIALIST", "🔍 SEO-ARCHITEKT"
        ], horizontal=True, label_visibility="collapsed")

        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

        # ============================================================
        # SCOUT AGENT
        # ============================================================
        if "SCOUT" in agent_tab:
            st.markdown("<div class='section-title'>AGENT · KONFIGURATION</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-family: Orbitron; font-size: 16px; color: #fff; margin-bottom: 16px;'>🔭 SCOUT AGENT</div>", unsafe_allow_html=True)

            keywords, competitors, language = get_scout_config()

            col_config, col_run = st.columns([2, 1])

            with col_config:
                # Keywords
                st.markdown("<div class='config-box'>", unsafe_allow_html=True)
                st.markdown("<div class='config-box-title'>⚙ KEYWORDS KONFIGURATION</div>", unsafe_allow_html=True)

                keywords_text = st.text_area(
                    "KEYWORDS (ein Keyword pro Zeile)",
                    value="\n".join(keywords),
                    height=200,
                    help="Der Scout sucht täglich nach diesen Keywords"
                )

                st.markdown("</div>", unsafe_allow_html=True)

                # Konkurrenten
                st.markdown("<div class='config-box'>", unsafe_allow_html=True)
                st.markdown("<div class='config-box-title'>🎯 KONKURRENTEN ÜBERWACHUNG</div>", unsafe_allow_html=True)

                competitors_text = st.text_area(
                    "KONKURRENTEN (ein Name pro Zeile)",
                    value="\n".join(competitors),
                    height=200,
                    help="Der Scout analysiert diese Konkurrenten täglich"
                )
                st.markdown("</div>", unsafe_allow_html=True)

                # Sprache
                lang = st.selectbox("AUSGABE-SPRACHE", ["de", "en"], index=0 if language == "de" else 1)

                if st.button("💾  KONFIGURATION SPEICHERN", use_container_width=True):
                    new_keywords = [k.strip() for k in keywords_text.split("\n") if k.strip()]
                    new_competitors = [c.strip() for c in competitors_text.split("\n") if c.strip()]
                    save_scout_config(new_keywords, new_competitors, lang)
                    st.success("✅ Konfiguration gespeichert!")

            with col_run:
                st.markdown("<div class='config-box'>", unsafe_allow_html=True)
                st.markdown("<div class='config-box-title'>▶ SCOUT STARTEN</div>", unsafe_allow_html=True)
                st.markdown("""
                <div style='font-family: Rajdhani; font-size: 13px; color: #4a7a9b; margin-bottom: 16px;'>
                    Der Scout analysiert den Markt und liefert:<br><br>
                    ● Aktuelle Markttrends<br>
                    ● Konkurrenz-Analyse<br>
                    ● Marktchancen für VIKIphone<br>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🔭  JETZT SCANNEN", use_container_width=True):
                    current_kw = [k.strip() for k in keywords_text.split("\n") if k.strip()]
                    current_comp = [c.strip() for c in competitors_text.split("\n") if c.strip()]

                    with st.spinner("Scout analysiert Markt..."):
                        results = run_scout_agent(current_kw, current_comp, lang)
                        if results:
                            save_scout_results(results)
                            st.success(f"✅ {len(results)} Ergebnisse gefunden!")
                            st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

                # Status
                st.markdown("<div class='config-box'>", unsafe_allow_html=True)
                st.markdown("<div class='config-box-title'>📊 STATUS</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='font-family: Rajdhani; font-size: 13px; color: #8ab4d4;'>
                    Gesamt Ergebnisse: <span style='color:#00d4ff'>{result_count}</span><br>
                    Keywords aktiv: <span style='color:#00d4ff'>{len(keywords)}</span><br>
                    Konkurrenten: <span style='color:#00d4ff'>{len(competitors)}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # ERGEBNISSE
            st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>LETZTE SCOUT ERGEBNISSE</div>", unsafe_allow_html=True)

            rows = get_scout_results(20)
            if rows:
                # Filter
                filter_type = st.selectbox("FILTER", ["ALLE", "TREND", "KONKURRENZ", "CHANCE"])

                for row in rows:
                    rtype, title, source, summary, relevance, created_at = row
                    if filter_type != "ALLE" and rtype != filter_type:
                        continue

                    color_map = {"TREND": "#00d4ff", "KONKURRENZ": "#ff6b6b", "CHANCE": "#00ff88"}
                    color = color_map.get(rtype, "#7b2fff")
                    rel_color = {"HOCH": "#00ff88", "MITTEL": "#ffd700", "NIEDRIG": "#4a7a9b"}.get(relevance, "#4a7a9b")

                    st.markdown(f"""
                    <div class='result-card' style='border-left-color: {color};'>
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
                            <span style='font-family: Orbitron; font-size: 10px; color: {color};
                                        border: 1px solid {color}; padding: 2px 8px; border-radius: 2px;'>
                                {rtype}
                            </span>
                            <span style='font-family: Rajdhani; font-size: 10px; color: {rel_color}; letter-spacing: 1px;'>
                                RELEVANZ: {relevance}
                            </span>
                        </div>
                        <div class='result-title'>{title}</div>
                        <div class='result-source'>📡 {source} · {created_at[:10]}</div>
                        <div class='result-summary'>{summary}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align:center; padding: 60px; color: #1a3a6e;
                            font-family: Orbitron; font-size: 14px; letter-spacing: 3px;'>
                    KEINE DATEN · SCOUT STARTEN
                </div>
                """, unsafe_allow_html=True)

        # ANDERE AGENTEN (Coming Soon)
        else:
            agent_names = {
                "GROWTH HACKER": ("🧠", "Analysiert virale Trends & entwickelt Kampagnen-Strategien für VIKIphone", "PHASE 2 · COMING SOON"),
                "CREATOR": ("✍️", "Schreibt Posts, Newsletter & Blogartikel basierend auf Scout-Daten", "PHASE 2 · COMING SOON"),
                "NISCHEN-SPEZIALIST": ("🏥", "Erstellt branchenspezifischen Content für Arztpraxen, Handwerker, Kanzleien", "PHASE 2 · COMING SOON"),
                "SEO-ARCHITEKT": ("🔍", "Keyword-Research & SEO-Artikel für organischen VIKIphone Traffic", "PHASE 2 · COMING SOON"),
            }
            for key, (icon, desc, status) in agent_names.items():
                if key in agent_tab:
                    st.markdown(f"""
                    <div class='agent-card'>
                        <div style='font-family: Orbitron; font-size: 16px; color: #fff;'>{icon} {key}</div>
                        <div style='font-family: Rajdhani; font-size: 14px; color: #4a7a9b; margin-top: 8px;'>{desc}</div>
                        <div style='margin-top: 12px;'>
                            <span style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e;
                                        letter-spacing: 2px; border: 1px solid #1a3a6e;
                                        padding: 2px 8px; border-radius: 2px;'>{status}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ANDERE MODULE
    elif "VERTRIEB" in seite:
        st.markdown("<div class='page-title'>🎯 VERTRIEB</div>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        for name, desc in [("DEMO-HUNTER", "Findet & kontaktiert potenzielle VIKIphone Kunden"), ("LEAD-HUNTER", "Personalisierte Outreach E-Mails für Inbound Leads")]:
            st.markdown(f"""<div class='agent-card'>
                <div style='font-family: Orbitron; font-size: 14px; color: #fff;'>🎯 {name}</div>
                <div style='color: #4a7a9b; margin-top: 8px;'>{desc}</div>
                <div style='margin-top: 10px;'><span style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e; letter-spacing: 2px; border: 1px solid #1a3a6e; padding: 2px 8px; border-radius: 2px;'>COMING SOON · PHASE 3</span></div>
            </div>""", unsafe_allow_html=True)

    elif "SUPPORT" in seite:
        st.markdown("<div class='page-title'>🛰 SUPPORT</div>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        st.markdown("""<div class='agent-card'>
            <div style='font-family: Orbitron; font-size: 14px; color: #fff;'>🛰 TICKET-MASTER</div>
            <div style='color: #4a7a9b; margin-top: 8px;'>IMAP E-Mail Analyse & automatische Antwort-Entwürfe</div>
            <div style='margin-top: 10px;'><span style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e; letter-spacing: 2px; border: 1px solid #1a3a6e; padding: 2px 8px; border-radius: 2px;'>COMING SOON · PHASE 4</span></div>
        </div>""", unsafe_allow_html=True)

    elif "BACKOFFICE" in seite:
        st.markdown("<div class='page-title'>🗄 BACKOFFICE</div>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        st.markdown("""<div class='agent-card'>
            <div style='font-family: Orbitron; font-size: 14px; color: #fff;'>🗄 BELEG-NERD</div>
            <div style='color: #4a7a9b; margin-top: 8px;'>OCR PDF Extraktion → CSV in SQLite Datenbank</div>
            <div style='margin-top: 10px;'><span style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e; letter-spacing: 2px; border: 1px solid #1a3a6e; padding: 2px 8px; border-radius: 2px;'>COMING SOON · PHASE 3</span></div>
        </div>""", unsafe_allow_html=True)

    elif "HR" in seite:
        st.markdown("<div class='page-title'>👾 HR</div>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        st.markdown("""<div class='agent-card'>
            <div style='font-family: Orbitron; font-size: 14px; color: #fff;'>👾 CV-SCANNER</div>
            <div style='color: #4a7a9b; margin-top: 8px;'>Lebenslauf Matching & Interview-Fragen Generator</div>
            <div style='margin-top: 10px;'><span style='font-family: Rajdhani; font-size: 10px; color: #1a3a6e; letter-spacing: 2px; border: 1px solid #1a3a6e; padding: 2px 8px; border-radius: 2px;'>COMING SOON · PHASE 3</span></div>
        </div>""", unsafe_allow_html=True)
