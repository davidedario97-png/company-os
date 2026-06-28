import streamlit as st
import anthropic
import json
import sqlite3
import os
from datetime import datetime
import urllib.request
import urllib.parse

st.set_page_config(
    page_title="VIKIphone OS",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

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
    --text-primary: #ffffff;
    --text-secondary: #888888;
    --text-muted: #444444;
    --success: #4CAF50;
    --warning: #FF9800;
    --danger: #f44336;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-black) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; display: none; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 24px 32px !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
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
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--viki-blue-glow) !important;
    color: var(--viki-blue) !important;
}

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

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
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

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--viki-blue); }

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
.metric-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 500;
}
.metric-icon {
    position: absolute;
    top: 20px; right: 20px;
    width: 36px; height: 36px;
    background: var(--viki-blue-glow);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}

.result-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 8px;
    transition: all 0.2s;
}
.result-item:hover { border-color: #2a2a2a; background: var(--bg-card-hover); }
.result-badge {
    display: inline-block;
    padding: 2px 10px; border-radius: 20px;
    font-size: 10px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.badge-trend { background: rgba(41,182,246,0.1); color: var(--viki-blue); }
.badge-konkurrenz { background: rgba(244,67,54,0.1); color: #f44336; }
.badge-chance { background: rgba(76,175,80,0.1); color: #4CAF50; }
.badge-news { background: rgba(255,152,0,0.1); color: #FF9800; }

.result-title-text {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px; font-weight: 600;
    color: var(--text-primary); margin: 8px 0 4px;
}
.result-summary-text { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
.result-meta { font-size: 11px; color: var(--text-muted); margin-top: 8px; }

.config-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px; margin-bottom: 12px;
}
.config-label {
    font-size: 13px; font-weight: 600;
    color: var(--text-primary); margin-bottom: 12px;
}
.page-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 22px; font-weight: 700;
    color: var(--text-primary); margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: var(--text-secondary); margin-bottom: 24px; }
.viki-divider { height: 1px; background: var(--border); margin: 16px 0; }
.coming-soon {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 40px; text-align: center;
}
.rel-high { color: #4CAF50; font-size: 11px; font-weight: 600; }
.rel-mid  { color: #FF9800; font-size: 11px; font-weight: 600; }
.rel-low  { color: #555; font-size: 11px; font-weight: 600; }

.live-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.3);
    color: #4CAF50; border-radius: 20px;
    padding: 3px 10px; font-size: 11px; font-weight: 600;
}
.source-link {
    color: var(--viki-blue); font-size: 11px;
    text-decoration: none;
}
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
        keywords TEXT, competitors TEXT,
        language TEXT DEFAULT 'de', updated_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS scout_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, title TEXT, source TEXT, url TEXT,
        summary TEXT, relevance TEXT, created_at TEXT
    )""")
    # Migration: url Spalte hinzufügen falls nicht vorhanden
    try:
        c.execute("ALTER TABLE scout_results ADD COLUMN url TEXT")
    except:
        pass
    c.execute("SELECT COUNT(*) FROM scout_config")
    if c.fetchone()[0] == 0:
        kw = json.dumps([
            "KI Telefonassistent", "Voice AI DACH", "KI Telefon Arztpraxis",
            "Telefonassistent SaaS", "KI Rezeption", "verpasste Anrufe Lösung",
            "24/7 Telefonservice", "DSGVO Telefonassistent", "AI phone assistant Germany"
        ])
        comp = json.dumps([
            "fonio.ai", "VITAS Telefonassistent", "HalloPetra", "heykiki",
            "Parloa", "Cognigy", "voiceOne", "Aaron.ai", "Synthflow", "smao.ai", "Safina AI", "RufLab"
        ])
        c.execute("INSERT INTO scout_config VALUES (1,?,?,'de',?)",
                  (kw, comp, datetime.now().isoformat()))
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
        c.execute("""INSERT INTO scout_results
                     (type,title,source,url,summary,relevance,created_at)
                     VALUES (?,?,?,?,?,?,?)""",
                  (r.get("type",""), r.get("title",""), r.get("source",""),
                   r.get("url",""), r.get("summary",""),
                   r.get("relevance",""), datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_results(limit=30):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""SELECT type,title,source,url,summary,relevance,created_at
                 FROM scout_results ORDER BY id DESC LIMIT ?""", (limit,))
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
# TAVILY LIVE SUCHE
# ============================================================
def tavily_search(query, api_key, max_results=5):
    """Live Web-Suche via Tavily API"""
    try:
        url = "https://api.tavily.com/search"
        payload = json.dumps({
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": max_results,
            "include_answer": False,
            "include_raw_content": False
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("results", [])
    except Exception as e:
        st.warning(f"Tavily Suche fehlgeschlagen für '{query}': {e}")
        return []

# ============================================================
# SCOUT AGENT MIT LIVE DATEN
# ============================================================
def run_scout(keywords, competitors, language):
    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
    tavily_key = st.secrets.get("TAVILY_API_KEY", os.environ.get("TAVILY_API_KEY", ""))

    if not anthropic_key:
        st.error("⚠ ANTHROPIC_API_KEY fehlt in Secrets!"); return []
    if not tavily_key:
        st.error("⚠ TAVILY_API_KEY fehlt in Secrets!"); return []

    client = anthropic.Anthropic(api_key=anthropic_key)

    # SCHRITT 1: Live Web-Suche mit Tavily
    status = st.empty()
    status.markdown("🔍 **Schritt 1/3:** Suche live im Web...")

    all_search_results = []
    search_queries = [
        f"{keywords[0]} DACH 2026 news",
        f"{keywords[1] if len(keywords) > 1 else keywords[0]} aktuell",
        f"fonio.ai OR VITAS OR HalloPetra news 2026",
        f"KI Telefonassistent Markt Deutschland 2026",
    ]

    # Top 3 Konkurrenten einzeln suchen
    for comp in competitors[:3]:
        search_queries.append(f"{comp} news update 2026")

    search_urls = {}
    for query in search_queries[:6]:  # Max 6 Suchen
        results = tavily_search(query, tavily_key, max_results=3)
        for r in results:
            title = r.get("title", "")
            content = r.get("content", "")
            url = r.get("url", "")
            if title and content:
                all_search_results.append({
                    "title": title,
                    "content": content[:500],
                    "url": url,
                    "query": query
                })
                if url:
                    search_urls[title[:50]] = url

    status.markdown(f"📊 **Schritt 2/3:** {len(all_search_results)} Live-Artikel gefunden — Claude analysiert...")

    # SCHRITT 2: Claude analysiert die echten Live-Daten
    search_context = "\n\n".join([
        f"ARTIKEL: {r['title']}\nURL: {r['url']}\nINHALT: {r['content']}"
        for r in all_search_results[:15]
    ])

    prompt = f"""Du bist der Scout-Agent für VIKIphone (KI-Telefonassistenz SaaS von Rynon, Deutschland).

VIKIphone USPs:
- Zero-Latency Konversation (kein Gedenksekunden)
- DSGVO Medical Mode (Arztpraxen - einzigartig am Markt)
- 24/7 Betrieb mit dedizierter Festnetz-Rufnummer
- Webhook API für CRM-Integration
- Automatische Datenlöschung nach 30 Tagen

ECHTE LIVE-DATEN VOM WEB (gerade gesucht):
{search_context}

ÜBERWACHTE KONKURRENTEN: {', '.join(competitors)}
KEYWORDS: {', '.join(keywords)}

Analysiere diese echten Web-Daten und erstelle einen Marktbericht als JSON-Array.
Nutze NUR Informationen aus den obigen echten Artikeln. Erfinde nichts.

Erstelle mindestens 8 Einträge:
- 3x "TREND" - echte Markttrends aus den Artikeln
- 3x "KONKURRENZ" - was die Konkurrenten gerade machen (aus echten Daten)
- 2x "CHANCE" - konkrete Chancen für VIKIphone basierend auf den echten Daten

Format (NUR JSON, kein anderer Text):
[
  {{
    "type": "TREND",
    "title": "Kurzer prägnanter Titel",
    "source": "Name der Quelle / Website",
    "url": "URL des Artikels oder leer",
    "summary": "2-3 Sätze was genau passiert und warum das für VIKIphone wichtig ist",
    "relevance": "HOCH"
  }}
]

Antworte NUR mit dem JSON-Array."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        text = msg.content[0].text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        results = json.loads(text)
        status.markdown(f"✅ **Schritt 3/3:** Analyse abgeschlossen — {len(results)} Erkenntnisse!")
        return results

    except Exception as e:
        status.error(f"Claude Fehler: {e}")
        return []

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center; margin-bottom:32px;'>
            <div style='font-size:48px; margin-bottom:8px;'>🔵</div>
            <div style='font-family: Plus Jakarta Sans; font-size:28px; font-weight:800;
                        color:#29B6F6; margin-bottom:4px;'>VIKIphone</div>
            <div style='font-size:13px; color:#555; font-weight:500;'>Company OS · Internal Dashboard</div>
        </div>
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
        </div></div>
        """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================
else:
    with st.sidebar:
        st.markdown("""
        <div style='padding:20px 16px 12px;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <div style='font-size:22px;'>🔵</div>
                <div>
                    <div style='font-family: Plus Jakarta Sans; font-size:15px; font-weight:700; color:#29B6F6;'>VIKIphone</div>
                    <div style='font-size:10px; color:#444;'>Company OS</div>
                </div>
            </div>
        </div>
        <div style='height:1px; background:#1e1e1e; margin:0 16px 12px;'></div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='padding:8px 16px; margin-bottom:8px;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <div style='width:32px; height:32px; background:rgba(41,182,246,0.15);
                            border-radius:8px; font-size:14px; display:flex;
                            align-items:center; justify-content:center;'>👤</div>
                <div>
                    <div style='font-size:13px; font-weight:600; color:#fff;'>{st.session_state.username.title()}</div>
                    <div style='font-size:11px; color:#4CAF50;'>● Online</div>
                </div>
            </div>
        </div>
        <div style='height:1px; background:#1e1e1e; margin:0 16px 8px;'></div>
        <div style='padding:4px 16px; font-size:10px; font-weight:600; color:#333;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;'>Navigation</div>
        """, unsafe_allow_html=True)

        seite = st.radio("nav", [
            "📡  Marketing", "🎯  Vertrieb", "🛰  Support", "🗄  Backoffice", "👾  HR"
        ], label_visibility="collapsed")

        st.markdown("<div style='height:1px; background:#1e1e1e; margin:8px 16px;'></div>", unsafe_allow_html=True)

        if st.button("Sign out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # MARKETING
    if "Marketing" in seite:
        st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:2px;'>
            <div class='page-header'>Marketing Zentrale</div>
            <span class='live-badge'>● LIVE</span>
        </div>
        <div class='page-sub'>VIKIphone Growth · KI-gesteuerte Echtzeit-Marktanalyse</div>
        """, unsafe_allow_html=True)

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

        agent = st.radio("Agent", [
            "🔭 Scout", "🧠 Growth Hacker", "✍️ Creator",
            "🏥 Nischen-Spezialist", "🔍 SEO-Architekt"
        ], horizontal=True, label_visibility="collapsed")

        st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)

        if "Scout" in agent:
            col_left, col_right = st.columns([2,1])

            with col_left:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>⚙️ Keywords konfigurieren</div>
                """, unsafe_allow_html=True)
                kw_text = st.text_area(
                    "Ein Keyword pro Zeile — Scout sucht diese live im Web",
                    value="\n".join(kw), height=180,
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🎯 Konkurrenten überwachen</div>
                """, unsafe_allow_html=True)
                comp_text = st.text_area(
                    "Ein Konkurrent pro Zeile — Scout sucht News zu jedem",
                    value="\n".join(comp), height=180,
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

                lang_sel = st.selectbox("Ausgabe-Sprache", ["de","en"],
                                        index=0 if lang=="de" else 1)

                if st.button("💾  Konfiguration speichern", use_container_width=True):
                    new_kw = [k.strip() for k in kw_text.split("\n") if k.strip()]
                    new_comp = [c.strip() for c in comp_text.split("\n") if c.strip()]
                    save_scout_config(new_kw, new_comp, lang_sel)
                    st.success("✅ Gespeichert!")

            with col_right:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🔭 Live Scout starten</div>
                    <div style='font-size:13px; color:#555; margin-bottom:16px; line-height:1.8;'>
                        <span class='live-badge' style='margin-bottom:8px; display:inline-flex;'>● LIVE Web-Suche</span><br><br>
                        <span style='color:#29B6F6'>①</span> Tavily sucht live im Web<br>
                        <span style='color:#29B6F6'>②</span> Echte Artikel werden geladen<br>
                        <span style='color:#29B6F6'>③</span> Claude analysiert die Daten<br>
                        <span style='color:#29B6F6'>④</span> Ergebnisse werden gespeichert
                    </div>
                """, unsafe_allow_html=True)

                if st.button("▶  Jetzt live scannen", use_container_width=True):
                    cur_kw = [k.strip() for k in kw_text.split("\n") if k.strip()]
                    cur_comp = [c.strip() for c in comp_text.split("\n") if c.strip()]
                    results = run_scout(cur_kw, cur_comp, lang_sel)
                    if results:
                        save_results(results)
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(f"""<div class='config-section'>
                    <div class='config-label'>📊 Status</div>
                    <div style='font-size:13px; color:#555;'>
                        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                            <span>Ergebnisse gesamt</span>
                            <span style='color:#fff; font-weight:600;'>{count}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                            <span>Keywords aktiv</span>
                            <span style='color:#29B6F6; font-weight:600;'>{len(kw)}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>Konkurrenten</span>
                            <span style='color:#29B6F6; font-weight:600;'>{len(comp)}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # ERGEBNISSE
            st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;'>
                <div style='font-size:15px; font-weight:600; color:#fff;'>Live Ergebnisse</div>
                <span class='live-badge'>● Echtzeit Web-Daten</span>
            </div>
            """, unsafe_allow_html=True)

            rows = get_results(30)
            if rows:
                filter_col, _ = st.columns([1,3])
                with filter_col:
                    filt = st.selectbox("Filter", ["Alle","TREND","KONKURRENZ","CHANCE"],
                                        label_visibility="collapsed")

                for row in rows:
                    rtype, title, source, url, summary, relevance, created_at = row
                    if filt != "Alle" and rtype != filt: continue

                    badge_class = {
                        "TREND":"badge-trend",
                        "KONKURRENZ":"badge-konkurrenz",
                        "CHANCE":"badge-chance"
                    }.get(rtype, "badge-trend")
                    rel_class = {
                        "HOCH":"rel-high","MITTEL":"rel-mid","NIEDRIG":"rel-low"
                    }.get(relevance,"rel-low")

                    url_html = f'<a href="{url}" target="_blank" class="source-link">🔗 Quelle öffnen</a>' if url else ""

                    st.markdown(f"""
                    <div class='result-item'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span class='result-badge {badge_class}'>{rtype}</span>
                            <span class='{rel_class}'>↑ {relevance}</span>
                        </div>
                        <div class='result-title-text'>{title}</div>
                        <div class='result-summary-text'>{summary}</div>
                        <div class='result-meta' style='display:flex; justify-content:space-between; align-items:center;'>
                            <span>📡 {source} · {created_at[:10]}</span>
                            {url_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align:center; padding:60px; color:#333; font-size:14px;'>
                    Noch keine Daten · Live Scout starten
                </div>
                """, unsafe_allow_html=True)

        else:
            labels = {
                "Growth Hacker": ("🧠", "Analysiert virale Trends und entwickelt Kampagnen-Strategien"),
                "Creator": ("✍️", "Schreibt Posts, Newsletter und Blogartikel basierend auf Scout-Daten"),
                "Nischen-Spezialist": ("🏥", "Content für Arztpraxen, Handwerker und Kanzleien"),
                "SEO-Architekt": ("🔍", "Keyword-Research und SEO-optimierte Artikel"),
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

    elif "Vertrieb" in seite:
        st.markdown("<div class='page-header'>Vertrieb</div><div class='page-sub'>Lead Management & Demo-Buchungen</div>", unsafe_allow_html=True)
        for n,d in [("🎯 Demo-Hunter","Findet und kontaktiert potenzielle VIKIphone Kunden"),("📬 Lead-Hunter","Personalisierte Outreach E-Mails für Inbound Leads")]:
            st.markdown(f"""<div class='coming-soon' style='margin-bottom:12px;'>
                <div style='font-size:32px; margin-bottom:8px;'>{n.split()[0]}</div>
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
            <div style='font-size:13px; color:#555; margin-bottom:12px;'>OCR PDF Extraktion → CSV in SQLite</div>
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
