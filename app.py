import streamlit as st
import anthropic
import json
import sqlite3
import os
from datetime import datetime

st.set_page_config(
    page_title="VIKIphone OS",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ROOT VARIABLEN */
:root {
    --viki-blue: #29B6F6;
    --viki-blue-dark: #0288D1;
    --viki-blue-light: #4FC3F7;
    --viki-blue-glow: rgba(41, 182, 246, 0.15);
    --bg-black: #080808;
    --bg-card: #111111;
    --bg-card-hover: #161616;
    --bg-input: #0e0e0e;
    --border: #1e1e1e;
    --border-active: #29B6F6;
    --text-primary: #ffffff;
    --text-secondary: #888888;
    --text-muted: #444444;
    --success: #4CAF50;
    --warning: #FF9800;
    --danger: #f44336;
}

/* GLOBAL */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-black) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; display: none; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 24px 32px !important; max-width: 100% !important; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid var(--border) !important;
    width: 240px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

/* RADIO BUTTONS */
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio label {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    display: block !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--viki-blue-glow) !important;
    color: var(--viki-blue) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    font-family: 'Inter', sans-serif !important;
}

/* BUTTONS */
.stButton > button {
    background: var(--viki-blue) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 20px rgba(41,182,246,0.3) !important;
}
.stButton > button:hover {
    background: var(--viki-blue-light) !important;
    box-shadow: 0 0 30px rgba(41,182,246,0.5) !important;
    transform: translateY(-1px) !important;
}

/* SECONDARY BUTTON */
.btn-secondary > button {
    background: var(--bg-card) !important;
    color: var(--viki-blue) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}
.btn-secondary > button:hover {
    border-color: var(--viki-blue) !important;
    background: var(--viki-blue-glow) !important;
}

/* INPUTS */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--viki-blue) !important;
    box-shadow: 0 0 0 3px rgba(41,182,246,0.1) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--viki-blue); }

/* KARTEN */
.viki-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.2s;
}
.viki-card:hover { border-color: #2a2a2a; }

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.metric-number {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 4px;
}
.metric-number span {
    font-size: 14px;
    color: var(--success);
    font-weight: 500;
    margin-left: 6px;
}
.metric-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 500;
}
.metric-icon {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 36px;
    height: 36px;
    background: var(--viki-blue-glow);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

/* AGENT TABS */
.agent-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    margin-right: 6px;
}
.agent-pill.active {
    background: var(--viki-blue-glow);
    border-color: var(--viki-blue);
    color: var(--viki-blue);
}

/* RESULT CARDS */
.result-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 8px;
    transition: all 0.2s;
}
.result-item:hover {
    border-color: #2a2a2a;
    background: var(--bg-card-hover);
}
.result-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-trend { background: rgba(41,182,246,0.1); color: var(--viki-blue); }
.badge-konkurrenz { background: rgba(244,67,54,0.1); color: #f44336; }
.badge-chance { background: rgba(76,175,80,0.1); color: #4CAF50; }
.result-title-text {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 8px 0 4px;
}
.result-summary-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
}
.result-meta {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 8px;
}

/* CONFIG SECTION */
.config-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}
.config-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* PAGE HEADER */
.page-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 2px;
}
.page-sub {
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 24px;
}

/* NAV LABEL */
.nav-section {
    font-size: 10px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 16px 16px 6px;
}

/* DIVIDER */
.viki-divider {
    height: 1px;
    background: var(--border);
    margin: 16px 0;
}

/* COMING SOON */
.coming-soon {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px;
    text-align: center;
}

/* STATUS DOT */
.status-online { color: var(--success); font-size: 10px; }

