import streamlit as st
import anthropic
import json
import sqlite3
import os
from datetime import datetime
import urllib.request
import urllib.parse
import re

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
    --viki-blue-light: #4FC3F7;
    --viki-blue-glow: rgba(41,182,246,0.15);
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
    --purple: #9C27B0;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-black) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 24px 32px !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio label {
    background: transparent !important; border: none !important;
    border-radius: 8px !important; padding: 10px 16px !important;
    color: var(--text-secondary) !important; font-family: 'Inter', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important; transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--viki-blue-glow) !important; color: var(--viki-blue) !important;
}

.stButton > button {
    background: var(--viki-blue) !important; color: #000 !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
    font-size: 13px !important; padding: 10px 20px !important;
    transition: all 0.2s !important; box-shadow: 0 0 20px rgba(41,182,246,0.3) !important;
}
.stButton > button:hover {
    background: var(--viki-blue-light) !important;
    box-shadow: 0 0 30px rgba(41,182,246,0.5) !important; transform: translateY(-1px) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-input) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important; font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--viki-blue) !important;
    box-shadow: 0 0 0 3px rgba(41,182,246,0.1) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label {
    color: var(--text-secondary) !important; font-family: 'Inter', sans-serif !important;
    font-size: 12px !important; font-weight: 500 !important;
    text-transform: none !important; letter-spacing: 0 !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }

/* METRIKEN */
.metric-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 20px 24px; position: relative; overflow: hidden;
}
.metric-number {
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 32px;
    font-weight: 700; color: var(--text-primary); line-height: 1; margin-bottom: 4px;
}
.metric-label { font-size: 12px; color: var(--text-secondary); font-weight: 500; }
.metric-icon {
    position: absolute; top: 20px; right: 20px;
    width: 36px; height: 36px; background: var(--viki-blue-glow);
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 16px;
}

/* SECTION HEADERS */
.section-header {
    display: flex; align-items: center; gap: 10px;
    padding: 16px 0 12px; margin-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.section-icon {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center; font-size: 16px;
}
.section-title-text {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 15px; font-weight: 700; color: var(--text-primary);
}
.section-count {
    margin-left: auto; font-size: 12px; color: var(--text-muted);
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 20px; padding: 2px 10px;
}

/* RESULT CARDS */
.result-item {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px 20px; margin-bottom: 8px; transition: all 0.2s;
}
.result-item:hover { border-color: #2a2a2a; background: var(--bg-card-hover); }

.result-badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
}
/* Badge Farben */
.badge-trend { background: rgba(41,182,246,0.1); color: #29B6F6; }
.badge-konkurrenz { background: rgba(244,67,54,0.1); color: #f44336; }
.badge-chance { background: rgba(76,175,80,0.1); color: #4CAF50; }
.badge-alarm { background: rgba(255,152,0,0.15); color: #FF9800; border: 1px solid rgba(255,152,0,0.3); }
.badge-feature { background: rgba(156,39,176,0.1); color: #9C27B0; }
.badge-bewertung { background: rgba(255,235,59,0.1); color: #FFC107; }
.badge-funding { background: rgba(0,188,212,0.1); color: #00BCD4; }

.result-title-text {
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px;
    font-weight: 600; color: var(--text-primary); margin: 8px 0 4px;
}
.result-summary-text { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
.result-meta { font-size: 11px; color: var(--text-muted); margin-top: 8px; }

/* ALARM CARD */
.alarm-card {
    background: rgba(255,152,0,0.05); border: 1px solid rgba(255,152,0,0.3);
    border-left: 3px solid #FF9800; border-radius: 12px;
    padding: 16px 20px; margin-bottom: 8px;
}
.alarm-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; font-weight: 700; color: #FF9800; }

/* KNOWLEDGE BASE */
.kb-item {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 16px; margin-bottom: 8px;
    display: flex; align-items: center; gap: 12px;
}
.kb-icon {
    width: 36px; height: 36px; background: var(--viki-blue-glow);
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-size: 16px; flex-shrink: 0;
}
.kb-title { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.kb-meta { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* CONTENT CARDS (Creator Output) */
.content-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px; margin-bottom: 12px;
}
.content-platform {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--viki-blue-glow); border: 1px solid rgba(41,182,246,0.3);
    color: var(--viki-blue); border-radius: 20px;
    padding: 3px 12px; font-size: 11px; font-weight: 600; margin-bottom: 12px;
}
.content-text {
    font-size: 14px; color: var(--text-primary); line-height: 1.7;
    white-space: pre-wrap; font-family: 'Inter', sans-serif;
}
.approve-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.3);
    color: #4CAF50; border-radius: 20px; padding: 3px 12px;
    font-size: 11px; font-weight: 600;
}
.pending-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(255,152,0,0.1); border: 1px solid rgba(255,152,0,0.3);
    color: #FF9800; border-radius: 20px; padding: 3px 12px;
    font-size: 11px; font-weight: 600;
}

/* MISC */
.config-section {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 20px; margin-bottom: 12px;
}
.config-label { font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; }
.page-header {
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px;
    font-weight: 700; color: var(--text-primary); margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: var(--text-secondary); margin-bottom: 24px; }
.viki-divider { height: 1px; background: var(--border); margin: 16px 0; }
.coming-soon {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 40px; text-align: center;
}
.live-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.3);
    color: #4CAF50; border-radius: 20px; padding: 3px 10px;
    font-size: 11px; font-weight: 600;
}
.rel-high { color: #4CAF50; font-size: 11px; font-weight: 600; }
.rel-mid  { color: #FF9800; font-size: 11px; font-weight: 600; }
.rel-low  { color: #555; font-size: 11px; font-weight: 600; }
.source-link { color: var(--viki-blue); font-size: 11px; text-decoration: none; }
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
        id INTEGER PRIMARY KEY, keywords TEXT, competitors TEXT,
        language TEXT DEFAULT 'de', updated_at TEXT
    )""")

    # Scout Results — erweitert mit section
    c.execute("""CREATE TABLE IF NOT EXISTS scout_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, section TEXT, title TEXT, source TEXT, url TEXT,
        summary TEXT, relevance TEXT, is_alarm INTEGER DEFAULT 0, created_at TEXT
    )""")
    try: c.execute("ALTER TABLE scout_results ADD COLUMN section TEXT")
    except: pass
    try: c.execute("ALTER TABLE scout_results ADD COLUMN is_alarm INTEGER DEFAULT 0")
    except: pass
    try: c.execute("ALTER TABLE scout_results ADD COLUMN url TEXT")
    except: pass

    # Knowledge Base
    c.execute("""CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, title TEXT, content TEXT, source_url TEXT,
        created_at TEXT
    )""")

    # Content (Creator Output)
    c.execute("""CREATE TABLE IF NOT EXISTS content_drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT, title TEXT, content TEXT,
        strategy TEXT, status TEXT DEFAULT 'pending',
        created_at TEXT
    )""")

    # Default Scout Config
    c.execute("SELECT COUNT(*) FROM scout_config")
    if c.fetchone()[0] == 0:
        kw = json.dumps([
            "KI Telefonassistent DACH", "Voice AI Deutschland",
            "KI Telefon Arztpraxis", "Telefonassistent SaaS",
            "KI Rezeption", "verpasste Anrufe Lösung",
            "24/7 Telefonservice", "DSGVO Telefonassistent"
        ])
        comp = json.dumps([
            "fonio.ai", "VITAS Telefonassistent", "HalloPetra", "heykiki",
            "Parloa", "Cognigy", "voiceOne", "Aaron.ai",
            "Synthflow", "smao.ai", "Safina AI", "RufLab"
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

def save_scout_results(results):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    for r in results:
        c.execute("""INSERT INTO scout_results
                     (type,section,title,source,url,summary,relevance,is_alarm,created_at)
                     VALUES (?,?,?,?,?,?,?,?,?)""",
                  (r.get("type",""), r.get("section","MARKT"),
                   r.get("title",""), r.get("source",""), r.get("url",""),
                   r.get("summary",""), r.get("relevance","MITTEL"),
                   1 if r.get("is_alarm") else 0,
                   datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_scout_results(limit=50):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""SELECT type,section,title,source,url,summary,relevance,is_alarm,created_at
                 FROM scout_results ORDER BY is_alarm DESC, id DESC LIMIT ?""", (limit,))
    rows = c.fetchall(); conn.close()
    return rows

def get_scout_count():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM scout_results")
    n = c.fetchone()[0]; conn.close()
    return n

def get_alarm_count():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM scout_results WHERE is_alarm=1")
    n = c.fetchone()[0]; conn.close()
    return n

def save_kb_item(type_, title, content, source_url=""):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("INSERT INTO knowledge_base (type,title,content,source_url,created_at) VALUES (?,?,?,?,?)",
              (type_, title, content, source_url, datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_kb_items():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT id,type,title,content,source_url,created_at FROM knowledge_base ORDER BY id DESC")
    rows = c.fetchall(); conn.close()
    return rows

def delete_kb_item(item_id):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("DELETE FROM knowledge_base WHERE id=?", (item_id,))
    conn.commit(); conn.close()

def get_kb_context():
    items = get_kb_items()
    if not items: return ""
    context = "=== VIKIPHONE KNOWLEDGE BASE ===\n\n"
    for item in items:
        context += f"[{item[1].upper()}] {item[2]}\n{item[3][:800]}\n\n"
    return context

def save_content_draft(platform, title, content, strategy):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("INSERT INTO content_drafts (platform,title,content,strategy,status,created_at) VALUES (?,?,?,?,?,?)",
              (platform, title, content, strategy, "pending", datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_content_drafts():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT id,platform,title,content,strategy,status,created_at FROM content_drafts ORDER BY id DESC")
    rows = c.fetchall(); conn.close()
    return rows

def approve_content(draft_id):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("UPDATE content_drafts SET status='approved' WHERE id=?", (draft_id,))
    conn.commit(); conn.close()

def delete_content(draft_id):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("DELETE FROM content_drafts WHERE id=?", (draft_id,))
    conn.commit(); conn.close()

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
# TAVILY SUCHE
# ============================================================
def tavily_search(query, api_key, max_results=5):
    try:
        url = "https://api.tavily.com/search"
        payload = json.dumps({
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": max_results,
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("results", [])
    except Exception as e:
        return []

# ============================================================
# YOUTUBE TRANSKRIPT LADEN
# ============================================================
def get_youtube_transcript(video_url, api_key):
    """Lädt YouTube Video Info via Tavily"""
    video_id = ""
    patterns = [r'v=([a-zA-Z0-9_-]{11})', r'youtu\.be/([a-zA-Z0-9_-]{11})']
    for p in patterns:
        m = re.search(p, video_url)
        if m: video_id = m.group(1); break
    if not video_id:
        return None, "Ungültige YouTube URL"

    tavily_key = st.secrets.get("TAVILY_API_KEY", os.environ.get("TAVILY_API_KEY",""))
    results = tavily_search(f"youtube video {video_id} transcript summary marketing", tavily_key, 3)

    anthropic_key = api_key
    client = anthropic.Anthropic(api_key=anthropic_key)

    context = "\n".join([r.get("content","") for r in results[:3]])

    prompt = f"""Du analysierst ein YouTube Marketing-Video (ID: {video_id}).

Gefundener Kontext aus dem Web:
{context[:2000]}

Extrahiere die wichtigsten Marketing-Strategien und Lektionen aus diesem Video.
Formatiere als strukturierte Zusammenfassung mit:
- Hauptthema
- 5-7 Key Marketing-Strategien/Lektionen
- Wie diese für VIKIphone (KI-Telefonassistenz B2B SaaS) anwendbar sind

Antworte auf Deutsch."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=1500,
            messages=[{"role":"user","content":prompt}])
        return msg.content[0].text, None
    except Exception as e:
        return None, str(e)

# ============================================================
# SCOUT AGENT — ERWEITERT MIT ALARM & SEKTIONEN
# ============================================================
def run_scout(keywords, competitors, language):
    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY",""))
    tavily_key = st.secrets.get("TAVILY_API_KEY", os.environ.get("TAVILY_API_KEY",""))

    if not anthropic_key: st.error("⚠ ANTHROPIC_API_KEY fehlt!"); return []
    if not tavily_key: st.error("⚠ TAVILY_API_KEY fehlt!"); return []

    client = anthropic.Anthropic(api_key=anthropic_key)
    status = st.empty()
    progress = st.progress(0)

    # SCHRITT 1: Live Suchen
    status.markdown("🔍 **Schritt 1/4:** Suche live im Web nach Marktdaten...")
    progress.progress(10)

    all_results = []
    searches = [
        # Markt & Trends
        (f"KI Telefonassistent DACH Markt 2026 news", "MARKT"),
        (f"Voice AI B2B Deutschland aktuell 2026", "MARKT"),
        (f"KI Telefon Arztpraxis Handwerker Lösung 2026", "NISCHEN"),
        # Konkurrenz gezielt
        (f"fonio.ai news update features 2026", "KONKURRENZ"),
        (f"VITAS Telefonassistent news 2026", "KONKURRENZ"),
        (f"HalloPetra heykiki voiceOne news 2026", "KONKURRENZ"),
        (f"Parloa Cognigy KI Telefon enterprise 2026", "KONKURRENZ"),
        # Alarm-Signale
        (f"fonio.ai OR VITAS OR HalloPetra Preis Rabatt Aktion 2026", "ALARM"),
        (f"KI Telefonassistent neue features launch 2026", "ALARM"),
        (f"fonio.ai OR voiceOne bewertung kritik problem 2026", "ALARM"),
    ]

    raw_data = {}
    for i, (query, section) in enumerate(searches):
        results = tavily_search(query, tavily_key, max_results=4)
        raw_data[section] = raw_data.get(section, [])
        for r in results:
            if r.get("title") and r.get("content"):
                raw_data[section].append({
                    "title": r.get("title",""),
                    "content": r.get("content","")[:400],
                    "url": r.get("url",""),
                    "query": query
                })
        progress.progress(10 + int((i/len(searches))*40))

    status.markdown(f"📊 **Schritt 2/4:** Web-Daten gesammelt — Claude analysiert...")
    progress.progress(55)

    # SCHRITT 2: Kontext aufbauen
    context_parts = []
    for section, items in raw_data.items():
        if items:
            context_parts.append(f"\n=== {section} DATEN ===")
            for item in items[:4]:
                context_parts.append(f"Titel: {item['title']}\nURL: {item['url']}\nInhalt: {item['content']}")

    full_context = "\n".join(context_parts)

    # SCHRITT 3: Claude analysiert
    status.markdown("🧠 **Schritt 3/4:** Claude erstellt Marktbericht...")
    progress.progress(65)

    prompt = f"""Du bist der Elite-Scout-Agent für VIKIphone (KI-Telefonassistenz SaaS, Rynon, Deutschland).

VIKIphone USPs:
- Zero-Latency Konversation (einzigartig — kein Gedenksekunden)
- DSGVO Medical Mode (nur VIKIphone hat das für Arztpraxen)
- 24/7 mit dedizierter Festnetz-Rufnummer
- Webhook API für CRM-Integration
- Automatische 30-Tage Datenlöschung

ECHTE WEB-DATEN VON HEUTE:
{full_context[:4000]}

Erstelle einen strukturierten Marktbericht als JSON-Array.
Nutze NUR echte Informationen aus den Web-Daten.

SEKTIONEN (section Feld):
- "MARKTTRENDS" → Was bewegt den Markt gerade?
- "KONKURRENZ_ANALYSE" → Was machen Konkurrenten?
- "ALARM" → Dringende Signale (neues Feature, Preissenkung, negative Bewertungen bei Konkurrenz)
- "NISCHEN_CHANCE" → Konkrete Chancen in spezifischen Branchen
- "STRATEGISCHE_CHANCE" → Größere strategische Möglichkeiten

TYPES:
- "TREND", "KONKURRENZ", "ALARM", "FEATURE", "BEWERTUNG", "FUNDING", "CHANCE"

FORMAT (NUR JSON):
[
  {{
    "type": "ALARM",
    "section": "ALARM",
    "title": "Kurzer prägnanter Titel",
    "source": "Website/Quelle",
    "url": "URL oder leer",
    "summary": "2-3 Sätze: Was passiert genau? Warum wichtig für VIKIphone? Was sollte VIKIphone tun?",
    "relevance": "HOCH",
    "is_alarm": true
  }}
]

Erstelle mindestens 12 Einträge:
- 3x section "MARKTTRENDS"
- 3x section "KONKURRENZ_ANALYSE"  
- 2x section "ALARM" (is_alarm: true, nur wenn wirklich relevant)
- 2x section "NISCHEN_CHANCE"
- 2x section "STRATEGISCHE_CHANCE"

Antworte NUR mit JSON."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=4000,
            messages=[{"role":"user","content":prompt}])
        text = msg.content[0].text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
        results = json.loads(text)
        progress.progress(100)
        status.markdown(f"✅ **Fertig!** {len(results)} Erkenntnisse — {sum(1 for r in results if r.get('is_alarm'))} Alarme")
        return results
    except Exception as e:
        st.error(f"Fehler: {e}"); return []

# ============================================================
# GROWTH HACKER AGENT
# ============================================================
def run_growth_hacker():
    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY",""))
    if not anthropic_key: st.error("⚠ ANTHROPIC_API_KEY fehlt!"); return []

    client = anthropic.Anthropic(api_key=anthropic_key)

    # Scout Daten holen
    scout_rows = get_scout_results(20)
    scout_context = "\n".join([f"[{r[0]}] {r[2]}: {r[5]}" for r in scout_rows[:10]])

    # Knowledge Base holen
    kb_context = get_kb_context()

    if not kb_context:
        st.warning("⚠ Knowledge Base ist leer! Lade zuerst VIKIphone Docs und YouTube Videos hoch.")
        return []

    prompt = f"""Du bist der Growth Hacker Agent für VIKIphone — der beste B2B SaaS Marketing Stratege der Welt.

Du hast Zugang zu:
1. Echten Marktdaten vom Scout
2. Gelernten Marketing-Strategien aus der Knowledge Base

AKTUELLE MARKTDATEN (vom Scout):
{scout_context}

GELERNTE MARKETING-STRATEGIEN (Knowledge Base):
{kb_context[:3000]}

VIKIphone USPs:
- Zero-Latency Konversation (kein Gedenksekunden — einzigartig)
- DSGVO Medical Mode (Arztpraxen — kein Konkurrent hat das)
- 24/7 dedizierte Festnetz-Rufnummer
- Webhook API für CRM-Integration

Kombiniere die Marktdaten mit den gelernten Marketing-Strategien.
Erstelle 3 konkrete Kampagnen-Strategien für VIKIphone als JSON:

[
  {{
    "strategie_name": "Name der Kampagne",
    "gelernte_methode": "Welche Marketing-Strategie/Framework du anwendest (z.B. Problem-Agitate-Solve von Hormozi)",
    "markt_trigger": "Welchen Markttrend/Signal du nutzt",
    "zielgruppe": "Genau wer angesprochen wird",
    "kern_botschaft": "Die eine starke Botschaft",
    "plattformen": ["LinkedIn", "Instagram"],
    "content_ideen": ["Idee 1", "Idee 2", "Idee 3"]
  }}
]

Antworte NUR mit JSON."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=2000,
            messages=[{"role":"user","content":prompt}])
        text = msg.content[0].text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"Growth Hacker Fehler: {e}"); return []

# ============================================================
# CREATOR AGENT
# ============================================================
def run_creator(strategy, platform):
    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY",""))
    if not anthropic_key: return ""

    client = anthropic.Anthropic(api_key=anthropic_key)

    platform_guides = {
        "LinkedIn": "Professionell, 150-300 Wörter, Hook in Zeile 1, 3-5 Absätze, CTA am Ende, 3-5 Hashtags",
        "Instagram": "Emotional, 80-150 Wörter, starker Hook, Emojis einsetzen, CTA, 10-15 Hashtags",
        "Newsletter": "Persönlich, 200-400 Wörter, Betreffzeile + Fließtext + CTA Button",
        "Blog": "SEO-optimiert, 400-600 Wörter Intro, H2 Überschriften, Keyword-Integration",
    }

    prompt = f"""Du bist der beste B2B SaaS Copywriter der Welt.

Schreibe fertigen {platform} Content für VIKIphone basierend auf dieser Strategie:

STRATEGIE: {strategy.get('strategie_name','')}
METHODE: {strategy.get('gelernte_methode','')}
ZIELGRUPPE: {strategy.get('zielgruppe','')}
KERN-BOTSCHAFT: {strategy.get('kern_botschaft','')}

PLATFORM-GUIDE für {platform}: {platform_guides.get(platform, '')}

VIKIphone USPs die du nutzen kannst:
- Zero-Latency (kein Gedenksekunden — Kunden merken keinen Unterschied zu einem Menschen)
- DSGVO Medical Mode (Arztpraxen können sicher telefonieren)
- 24/7 niemals verpasste Anrufe
- Dedizierte Festnetz-Rufnummer

Schreibe den FERTIGEN POST — direkt verwendbar, kein Kommentar darum.
Auf Deutsch. Hook muss sofort grabben."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=1000,
            messages=[{"role":"user","content":prompt}])
        return msg.content[0].text.strip()
    except Exception as e:
        return f"Fehler: {e}"

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
            <div style='font-family: Plus Jakarta Sans; font-size:28px; font-weight:800; color:#29B6F6; margin-bottom:4px;'>VIKIphone</div>
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
        st.markdown("<div style='text-align:center; margin-top:16px; font-size:12px; color:#333;'>admin / admin123</div></div>", unsafe_allow_html=True)

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

        alarm_count = get_alarm_count()
        alarm_html = f'<span style="background:#FF9800; color:#000; border-radius:10px; padding:1px 6px; font-size:10px; font-weight:700; margin-left:4px;">{alarm_count}</span>' if alarm_count > 0 else ""

        st.markdown(f"""
        <div style='padding:8px 16px; margin-bottom:8px;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <div style='width:32px; height:32px; background:rgba(41,182,246,0.15); border-radius:8px; font-size:14px; display:flex; align-items:center; justify-content:center;'>👤</div>
                <div>
                    <div style='font-size:13px; font-weight:600; color:#fff;'>{st.session_state.username.title()}</div>
                    <div style='font-size:11px; color:#4CAF50;'>● Online</div>
                </div>
            </div>
        </div>
        <div style='height:1px; background:#1e1e1e; margin:0 16px 8px;'></div>
        <div style='padding:4px 16px; font-size:10px; font-weight:600; color:#333; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;'>Navigation</div>
        """, unsafe_allow_html=True)

        seite = st.radio("nav", [
            "📡  Marketing", "🎯  Vertrieb", "🛰  Support", "🗄  Backoffice", "👾  HR"
        ], label_visibility="collapsed")

        st.markdown("<div style='height:1px; background:#1e1e1e; margin:8px 16px;'></div>", unsafe_allow_html=True)

        if alarm_count > 0:
            st.markdown(f"""
            <div style='margin:8px 16px; padding:10px 14px; background:rgba(255,152,0,0.08);
                        border:1px solid rgba(255,152,0,0.3); border-radius:8px;'>
                <div style='font-size:12px; font-weight:600; color:#FF9800;'>🚨 {alarm_count} Alarm{'e' if alarm_count > 1 else ''}</div>
                <div style='font-size:11px; color:#666; margin-top:2px;'>Konkurrenz-Aktivität erkannt</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Sign out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # ============================================================
    # MARKETING MODULE
    # ============================================================
    if "Marketing" in seite:
        st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:2px;'>
            <div class='page-header'>Marketing Zentrale</div>
            <span class='live-badge'>● LIVE</span>
        </div>
        <div class='page-sub'>VIKIphone Growth · KI-gesteuerte Echtzeit-Marktanalyse & Content-Pipeline</div>
        """, unsafe_allow_html=True)

        # METRIKEN
        count = get_scout_count()
        alarms = get_alarm_count()
        kw, comp, lang = get_scout_config()
        kb_items = get_kb_items()
        drafts = get_content_drafts()
        pending = sum(1 for d in drafts if d[5] == "pending")

        c1,c2,c3,c4,c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>📡</div>
                <div class='metric-number'>{count}</div>
                <div class='metric-label'>Scout Ergebnisse</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card' style='{"border-color: rgba(255,152,0,0.4);" if alarms > 0 else ""}'>
                <div class='metric-icon' style='background:rgba(255,152,0,0.1);'>🚨</div>
                <div class='metric-number' style='color:{"#FF9800" if alarms > 0 else "white"}'>{alarms}</div>
                <div class='metric-label'>Alarme</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon' style='background:rgba(156,39,176,0.1);'>🧠</div>
                <div class='metric-number'>{len(kb_items)}</div>
                <div class='metric-label'>Knowledge Base</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon' style='background:rgba(76,175,80,0.1);'>✍️</div>
                <div class='metric-number'>{pending}</div>
                <div class='metric-label'>Entwürfe ausstehend</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>🎯</div>
                <div class='metric-number'>{len(comp)}</div>
                <div class='metric-label'>Konkurrenten</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # AGENT TABS
        agent = st.radio("Agent", [
            "🔭 Scout", "📚 Knowledge Base", "🧠 Growth Hacker", "✍️ Creator & Freigabe",
            "🏥 Nischen-Spezialist", "🔍 SEO-Architekt"
        ], horizontal=True, label_visibility="collapsed")

        st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)

        # ============================================================
        # SCOUT
        # ============================================================
        if "Scout" in agent:
            col_left, col_right = st.columns([2,1])
            with col_left:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>⚙️ Keywords konfigurieren</div>
                """, unsafe_allow_html=True)
                kw_text = st.text_area("Keywords", value="\n".join(kw), height=150, label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🎯 Konkurrenten überwachen</div>
                """, unsafe_allow_html=True)
                comp_text = st.text_area("Konkurrenten", value="\n".join(comp), height=150, label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)

                lang_sel = st.selectbox("Sprache", ["de","en"], index=0 if lang=="de" else 1)
                if st.button("💾 Konfiguration speichern", use_container_width=True):
                    save_scout_config(
                        [k.strip() for k in kw_text.split("\n") if k.strip()],
                        [c.strip() for c in comp_text.split("\n") if c.strip()],
                        lang_sel)
                    st.success("✅ Gespeichert!")

            with col_right:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🔭 Live Scout</div>
                    <div style='font-size:13px; color:#555; margin-bottom:16px; line-height:1.8;'>
                        <span class='live-badge'>● Echtzeit</span><br><br>
                        <span style='color:#29B6F6'>①</span> Tavily sucht live im Web<br>
                        <span style='color:#29B6F6'>②</span> Markt + Konkurrenz + Alarme<br>
                        <span style='color:#29B6F6'>③</span> Claude analysiert & bewertet<br>
                        <span style='color:#FF9800'>④</span> Alarme bei wichtigen Signalen
                    </div>
                """, unsafe_allow_html=True)
                if st.button("▶ Jetzt live scannen", use_container_width=True):
                    cur_kw = [k.strip() for k in kw_text.split("\n") if k.strip()]
                    cur_comp = [c.strip() for c in comp_text.split("\n") if c.strip()]
                    results = run_scout(cur_kw, cur_comp, lang_sel)
                    if results:
                        save_scout_results(results)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(f"""<div class='config-section'>
                    <div class='config-label'>📊 Status</div>
                    <div style='font-size:13px; color:#555;'>
                        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                            <span>Ergebnisse</span><span style='color:#fff; font-weight:600;'>{count}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                            <span>🚨 Alarme</span><span style='color:#FF9800; font-weight:600;'>{alarms}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                            <span>Keywords</span><span style='color:#29B6F6; font-weight:600;'>{len(kw)}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>Konkurrenten</span><span style='color:#29B6F6; font-weight:600;'>{len(comp)}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # ERGEBNISSE IN SEKTIONEN
            st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)

            rows = get_scout_results(50)
            if rows:
                # ALARME ZUERST
                alarm_rows = [r for r in rows if r[7] == 1]
                if alarm_rows:
                    st.markdown("""
                    <div class='section-header'>
                        <div class='section-icon' style='background:rgba(255,152,0,0.1);'>🚨</div>
                        <div class='section-title-text'>Alarme — Sofortige Aufmerksamkeit</div>
                    </div>
                    """, unsafe_allow_html=True)
                    for row in alarm_rows:
                        rtype, section, title, source, url, summary, relevance, is_alarm, created_at = row
                        url_html = f'<a href="{url}" target="_blank" class="source-link">🔗 Quelle</a>' if url else ""
                        st.markdown(f"""
                        <div class='alarm-card'>
                            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
                                <span class='result-badge badge-alarm'>🚨 {rtype}</span>
                                <span class='rel-high'>↑ HOCH</span>
                            </div>
                            <div class='alarm-title'>{title}</div>
                            <div class='result-summary-text' style='margin-top:6px;'>{summary}</div>
                            <div class='result-meta' style='display:flex; justify-content:space-between;'>
                                <span>📡 {source} · {created_at[:10]}</span>{url_html}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # SEKTIONEN
                sections = {
                    "MARKTTRENDS": ("📈", "Markttrends", "rgba(41,182,246,0.1)"),
                    "KONKURRENZ_ANALYSE": ("🎯", "Konkurrenz-Analyse", "rgba(244,67,54,0.1)"),
                    "NISCHEN_CHANCE": ("🏥", "Nischen-Chancen", "rgba(76,175,80,0.1)"),
                    "STRATEGISCHE_CHANCE": ("💡", "Strategische Chancen", "rgba(156,39,176,0.1)"),
                }

                for sec_key, (icon, sec_label, bg) in sections.items():
                    sec_rows = [r for r in rows if r[1] == sec_key and r[7] == 0]
                    if not sec_rows: continue

                    st.markdown(f"""
                    <div class='section-header' style='margin-top:20px;'>
                        <div class='section-icon' style='background:{bg};'>{icon}</div>
                        <div class='section-title-text'>{sec_label}</div>
                        <div class='section-count'>{len(sec_rows)} Einträge</div>
                    </div>
                    """, unsafe_allow_html=True)

                    for row in sec_rows:
                        rtype, section, title, source, url, summary, relevance, is_alarm, created_at = row
                        badge_map = {
                            "TREND":"badge-trend","KONKURRENZ":"badge-konkurrenz",
                            "CHANCE":"badge-chance","FEATURE":"badge-feature",
                            "BEWERTUNG":"badge-bewertung","FUNDING":"badge-funding",
                            "ALARM":"badge-alarm"
                        }
                        badge_class = badge_map.get(rtype, "badge-trend")
                        rel_class = {"HOCH":"rel-high","MITTEL":"rel-mid","NIEDRIG":"rel-low"}.get(relevance,"rel-low")
                        url_html = f'<a href="{url}" target="_blank" class="source-link">🔗 Quelle</a>' if url else ""

                        st.markdown(f"""
                        <div class='result-item'>
                            <div style='display:flex; justify-content:space-between; align-items:center;'>
                                <span class='result-badge {badge_class}'>{rtype}</span>
                                <span class='{rel_class}'>↑ {relevance}</span>
                            </div>
                            <div class='result-title-text'>{title}</div>
                            <div class='result-summary-text'>{summary}</div>
                            <div class='result-meta' style='display:flex; justify-content:space-between;'>
                                <span>📡 {source} · {created_at[:10]}</span>{url_html}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align:center; padding:60px; color:#333; font-size:14px;'>
                    Noch keine Daten · Starte den Live Scout
                </div>
                """, unsafe_allow_html=True)

        # ============================================================
        # KNOWLEDGE BASE
        # ============================================================
        elif "Knowledge" in agent:
            st.markdown("<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:16px;'>📚 Knowledge Base — VIKIphone Wissen</div>", unsafe_allow_html=True)

            tab1, tab2 = st.tabs(["📄 Dokument hochladen", "🎥 YouTube Video laden"])

            with tab1:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>📄 VIKIphone Dokument hinzufügen</div>
                """, unsafe_allow_html=True)

                doc_title = st.text_input("Titel des Dokuments", placeholder="z.B. VIKIphone USPs 2026")
                doc_content = st.text_area(
                    "Inhalt (Text einfügen oder aus PDF kopieren)",
                    placeholder="Füge hier den Inhalt ein...",
                    height=200
                )
                doc_type = st.selectbox("Typ", ["PRODUKT", "STRATEGIE", "ZIELGRUPPE", "WETTBEWERB", "SONSTIGES"])

                if st.button("📄 Dokument speichern", use_container_width=True):
                    if doc_title and doc_content:
                        save_kb_item(doc_type, doc_title, doc_content)
                        st.success(f"✅ '{doc_title}' gespeichert!")
                        st.rerun()
                    else:
                        st.error("Titel und Inhalt sind pflicht!")
                st.markdown("</div>", unsafe_allow_html=True)

            with tab2:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🎥 YouTube Marketing-Video laden</div>
                    <div style='font-size:13px; color:#555; margin-bottom:16px;'>
                        Füge YouTube URLs von Marketing-Experten ein.<br>
                        Claude extrahiert die Marketing-Strategien automatisch.
                    </div>
                """, unsafe_allow_html=True)

                yt_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
                yt_title = st.text_input("Video Titel (optional)", placeholder="z.B. Alex Hormozi — Offer Building")

                st.markdown("""
                <div style='font-size:12px; color:#444; margin-bottom:12px;'>
                💡 Empfohlen: Alex Hormozi, Gary Vaynerchuk, Neil Patel, Marketing-Experten
                </div>
                """, unsafe_allow_html=True)

                if st.button("🎥 Video analysieren & laden", use_container_width=True):
                    if yt_url:
                        anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", "")
                        with st.spinner("Analysiere Video..."):
                            content, error = get_youtube_transcript(yt_url, anthropic_key)
                            if content:
                                title = yt_title or f"YouTube: {yt_url[:50]}"
                                save_kb_item("YOUTUBE_STRATEGIE", title, content, yt_url)
                                st.success(f"✅ Video analysiert & gespeichert!")
                                st.rerun()
                            else:
                                st.error(f"Fehler: {error}")
                    else:
                        st.error("Bitte YouTube URL eingeben!")
                st.markdown("</div>", unsafe_allow_html=True)

            # KB ITEMS ANZEIGEN
            st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:12px;'>Gespeicherte Inhalte ({len(kb_items)})</div>", unsafe_allow_html=True)

            if kb_items:
                for item in kb_items:
                    item_id, type_, title, content, source_url, created_at = item
                    icon_map = {
                        "YOUTUBE_STRATEGIE": "🎥", "PRODUKT": "📦",
                        "STRATEGIE": "🧠", "ZIELGRUPPE": "👥",
                        "WETTBEWERB": "🎯", "SONSTIGES": "📄"
                    }
                    icon = icon_map.get(type_, "📄")

                    col_item, col_del = st.columns([10,1])
                    with col_item:
                        with st.expander(f"{icon} {title} · {type_} · {created_at[:10]}"):
                            st.markdown(f"<div style='font-size:13px; color:#888; line-height:1.6;'>{content[:500]}...</div>", unsafe_allow_html=True)
                            if source_url:
                                st.markdown(f"[🔗 Quelle]({source_url})")
                    with col_del:
                        if st.button("🗑", key=f"del_{item_id}"):
                            delete_kb_item(item_id)
                            st.rerun()
            else:
                st.markdown("""
                <div style='text-align:center; padding:40px; color:#333; font-size:14px;'>
                    Noch keine Inhalte · Lade VIKIphone Docs und YouTube Videos hoch
                </div>
                """, unsafe_allow_html=True)

        # ============================================================
        # GROWTH HACKER
        # ============================================================
        elif "Growth Hacker" in agent:
            st.markdown("<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:8px;'>🧠 Growth Hacker — Kampagnen-Strategie</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px; color:#555; margin-bottom:16px;'>Kombiniert Scout-Daten + Knowledge Base → Konkrete Kampagnen-Strategien</div>", unsafe_allow_html=True)

            if len(kb_items) == 0:
                st.warning("⚠️ Knowledge Base ist leer! Lade zuerst Docs und YouTube Videos hoch.")
            elif count == 0:
                st.warning("⚠️ Keine Scout-Daten! Starte zuerst den Scout.")
            else:
                if st.button("🧠 Kampagnen-Strategien generieren", use_container_width=True):
                    with st.spinner("Growth Hacker analysiert..."):
                        strategies = run_growth_hacker()
                        if strategies:
                            st.session_state.strategies = strategies
                            st.success(f"✅ {len(strategies)} Strategien erstellt!")

                if "strategies" in st.session_state and st.session_state.strategies:
                    for i, strat in enumerate(st.session_state.strategies):
                        st.markdown(f"""
                        <div class='content-card' style='border-left: 3px solid #29B6F6;'>
                            <div style='font-family: Plus Jakarta Sans; font-size:16px; font-weight:700; color:#fff; margin-bottom:12px;'>
                                {i+1}. {strat.get('strategie_name','')}
                            </div>
                            <div style='display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;'>
                                <div>
                                    <div style='font-size:11px; color:#444; margin-bottom:4px;'>METHODE</div>
                                    <div style='font-size:13px; color:#888;'>{strat.get('gelernte_methode','')}</div>
                                </div>
                                <div>
                                    <div style='font-size:11px; color:#444; margin-bottom:4px;'>ZIELGRUPPE</div>
                                    <div style='font-size:13px; color:#888;'>{strat.get('zielgruppe','')}</div>
                                </div>
                            </div>
                            <div style='background:rgba(41,182,246,0.05); border:1px solid rgba(41,182,246,0.1); border-radius:8px; padding:12px; margin-bottom:12px;'>
                                <div style='font-size:11px; color:#444; margin-bottom:4px;'>KERN-BOTSCHAFT</div>
                                <div style='font-size:14px; color:#fff; font-weight:500;'>{strat.get('kern_botschaft','')}</div>
                            </div>
                            <div style='font-size:11px; color:#444; margin-bottom:6px;'>CONTENT IDEEN</div>
                            {"".join([f'<div style="font-size:13px; color:#888; margin-bottom:4px;">→ {idea}</div>' for idea in strat.get('content_ideen',[])])}
                        </div>
                        """, unsafe_allow_html=True)

                        # Direkt Content erstellen
                        platforms = strat.get("plattformen", ["LinkedIn", "Instagram"])
                        selected_platform = st.selectbox(
                            f"Content erstellen für Strategie {i+1}",
                            platforms,
                            key=f"platform_{i}"
                        )
                        if st.button(f"✍️ Content für '{selected_platform}' erstellen", key=f"create_{i}"):
                            with st.spinner("Creator schreibt..."):
                                content = run_creator(strat, selected_platform)
                                if content:
                                    save_content_draft(
                                        selected_platform,
                                        strat.get("strategie_name",""),
                                        content,
                                        strat.get("kern_botschaft","")
                                    )
                                    st.success("✅ Content erstellt — sieh ihn unter 'Creator & Freigabe'!")

        # ============================================================
        # CREATOR & FREIGABE
        # ============================================================
        elif "Creator" in agent:
            st.markdown("<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:8px;'>✍️ Creator & Freigabe</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px; color:#555; margin-bottom:16px;'>Fertige Content-Entwürfe — prüfen, bearbeiten, freigeben</div>", unsafe_allow_html=True)

            drafts = get_content_drafts()
            if drafts:
                pending_drafts = [d for d in drafts if d[5] == "pending"]
                approved_drafts = [d for d in drafts if d[5] == "approved"]

                if pending_drafts:
                    st.markdown(f"""
                    <div class='section-header'>
                        <div class='section-icon' style='background:rgba(255,152,0,0.1);'>⏳</div>
                        <div class='section-title-text'>Warten auf Freigabe</div>
                        <div class='section-count'>{len(pending_drafts)} Entwürfe</div>
                    </div>
                    """, unsafe_allow_html=True)

                    for draft in pending_drafts:
                        draft_id, platform, title, content, strategy, status, created_at = draft
                        platform_icons = {"LinkedIn":"💼","Instagram":"📸","Newsletter":"📧","Blog":"📝"}
                        p_icon = platform_icons.get(platform, "📄")

                        st.markdown(f"""
                        <div class='content-card'>
                            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                                <span class='content-platform'>{p_icon} {platform}</span>
                                <span class='pending-badge'>⏳ Ausstehend</span>
                            </div>
                            <div style='font-size:14px; font-weight:600; color:#fff; margin-bottom:8px;'>{title}</div>
                            <div class='content-text'>{content}</div>
                            <div style='font-size:11px; color:#444; margin-top:10px;'>Strategie: {strategy}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        col_approve, col_delete = st.columns([1,1])
                        with col_approve:
                            if st.button(f"✅ Freigeben", key=f"approve_{draft_id}"):
                                approve_content(draft_id)
                                st.success("✅ Freigegeben!")
                                st.rerun()
                        with col_delete:
                            if st.button(f"🗑 Löschen", key=f"delete_{draft_id}"):
                                delete_content(draft_id)
                                st.rerun()

                if approved_drafts:
                    st.markdown(f"""
                    <div class='section-header' style='margin-top:24px;'>
                        <div class='section-icon' style='background:rgba(76,175,80,0.1);'>✅</div>
                        <div class='section-title-text'>Freigegeben</div>
                        <div class='section-count'>{len(approved_drafts)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    for draft in approved_drafts:
                        draft_id, platform, title, content, strategy, status, created_at = draft
                        st.markdown(f"""
                        <div class='content-card' style='opacity:0.7;'>
                            <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                                <span style='font-size:13px; font-weight:600; color:#fff;'>{title} · {platform}</span>
                                <span class='approve-badge'>✅ Freigegeben</span>
                            </div>
                            <div class='content-text' style='font-size:12px;'>{content[:200]}...</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align:center; padding:60px; color:#333; font-size:14px;'>
                    Noch keine Entwürfe · Starte den Growth Hacker um Content zu erstellen
                </div>
                """, unsafe_allow_html=True)

        # COMING SOON AGENTS
        else:
            labels = {
                "Nischen-Spezialist": ("🏥", "Erstellt branchenspezifischen Content für Arztpraxen, Handwerker und Kanzleien"),
                "SEO-Architekt": ("🔍", "Keyword-Research und SEO-optimierte Artikel für organischen Traffic"),
            }
            for key, (icon, desc) in labels.items():
                if key in agent:
                    st.markdown(f"""
                    <div class='coming-soon'>
                        <div style='font-size:40px; margin-bottom:16px;'>{icon}</div>
                        <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>{key}</div>
                        <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>{desc}</div>
                        <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 2</span>
                    </div>
                    """, unsafe_allow_html=True)

    # ANDERE MODULE
    elif "Vertrieb" in seite:
        st.markdown("<div class='page-header'>Vertrieb</div><div class='page-sub'>Lead Management & Demo-Buchungen</div>", unsafe_allow_html=True)
        for n,d in [("🎯 Demo-Hunter","Findet und kontaktiert potenzielle VIKIphone Kunden"),("📬 Lead-Hunter","Personalisierte Outreach E-Mails")]:
            st.markdown(f"""<div class='coming-soon' style='margin-bottom:12px;'>
                <div style='font-size:32px; margin-bottom:8px;'>{n.split()[0]}</div>
                <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>{n[2:]}</div>
                <div style='font-size:13px; color:#555; margin-bottom:12px;'>{d}</div>
                <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
            </div>""", unsafe_allow_html=True)

    elif "Support" in seite:
        st.markdown("<div class='page-header'>Support</div><div class='page-sub'>E-Mail Assistenz</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'><div style='font-size:32px; margin-bottom:12px;'>🛰</div>
            <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>Ticket-Master</div>
            <div style='font-size:13px; color:#555; margin-bottom:12px;'>IMAP E-Mail Analyse & Antwort-Entwürfe</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 4</span>
        </div>""", unsafe_allow_html=True)

    elif "Backoffice" in seite:
        st.markdown("<div class='page-header'>Backoffice</div><div class='page-sub'>Rechnungen & Finanzdaten</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'><div style='font-size:32px; margin-bottom:12px;'>🗄</div>
            <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>Beleg-Nerd</div>
            <div style='font-size:13px; color:#555; margin-bottom:12px;'>OCR PDF Extraktion → CSV in SQLite</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)

    elif "HR" in seite:
        st.markdown("<div class='page-header'>HR & Recruiting</div><div class='page-sub'>Bewerbermanagement</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'><div style='font-size:32px; margin-bottom:12px;'>👾</div>
            <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:6px;'>CV-Scanner</div>
            <div style='font-size:13px; color:#555; margin-bottom:12px;'>Lebenslauf Matching & Interview-Fragen</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)