/* RELEVANCE */
.rel-high { color: #4CAF50; font-size: 11px; font-weight: 600; }
.rel-mid  { color: #FF9800; font-size: 11px; font-weight: 600; }
.rel-low  { color: #555; font-size: 11px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================
def init_db():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS scout_config (
        id INTEGER PRIMARY KEY,
        keywords TEXT,
        competitors TEXT,
        language TEXT DEFAULT 'de',
        updated_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS scout_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, title TEXT, source TEXT,
        summary TEXT, relevance TEXT, created_at TEXT
    )""")
    c.execute("SELECT COUNT(*) FROM scout_config")
    if c.fetchone()[0] == 0:
        kw = json.dumps(["KI Telefonassistent","Voice AI DACH","KI Telefon Arztpraxis",
            "Telefonassistent SaaS","VIKIphone","KI Rezeption",
            "AI phone assistant Germany","verpasste Anrufe Lösung",
            "24/7 Telefonservice","DSGVO Telefonassistent"])
        comp = json.dumps(["fonio.ai","VITAS Telefonassistent","HalloPetra","heykiki",
            "Parloa","Cognigy","voiceOne","Aaron.ai","Synthflow","smao.ai","Safina AI","RufLab"])
        c.execute("INSERT INTO scout_config VALUES (1,?,?,'de',?)", (kw, comp, datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_scout_config():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT keywords, competitors, language FROM scout_config WHERE id=1")
    row = c.fetchone(); conn.close()
    if row: return json.loads(row[0]), json.loads(row[1]), row[2]
    return [], [], "de"

def save_scout_config(kw, comp, lang):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("UPDATE scout_config SET keywords=?,competitors=?,language=?,updated_at=? WHERE id=1",
              (json.dumps(kw), json.dumps(comp), lang, datetime.now().isoformat()))
    conn.commit(); conn.close()

def save_results(results):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    for r in results:
        c.execute("INSERT INTO scout_results (type,title,source,summary,relevance,created_at) VALUES (?,?,?,?,?,?)",
                  (r.get("type",""), r.get("title",""), r.get("source",""),
                   r.get("summary",""), r.get("relevance",""), datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_results(limit=30):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT type,title,source,summary,relevance,created_at FROM scout_results ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close()
    return rows

def get_count():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM scout_results")
    n = c.fetchone()[0]; conn.close()
    return n

init_db()

# ============================================================
# SESSION STATE
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

USERS = {"admin": "admin123"}

# ============================================================
# SCOUT
# ============================================================
def run_scout(keywords, competitors, language):
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY",""))
    if not api_key:
        st.error("ANTHROPIC_API_KEY fehlt!"); return []
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""Du bist der Scout-Agent für VIKIphone (KI-Telefonassistenz SaaS von Rynon).
Analysiere den DACH-Markt für KI-Telefonassistenten.

KEYWORDS: {', '.join(keywords)}
KONKURRENTEN: {', '.join(competitors)}

VIKIphone USPs: Zero-Latency Konversation, DSGVO Medical Mode, 24/7 Betrieb, Webhook API, automatische Datenlöschung nach 30 Tagen.

Erstelle 10 Einträge als JSON-Array:
- 3x type "TREND" (aktuelle Markttrends DACH 2026)
- 4x type "KONKURRENZ" (fonio.ai, VITAS, HalloPetra, voiceOne analysieren)
- 3x type "CHANCE" (konkrete Chancen für VIKIphone)

Format:
[{{"type":"TREND","title":"...","source":"Marktanalyse DACH 2026","summary":"2-3 Sätze detailliert...","relevance":"HOCH"}}]

Antworte NUR mit dem JSON-Array."""
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=3000,
            messages=[{"role":"user","content":prompt}])
        text = msg.content[0].text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"Scout Fehler: {e}"); return []

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        # Logo & Titel
        st.markdown("""
        <div style='text-align:center; margin-bottom:32px;'>
            <div style='font-size:48px; margin-bottom:8px;'>🔵</div>
            <div style='font-family: Plus Jakarta Sans; font-size:28px; font-weight:800;
                        color:#29B6F6; margin-bottom:4px;'>VIKIphone</div>
            <div style='font-size:13px; color:#555; font-weight:500;'>Company OS · Internal Dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:#111; border:1px solid #1e1e1e; border-radius:16px; padding:32px;'>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Sign in", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("""
        <div style='text-align:center; margin-top:16px; font-size:12px; color:#333;'>
            admin / admin123
        </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================
else:
    # SIDEBAR
    with st.sidebar:
        st.markdown("""
        <div style='padding:20px 16px 12px;'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:4px;'>
                <div style='font-size:22px;'>🔵</div>
                <div>
                    <div style='font-family: Plus Jakarta Sans; font-size:15px; font-weight:700; color:#29B6F6;'>VIKIphone</div>
                    <div style='font-size:10px; color:#444; font-weight:500;'>Company OS</div>
                </div>
            </div>
        </div>
        <div style='height:1px; background:#1e1e1e; margin: 0 16px 12px;'></div>
        """, unsafe_allow_html=True)

        # User
        st.markdown(f"""
        <div style='padding: 8px 16px; margin-bottom:8px;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <div style='width:32px; height:32px; background: rgba(41,182,246,0.15);
                            border-radius:8px; display:flex; align-items:center; justify-content:center;
                            font-size:14px;'>👤</div>
                <div>
                    <div style='font-size:13px; font-weight:600; color:#fff;'>{st.session_state.username.title()}</div>
                    <div style='font-size:11px; color:#4CAF50;'>● Online</div>
                </div>
            </div>
        </div>
        <div style='height:1px; background:#1e1e1e; margin: 0 16px 8px;'></div>
        <div style='padding: 4px 16px; font-size:10px; font-weight:600; color:#333; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;'>Navigation</div>
        """, unsafe_allow_html=True)

        seite = st.radio("nav", [
            "📡  Marketing", "🎯  Vertrieb", "🛰  Support", "🗄  Backoffice", "👾  HR"
        ], label_visibility="collapsed")

        st.markdown("""
        <div style='height:1px; background:#1e1e1e; margin: 8px 16px;'></div>
        """, unsafe_allow_html=True)

        if st.button("Sign out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # ============================================================
    # MARKETING
    # ============================================================
    if "Marketing" in seite:
        st.markdown("""
        <div class='page-header'>Marketing Zentrale</div>
        <div class='page-sub'>VIKIphone Growth · KI-gesteuerte Marktanalyse & Content</div>
        """, unsafe_allow_html=True)

        # Metriken
        count = get_count()
        kw, comp, lang = get_scout_config()
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>📡</div>
                <div class='metric-number'>{count}</div>
                <div class='metric-label'>Scout Ergebnisse</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>🎯</div>
                <div class='metric-number'>{len(comp)}</div>
                <div class='metric-label'>Konkurrenten</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class='metric-card'>
                <div class='metric-icon'>✍️</div>
                <div class='metric-number'>0</div>
                <div class='metric-label'>Posts bereit</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown("""<div class='metric-card'>
                <div class='metric-icon'>🔍</div>
                <div class='metric-number'>0</div>
                <div class='metric-label'>SEO Artikel</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # AGENT AUSWAHL
        agent = st.radio("Agent", [
            "🔭 Scout", "🧠 Growth Hacker", "✍️ Creator", "🏥 Nischen-Spezialist", "🔍 SEO-Architekt"
        ], horizontal=True, label_visibility="collapsed")

        st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)

        # SCOUT
        if "Scout" in agent:
            col_left, col_right = st.columns([2,1])
            with col_left:
                # Keywords
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>⚙️ Keywords konfigurieren</div>
                """, unsafe_allow_html=True)
                kw_text = st.text_area("Ein Keyword pro Zeile", value="\n".join(kw), height=180, label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)

                # Konkurrenten
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🎯 Konkurrenten überwachen</div>
                """, unsafe_allow_html=True)
                comp_text = st.text_area("Ein Konkurrent pro Zeile", value="\n".join(comp), height=180, label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)

                lang_sel = st.selectbox("Ausgabe-Sprache", ["de","en"], index=0 if lang=="de" else 1)

                if st.button("💾  Konfiguration speichern", use_container_width=True):
                    new_kw = [k.strip() for k in kw_text.split("\n") if k.strip()]
                    new_comp = [c.strip() for c in comp_text.split("\n") if c.strip()]
                    save_scout_config(new_kw, new_comp, lang_sel)
                    st.success("✅ Gespeichert!")

            with col_right:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🔭 Scout starten</div>
                    <div style='font-size:13px; color:#555; margin-bottom:16px; line-height:1.6;'>
                        Claude analysiert den DACH-Markt und liefert:<br><br>
                        <span style='color:#29B6F6'>●</span> Aktuelle Markttrends<br>
                        <span style='color:#f44336'>●</span> Konkurrenz-Analyse<br>
                        <span style='color:#4CAF50'>●</span> Marktchancen für VIKIphone
                    </div>
                """, unsafe_allow_html=True)

                if st.button("▶  Jetzt scannen", use_container_width=True):
                    cur_kw = [k.strip() for k in kw_text.split("\n") if k.strip()]
                    cur_comp = [c.strip() for c in comp_text.split("\n") if c.strip()]
                    with st.spinner("Scout analysiert..."):
                        results = run_scout(cur_kw, cur_comp, lang_sel)
                        if results:
                            save_results(results)
                            st.success(f"✅ {len(results)} neue Ergebnisse!")
                            st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(f"""<div class='config-section'>
                    <div class='config-label'>📊 Status</div>
                    <div style='font-size:13px; color:#555;'>
                        <div style='margin-bottom:8px; display:flex; justify-content:space-between;'>
                            <span>Ergebnisse gesamt</span><span style='color:#fff'>{count}</span>
                        </div>
                        <div style='margin-bottom:8px; display:flex; justify-content:space-between;'>
                            <span>Keywords aktiv</span><span style='color:#29B6F6'>{len(kw)}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>Konkurrenten</span><span style='color:#29B6F6'>{len(comp)}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # ERGEBNISSE
            st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:12px;'>Letzte Ergebnisse</div>", unsafe_allow_html=True)

            rows = get_results(30)
            if rows:
                filter_col, _ = st.columns([1,3])
                with filter_col:
                    filt = st.selectbox("Filter", ["Alle","TREND","KONKURRENZ","CHANCE"], label_visibility="collapsed")

                for row in rows:
                    rtype, title, source, summary, relevance, created_at = row
                    if filt != "Alle" and rtype != filt: continue

                    badge_class = {"TREND":"badge-trend","KONKURRENZ":"badge-konkurrenz","CHANCE":"badge-chance"}.get(rtype,"badge-trend")
                    rel_class = {"HOCH":"rel-high","MITTEL":"rel-mid","NIEDRIG":"rel-low"}.get(relevance,"rel-low")

                    st.markdown(f"""
                    <div class='result-item'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span class='result-badge {badge_class}'>{rtype}</span>
                            <span class='{rel_class}'>↑ {relevance}</span>
                        </div>
                        <div class='result-title-text'>{title}</div>
                        <div class='result-summary-text'>{summary}</div>
                        <div class='result-meta'>📡 {source} · {created_at[:10]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align:center; padding:60px; color:#333; font-size:14px;'>
                    Noch keine Daten · Scout starten um Marktanalyse zu laden
                </div>
                """, unsafe_allow_html=True)

        else:
            # Andere Agenten Coming Soon
            labels = {
                "Growth Hacker": ("🧠", "Analysiert virale Trends und entwickelt Kampagnen-Strategien für VIKIphone"),
                "Creator": ("✍️", "Schreibt Posts, Newsletter und Blogartikel basierend auf Scout-Daten"),
                "Nischen-Spezialist": ("🏥", "Erstellt branchenspezifischen Content für Arztpraxen, Handwerker und Kanzleien"),
                "SEO-Architekt": ("🔍", "Keyword-Research und SEO-optimierte Artikel für organischen VIKIphone Traffic"),
            }
            for key, (icon, desc) in labels.items():
                if key in agent:
                    st.markdown(f"""
                    <div class='coming-soon'>
                        <div style='font-size:40px; margin-bottom:16px;'>{icon}</div>
                        <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700;
                                    color:#fff; margin-bottom:8px;'>{key}</div>
                        <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>{desc}</div>
                        <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px;
                                     padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 2</span>
                    </div>
                    """, unsafe_allow_html=True)

    # ANDERE MODULE
    elif "Vertrieb" in seite:
        st.markdown("<div class='page-header'>Vertrieb</div><div class='page-sub'>Lead Management & Demo-Buchungen</div>", unsafe_allow_html=True)
        for n,d in [("🎯 Demo-Hunter","Findet und kontaktiert potenzielle VIKIphone Kunden automatisch"),("📬 Lead-Hunter","Personalisierte Outreach E-Mails für Inbound Leads")]:
            st.markdown(f"""<div class='coming-soon' style='margin-bottom:12px;'>
                <div style='font-size:24px; margin-bottom:8px;'>{n.split()[0]}</div>
                <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>{n[2:]}</div>
                <div style='font-size:13px; color:#555; margin-bottom:12px;'>{d}</div>
                <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
            </div>""", unsafe_allow_html=True)

    elif "Support" in seite:
        st.markdown("<div class='page-header'>Support</div><div class='page-sub'>E-Mail Assistenz & Ticket Management</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:32px; margin-bottom:12px;'>🛰</div>
            <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>Ticket-Master</div>
            <div style='font-size:13px; color:#555; margin-bottom:12px;'>IMAP E-Mail Analyse & automatische Antwort-Entwürfe</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 4</span>
        </div>""", unsafe_allow_html=True)

    elif "Backoffice" in seite:
        st.markdown("<div class='page-header'>Backoffice</div><div class='page-sub'>Rechnungen & Finanzdaten</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:32px; margin-bottom:12px;'>🗄</div>
            <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>Beleg-Nerd</div>
            <div style='font-size:13px; color:#555; margin-bottom:12px;'>OCR PDF Extraktion → automatische CSV Tabelle in SQLite</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)

    elif "HR" in seite:
        st.markdown("<div class='page-header'>HR & Recruiting</div><div class='page-sub'>Bewerbermanagement</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:32px; margin-bottom:12px;'>👾</div>
            <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>CV-Scanner</div>
            <div style='font-size:13px; color:#555; margin-bottom:12px;'>Lebenslauf Matching & Interview-Fragen Generator</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)
