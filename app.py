import streamlit as st
import anthropic
import json
import sqlite3
import os
from datetime import datetime
import urllib.request
import urllib.parse
import re
import base64

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
    box-shadow: 0 0 30px rgba(41,182,246,0.5) !important;
    transform: translateY(-1px) !important;
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

/* File Uploader */
[data-testid="stFileUploader"] {
    background: var(--bg-input) !important;
    border: 1px dashed #333 !important;
    border-radius: 8px !important;
    padding: 8px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--viki-blue) !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }

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
    position: absolute; top: 20px; right: 20px; width: 36px; height: 36px;
    background: var(--viki-blue-glow); border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 16px;
}

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

.result-item {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px 20px; margin-bottom: 8px; transition: all 0.2s;
}
.result-item:hover { border-color: #2a2a2a; background: var(--bg-card-hover); }
.result-badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
}
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

.alarm-card {
    background: rgba(255,152,0,0.05); border: 1px solid rgba(255,152,0,0.3);
    border-left: 3px solid #FF9800; border-radius: 12px; padding: 16px 20px; margin-bottom: 8px;
}
.alarm-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; font-weight: 700; color: #FF9800; }

/* KB Items */
.kb-item {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px 20px; margin-bottom: 8px;
}
.kb-badge {
    display: inline-block; padding: 2px 8px; border-radius: 20px;
    font-size: 10px; font-weight: 600; text-transform: uppercase;
    margin-bottom: 8px;
}
.kb-youtube { background: rgba(255,0,0,0.1); color: #ff4444; }
.kb-produkt { background: rgba(41,182,246,0.1); color: #29B6F6; }
.kb-strategie { background: rgba(156,39,176,0.1); color: #9C27B0; }
.kb-internet { background: rgba(0,188,212,0.1); color: #00BCD4; }
.kb-pdf { background: rgba(76,175,80,0.1); color: #4CAF50; }
.kb-zielgruppe { background: rgba(255,152,0,0.1); color: #FF9800; }
.kb-wettbewerb { background: rgba(244,67,54,0.1); color: #f44336; }

.kb-weight-bar {
    height: 3px; background: #1e1e1e; border-radius: 2px; margin-top: 8px;
}
.kb-weight-fill {
    height: 3px; border-radius: 2px; background: var(--viki-blue);
}

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

.conflict-warning {
    background: rgba(244,67,54,0.05); border: 1px solid rgba(244,67,54,0.2);
    border-radius: 8px; padding: 10px 14px; margin-top: 8px;
    font-size: 12px; color: #f44336;
}
.confirm-badge {
    display: inline-block; background: rgba(76,175,80,0.1); color: #4CAF50;
    border-radius: 20px; padding: 2px 8px; font-size: 10px; font-weight: 600;
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
        id INTEGER PRIMARY KEY, keywords TEXT, competitors TEXT,
        language TEXT DEFAULT 'de', updated_at TEXT
    )""")
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

    # Knowledge Base mit Gewichtung & Konflikt-Flag
    c.execute("""CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, title TEXT, content TEXT, source_url TEXT,
        weight INTEGER DEFAULT 5,
        has_conflict INTEGER DEFAULT 0,
        conflict_note TEXT,
        created_at TEXT
    )""")
    try: c.execute("ALTER TABLE knowledge_base ADD COLUMN weight INTEGER DEFAULT 5")
    except: pass
    try: c.execute("ALTER TABLE knowledge_base ADD COLUMN has_conflict INTEGER DEFAULT 0")
    except: pass
    try: c.execute("ALTER TABLE knowledge_base ADD COLUMN conflict_note TEXT")
    except: pass

    c.execute("""CREATE TABLE IF NOT EXISTS content_drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT, title TEXT, content TEXT,
        strategy TEXT, status TEXT DEFAULT 'pending', created_at TEXT
    )""")
    c.execute("SELECT COUNT(*) FROM scout_config")
    if c.fetchone()[0] == 0:
        kw = json.dumps(["KI Telefonassistent DACH","Voice AI Deutschland",
            "KI Telefon Arztpraxis","Telefonassistent SaaS",
            "KI Rezeption","verpasste Anrufe Lösung","DSGVO Telefonassistent"])
        comp = json.dumps(["fonio.ai","VITAS Telefonassistent","HalloPetra","heykiki",
            "Parloa","Cognigy","voiceOne","Aaron.ai","Synthflow","smao.ai","Safina AI","RufLab"])
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
            (r.get("type",""), r.get("section","MARKT"), r.get("title",""),
             r.get("source",""), r.get("url",""), r.get("summary",""),
             r.get("relevance","MITTEL"), 1 if r.get("is_alarm") else 0,
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

def save_kb_item(type_, title, content, source_url="", weight=5):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""INSERT INTO knowledge_base
        (type,title,content,source_url,weight,has_conflict,created_at)
        VALUES (?,?,?,?,?,0,?)""",
        (type_, title, content, source_url, weight, datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_kb_items():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""SELECT id,type,title,content,source_url,weight,has_conflict,conflict_note,created_at
        FROM knowledge_base ORDER BY weight DESC, id DESC""")
    rows = c.fetchall(); conn.close()
    return rows

def delete_kb_item(item_id):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("DELETE FROM knowledge_base WHERE id=?", (item_id,))
    conn.commit(); conn.close()

def update_kb_weight(item_id, weight):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("UPDATE knowledge_base SET weight=? WHERE id=?", (weight, item_id))
    conn.commit(); conn.close()

def get_kb_context():
    items = get_kb_items()
    if not items: return ""
    context = "=== VIKIPHONE KNOWLEDGE BASE ===\n\n"
    # Nur Einträge mit Gewicht >= 4
    for item in items:
        if item[5] >= 4:
            context += f"[{item[1]}] {item[2]}\n{item[3][:600]}\n\n"
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
if "strategies" not in st.session_state:
    st.session_state.strategies = []

USERS = {"admin": "admin123"}

# ============================================================
# HELPERS
# ============================================================
def get_api_keys():
    ak = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY",""))
    tk = st.secrets.get("TAVILY_API_KEY", os.environ.get("TAVILY_API_KEY",""))
    return ak, tk

def tavily_search(query, api_key, max_results=5):
    try:
        payload = json.dumps({
            "api_key": api_key, "query": query,
            "search_depth": "basic", "max_results": max_results,
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.tavily.com/search", data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8")).get("results", [])
    except:
        return []

def claude_call(prompt, max_tokens=2000, model="claude-haiku-4-5-20251001"):
    ak, _ = get_api_keys()
    if not ak: return ""
    client = anthropic.Anthropic(api_key=ak)
    try:
        msg = client.messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role":"user","content":prompt}])
        return msg.content[0].text.strip()
    except Exception as e:
        st.error(f"Claude Fehler: {e}"); return ""

def parse_json(text):
    if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
    try: return json.loads(text)
    except: return []

# ============================================================
# PDF EXTRAKTION
# ============================================================
def extract_pdf_text(uploaded_file):
    """Sendet PDF an Claude zur Extraktion"""
    ak, _ = get_api_keys()
    if not ak: return ""
    client = anthropic.Anthropic(api_key=ak)
    try:
        pdf_data = base64.standard_b64encode(uploaded_file.read()).decode("utf-8")
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": "Extrahiere den vollständigen Text aus diesem Dokument. Behalte die Struktur bei. Gib nur den Text zurück, keine Kommentare."
                    }
                ]
            }])
        return msg.content[0].text.strip()
    except Exception as e:
        st.error(f"PDF Fehler: {e}"); return ""

# ============================================================
# WIDERSPRUCHS-CHECKER
# ============================================================
def check_conflict(new_title, new_content, existing_items):
    if not existing_items: return False, ""
    existing_summaries = "\n".join([f"- [{i[1]}] {i[2]}: {i[3][:200]}" for i in existing_items[:10]])
    prompt = f"""Prüfe ob dieser neue Inhalt Widersprüche zu bestehendem Wissen enthält.

NEUER INHALT:
Titel: {new_title}
Inhalt: {new_content[:400]}

BESTEHENDES WISSEN:
{existing_summaries}

Antworte NUR mit JSON:
{{"has_conflict": true/false, "conflict_note": "Kurze Beschreibung des Widerspruchs oder leer"}}"""

    result = claude_call(prompt, max_tokens=200)
    try:
        data = json.loads(result)
        return data.get("has_conflict", False), data.get("conflict_note", "")
    except:
        return False, ""

# ============================================================
# YOUTUBE ANALYSE
# ============================================================
def analyze_youtube_urls(urls_text):
    """Analysiert mehrere YouTube URLs auf einmal"""
    ak, tk = get_api_keys()
    if not ak: return []

    urls = [u.strip() for u in urls_text.strip().split("\n") if u.strip() and "youtube" in u.lower() or "youtu.be" in u.lower()]
    if not urls: return []

    results = []
    progress = st.progress(0)

    for i, url in enumerate(urls):
        video_id = ""
        for p in [r'v=([a-zA-Z0-9_-]{11})', r'youtu\.be/([a-zA-Z0-9_-]{11})']:
            m = re.search(p, url)
            if m: video_id = m.group(1); break

        if not video_id: continue

        # Web-Kontext via Tavily
        search_results = tavily_search(
            f"youtube {video_id} marketing strategy summary", tk, 3)
        context = " ".join([r.get("content","")[:300] for r in search_results])

        prompt = f"""Analysiere dieses YouTube Marketing-Video (ID: {video_id}, URL: {url}).

Web-Kontext: {context[:1500]}

Extrahiere die TOP Marketing-Strategien und Lektionen.
Fokus auf: Frameworks, Methoden, psychologische Prinzipien, konkrete Taktiken.

Format als strukturierte Analyse:
## Hauptthema
## Key Strategien (5-7 Punkte)
## Anwendung für VIKIphone B2B SaaS

Auf Deutsch. Sei konkret und umsetzbar."""

        content = claude_call(prompt, max_tokens=1200)
        if content:
            results.append({"url": url, "content": content, "video_id": video_id})

        progress.progress(int((i+1)/len(urls)*100))

    return results

# ============================================================
# INTERNET MARKETING RECHERCHE
# ============================================================
def research_marketing_strategies():
    """Recherchiert Marketing-Strategien live im Internet"""
    ak, tk = get_api_keys()
    if not ak or not tk: return []

    queries = [
        "best B2B SaaS marketing strategies 2026",
        "voice AI product marketing strategies",
        "B2B SaaS growth hacking techniques 2026",
        "problem agitate solve copywriting framework",
        "B2B cold outreach strategies that work 2026",
        "content marketing for SaaS companies 2026",
    ]

    status = st.empty()
    all_content = []

    for i, query in enumerate(queries):
        status.markdown(f"🌐 Recherchiere: *{query}*")
        results = tavily_search(query, tk, 3)
        for r in results:
            if r.get("content"):
                all_content.append(f"Quelle: {r.get('url','')}\n{r.get('content','')[:400]}")

    status.markdown("🧠 Claude destilliert Marketing-Wissen...")

    combined = "\n\n".join(all_content[:15])
    prompt = f"""Du bist ein Elite Marketing-Stratege.

Destilliere aus diesen echten Web-Quellen die wichtigsten Marketing-Frameworks und Strategien
speziell anwendbar für VIKIphone (B2B KI-Telefon SaaS, DACH-Markt).

WEB-QUELLEN:
{combined[:4000]}

Erstelle eine strukturierte Marketing-Strategie-Bibliothek:

## 1. Copywriting Frameworks
(PAS, AIDA, Hook-Story-Offer etc.)

## 2. B2B Content Strategien
(LinkedIn, Newsletter, Blog etc.)

## 3. Lead Generation Taktiken
(Cold Outreach, Demo-Anfragen etc.)

## 4. Psychologische Trigger
(Social Proof, FOMO, Authority etc.)

## 5. VIKIphone-spezifische Anwendung
(Wie jede Strategie konkret für VIKIphone funktioniert)

Sei sehr konkret mit Beispielen. Auf Deutsch."""

    content = claude_call(prompt, max_tokens=2500)
    status.empty()
    return content

# ============================================================
# SCOUT AGENT
# ============================================================
def run_scout(keywords, competitors, language):
    ak, tk = get_api_keys()
    if not ak: st.error("⚠ ANTHROPIC_API_KEY fehlt!"); return []
    if not tk: st.error("⚠ TAVILY_API_KEY fehlt!"); return []

    status = st.empty()
    progress = st.progress(0)

    status.markdown("🔍 **1/4** Suche live im Web...")
    progress.progress(10)

    raw_data = {}
    searches = [
        ("KI Telefonassistent DACH Markt news 2026", "MARKTTRENDS"),
        ("Voice AI B2B Deutschland aktuell 2026", "MARKTTRENDS"),
        ("KI Telefon Arztpraxis Handwerker 2026", "NISCHEN_CHANCE"),
        ("fonio.ai news update features 2026", "KONKURRENZ_ANALYSE"),
        ("VITAS Telefonassistent news 2026", "KONKURRENZ_ANALYSE"),
        ("HalloPetra heykiki voiceOne news 2026", "KONKURRENZ_ANALYSE"),
        ("Parloa Cognigy enterprise KI Telefon 2026", "KONKURRENZ_ANALYSE"),
        ("fonio.ai VITAS HalloPetra Preis Aktion 2026", "ALARM"),
        ("KI Telefonassistent neue features launch 2026", "ALARM"),
        ("fonio.ai voiceOne bewertung kritik problem 2026", "ALARM"),
    ]

    for i, (query, section) in enumerate(searches):
        results = tavily_search(query, tk, 4)
        raw_data.setdefault(section, [])
        for r in results:
            if r.get("title") and r.get("content"):
                raw_data[section].append({
                    "title": r.get("title",""),
                    "content": r.get("content","")[:400],
                    "url": r.get("url","")
                })
        progress.progress(10 + int((i/len(searches))*45))

    status.markdown("🧠 **2/4** Claude analysiert Marktdaten...")
    progress.progress(60)

    context = ""
    for sec, items in raw_data.items():
        if items:
            context += f"\n=== {sec} ===\n"
            for item in items[:4]:
                context += f"Titel: {item['title']}\nURL: {item['url']}\nInhalt: {item['content']}\n\n"

    prompt = f"""Scout-Agent für VIKIphone (KI-Telefonassistenz SaaS, Rynon).

VIKIphone USPs:
- Zero-Latency (kein Gedenksekunden — einzigartig)
- DSGVO Medical Mode (nur VIKIphone — Arztpraxen)
- 24/7 Festnetz-Rufnummer
- Webhook API CRM-Integration
- 30-Tage DSGVO-Datenlöschung

ECHTE WEB-DATEN:
{context[:4000]}

Erstelle Marktbericht als JSON. Nutze NUR echte Daten.

Sektionen:
- "MARKTTRENDS" → Was bewegt den Markt?
- "KONKURRENZ_ANALYSE" → Was machen Konkurrenten?
- "ALARM" → Dringende Signale (is_alarm: true)
- "NISCHEN_CHANCE" → Chancen in Branchen
- "STRATEGISCHE_CHANCE" → Größere Chancen

Types: TREND, KONKURRENZ, ALARM, FEATURE, BEWERTUNG, FUNDING, CHANCE

[{{"type":"ALARM","section":"ALARM","title":"...","source":"...","url":"...","summary":"2-3 Sätze was passiert + was VIKIphone tun sollte","relevance":"HOCH","is_alarm":true}}]

Mindestens 12 Einträge (3 MARKTTRENDS, 3 KONKURRENZ_ANALYSE, 2 ALARM, 2 NISCHEN_CHANCE, 2 STRATEGISCHE_CHANCE).
NUR JSON."""

    client = anthropic.Anthropic(api_key=ak)
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=4000,
            messages=[{"role":"user","content":prompt}])
        text = msg.content[0].text.strip()
        results = parse_json(text)
        progress.progress(100)
        alarms = sum(1 for r in results if r.get("is_alarm"))
        status.markdown(f"✅ **Fertig!** {len(results)} Erkenntnisse · {alarms} Alarme")
        return results
    except Exception as e:
        st.error(f"Fehler: {e}"); return []

# ============================================================
# GROWTH HACKER
# ============================================================
def run_growth_hacker():
    scout_rows = get_scout_results(20)
    scout_context = "\n".join([f"[{r[0]}] {r[2]}: {r[5]}" for r in scout_rows[:10]])
    kb_context = get_kb_context()

    if not kb_context:
        st.warning("⚠️ Knowledge Base leer! Lade erst Docs & Videos."); return []

    prompt = f"""Du bist der weltbeste B2B SaaS Growth Hacker für VIKIphone.

MARKTDATEN (Scout):
{scout_context}

GELERNTE STRATEGIEN (Knowledge Base):
{kb_context[:3000]}

VIKIphone USPs: Zero-Latency, DSGVO Medical Mode, 24/7, Webhook API

Kombiniere Marktdaten + gelernte Strategien → 3 konkrete Kampagnen.

JSON:
[{{"strategie_name":"...","gelernte_methode":"Welches Framework (z.B. PAS von Hormozi)","markt_trigger":"Welchen Trend nutzt du","zielgruppe":"Exakt wer","kern_botschaft":"Die eine starke Botschaft","plattformen":["LinkedIn"],"content_ideen":["Idee 1","Idee 2","Idee 3"]}}]

NUR JSON."""

    result = claude_call(prompt, max_tokens=2000)
    return parse_json(result)

# ============================================================
# CREATOR
# ============================================================
def run_creator(strategy, platform):
    guides = {
        "LinkedIn": "Professionell, 150-300 Wörter, Hook Zeile 1, 3-5 Absätze, CTA, 3-5 Hashtags",
        "Instagram": "Emotional, 80-150 Wörter, starker Hook, Emojis, CTA, 10 Hashtags",
        "Newsletter": "Persönlich, 200-400 Wörter, Betreff + Text + CTA",
        "Blog": "SEO, 400-600 Wörter Intro, H2 Struktur",
    }
    prompt = f"""Weltbester B2B SaaS Copywriter für VIKIphone.

Strategie: {strategy.get('strategie_name','')}
Methode: {strategy.get('gelernte_methode','')}
Zielgruppe: {strategy.get('zielgruppe','')}
Kern-Botschaft: {strategy.get('kern_botschaft','')}

Platform {platform}: {guides.get(platform,'')}

VIKIphone USPs: Zero-Latency (kein Gedenksekunden), DSGVO Medical Mode, 24/7, Festnetz-Nummer.

Schreibe den FERTIGEN POST — direkt verwendbar. Auf Deutsch. Hook muss sofort grabben."""

    return claude_call(prompt, max_tokens=1000)

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
                <div style='font-size:12px; font-weight:600; color:#FF9800;'>🚨 {alarm_count} Alarm{'e' if alarm_count>1 else ''}</div>
                <div style='font-size:11px; color:#666; margin-top:2px;'>Konkurrenz-Aktivität</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Sign out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # ============================================================
    # MARKETING
    # ============================================================
    if "Marketing" in seite:
        st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:2px;'>
            <div class='page-header'>Marketing Zentrale</div>
            <span class='live-badge'>● LIVE</span>
        </div>
        <div class='page-sub'>VIKIphone Growth · KI-gesteuerte Echtzeit-Marktanalyse & Content-Pipeline</div>
        """, unsafe_allow_html=True)

        count = get_scout_count()
        alarms = get_alarm_count()
        kw, comp, lang = get_scout_config()
        kb_items = get_kb_items()
        drafts = get_content_drafts()
        pending = sum(1 for d in drafts if d[5] == "pending")

        c1,c2,c3,c4,c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon'>📡</div>
                <div class='metric-number'>{count}</div><div class='metric-label'>Scout Ergebnisse</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card' style='{"border-color:rgba(255,152,0,0.4);" if alarms>0 else ""}'>
                <div class='metric-icon' style='background:rgba(255,152,0,0.1);'>🚨</div>
                <div class='metric-number' style='color:{"#FF9800" if alarms>0 else "white"}'>{alarms}</div>
                <div class='metric-label'>Alarme</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon' style='background:rgba(156,39,176,0.1);'>🧠</div>
                <div class='metric-number'>{len(kb_items)}</div><div class='metric-label'>Knowledge Base</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon' style='background:rgba(76,175,80,0.1);'>✍️</div>
                <div class='metric-number'>{pending}</div><div class='metric-label'>Entwürfe ausstehend</div></div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon'>🎯</div>
                <div class='metric-number'>{len(comp)}</div><div class='metric-label'>Konkurrenten</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        agent = st.radio("Agent", [
            "🔭 Scout", "📚 Knowledge Base", "🧠 Growth Hacker",
            "✍️ Creator & Freigabe", "🏥 Nischen-Spezialist", "🔍 SEO-Architekt"
        ], horizontal=True, label_visibility="collapsed")

        st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)

        # ============================================================
        # SCOUT
        # ============================================================
        if "Scout" in agent:
            col_left, col_right = st.columns([2,1])
            with col_left:
                st.markdown("""<div class='config-section'><div class='config-label'>⚙️ Keywords</div>""", unsafe_allow_html=True)
                kw_text = st.text_area("Keywords", value="\n".join(kw), height=140, label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("""<div class='config-section'><div class='config-label'>🎯 Konkurrenten</div>""", unsafe_allow_html=True)
                comp_text = st.text_area("Konkurrenten", value="\n".join(comp), height=140, label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)
                lang_sel = st.selectbox("Sprache", ["de","en"], index=0 if lang=="de" else 1)
                if st.button("💾 Speichern", use_container_width=True):
                    save_scout_config(
                        [k.strip() for k in kw_text.split("\n") if k.strip()],
                        [c.strip() for c in comp_text.split("\n") if c.strip()], lang_sel)
                    st.success("✅ Gespeichert!")

            with col_right:
                st.markdown("""<div class='config-section'><div class='config-label'>🔭 Live Scout</div>
                    <div style='font-size:13px; color:#555; margin-bottom:16px; line-height:1.8;'>
                        <span class='live-badge'>● Echtzeit Web-Suche</span><br><br>
                        <span style='color:#29B6F6'>①</span> Tavily sucht 10x live<br>
                        <span style='color:#29B6F6'>②</span> Markt + Konkurrenz + Alarme<br>
                        <span style='color:#29B6F6'>③</span> Claude analysiert & bewertet<br>
                        <span style='color:#FF9800'>④</span> 🚨 Alarm bei kritischen Signalen
                    </div>""", unsafe_allow_html=True)
                if st.button("▶ Jetzt live scannen", use_container_width=True):
                    results = run_scout(
                        [k.strip() for k in kw_text.split("\n") if k.strip()],
                        [c.strip() for c in comp_text.split("\n") if c.strip()], lang_sel)
                    if results:
                        save_scout_results(results)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown(f"""<div class='config-section'><div class='config-label'>📊 Status</div>
                    <div style='font-size:13px; color:#555;'>
                        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'><span>Ergebnisse</span><span style='color:#fff; font-weight:600;'>{count}</span></div>
                        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'><span>🚨 Alarme</span><span style='color:#FF9800; font-weight:600;'>{alarms}</span></div>
                        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'><span>Keywords</span><span style='color:#29B6F6; font-weight:600;'>{len(kw)}</span></div>
                        <div style='display:flex; justify-content:space-between;'><span>Konkurrenten</span><span style='color:#29B6F6; font-weight:600;'>{len(comp)}</span></div>
                    </div></div>""", unsafe_allow_html=True)

            # ERGEBNISSE IN SEKTIONEN
            st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)
            rows = get_scout_results(50)
            if rows:
                alarm_rows = [r for r in rows if r[7]==1]
                if alarm_rows:
                    st.markdown("""<div class='section-header'>
                        <div class='section-icon' style='background:rgba(255,152,0,0.1);'>🚨</div>
                        <div class='section-title-text'>Alarme — Sofortige Aufmerksamkeit</div>
                    </div>""", unsafe_allow_html=True)
                    for row in alarm_rows:
                        rtype,section,title,source,url,summary,relevance,is_alarm,created_at = row
                        url_html = f'<a href="{url}" target="_blank" class="source-link">🔗 Quelle</a>' if url else ""
                        st.markdown(f"""<div class='alarm-card'>
                            <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                                <span class='result-badge badge-alarm'>🚨 {rtype}</span>
                                <span class='rel-high'>↑ HOCH</span>
                            </div>
                            <div class='alarm-title'>{title}</div>
                            <div class='result-summary-text' style='margin-top:6px;'>{summary}</div>
                            <div class='result-meta' style='display:flex; justify-content:space-between;'>
                                <span>📡 {source} · {created_at[:10]}</span>{url_html}
                            </div></div>""", unsafe_allow_html=True)

                sections_config = {
                    "MARKTTRENDS": ("📈","Markttrends","rgba(41,182,246,0.1)"),
                    "KONKURRENZ_ANALYSE": ("🎯","Konkurrenz-Analyse","rgba(244,67,54,0.1)"),
                    "NISCHEN_CHANCE": ("🏥","Nischen-Chancen","rgba(76,175,80,0.1)"),
                    "STRATEGISCHE_CHANCE": ("💡","Strategische Chancen","rgba(156,39,176,0.1)"),
                }
                badge_map = {"TREND":"badge-trend","KONKURRENZ":"badge-konkurrenz","CHANCE":"badge-chance",
                             "FEATURE":"badge-feature","BEWERTUNG":"badge-bewertung","FUNDING":"badge-funding","ALARM":"badge-alarm"}
                rel_map = {"HOCH":"rel-high","MITTEL":"rel-mid","NIEDRIG":"rel-low"}

                for sec_key, (icon,sec_label,bg) in sections_config.items():
                    sec_rows = [r for r in rows if r[1]==sec_key and r[7]==0]
                    if not sec_rows: continue
                    st.markdown(f"""<div class='section-header' style='margin-top:20px;'>
                        <div class='section-icon' style='background:{bg};'>{icon}</div>
                        <div class='section-title-text'>{sec_label}</div>
                        <div class='section-count'>{len(sec_rows)} Einträge</div>
                    </div>""", unsafe_allow_html=True)
                    for row in sec_rows:
                        rtype,section,title,source,url,summary,relevance,is_alarm,created_at = row
                        bc = badge_map.get(rtype,"badge-trend")
                        rc = rel_map.get(relevance,"rel-low")
                        url_html = f'<a href="{url}" target="_blank" class="source-link">🔗 Quelle</a>' if url else ""
                        st.markdown(f"""<div class='result-item'>
                            <div style='display:flex; justify-content:space-between; align-items:center;'>
                                <span class='result-badge {bc}'>{rtype}</span>
                                <span class='{rc}'>↑ {relevance}</span>
                            </div>
                            <div class='result-title-text'>{title}</div>
                            <div class='result-summary-text'>{summary}</div>
                            <div class='result-meta' style='display:flex; justify-content:space-between;'>
                                <span>📡 {source} · {created_at[:10]}</span>{url_html}
                            </div></div>""", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align:center; padding:60px; color:#333; font-size:14px;'>Noch keine Daten · Starte den Live Scout</div>", unsafe_allow_html=True)

        # ============================================================
        # KNOWLEDGE BASE
        # ============================================================
        elif "Knowledge" in agent:
            st.markdown("<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:16px;'>📚 Knowledge Base — VIKIphone Wissen</div>", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["📄 Dokument / PDF", "🎥 YouTube Videos", "🌐 Internet Recherche"])

            # TAB 1: DOKUMENT / PDF
            with tab1:
                st.markdown("<div class='config-section'><div class='config-label'>📄 Dokument oder PDF hochladen</div>", unsafe_allow_html=True)

                upload_mode = st.radio("Modus", ["📎 PDF hochladen", "✏️ Text einfügen"], horizontal=True)

                if "PDF" in upload_mode:
                    uploaded_files = st.file_uploader(
                        "PDF Dateien hochladen (mehrere möglich)",
                        type=["pdf"],
                        accept_multiple_files=True
                    )
                    doc_type = st.selectbox("Typ", ["PRODUKT","STRATEGIE","ZIELGRUPPE","WETTBEWERB","SONSTIGES"])

                    if st.button("📎 PDFs analysieren & speichern", use_container_width=True):
                        if uploaded_files:
                            existing = get_kb_items()
                            for uploaded_file in uploaded_files:
                                with st.spinner(f"Lese {uploaded_file.name}..."):
                                    content = extract_pdf_text(uploaded_file)
                                    if content:
                                        has_conflict, conflict_note = check_conflict(
                                            uploaded_file.name, content, existing)
                                        save_kb_item(doc_type, uploaded_file.name, content, "", 5)
                                        if has_conflict:
                                            st.warning(f"⚠️ {uploaded_file.name}: Möglicher Widerspruch — {conflict_note}")
                                        else:
                                            st.success(f"✅ {uploaded_file.name} gespeichert!")
                            st.rerun()
                        else:
                            st.error("Bitte PDF auswählen!")
                else:
                    doc_title = st.text_input("Titel", placeholder="z.B. VIKIphone USPs 2026")
                    doc_content = st.text_area("Inhalt", placeholder="Text hier einfügen...", height=180)
                    doc_type2 = st.selectbox("Typ ", ["PRODUKT","STRATEGIE","ZIELGRUPPE","WETTBEWERB","SONSTIGES"])

                    if st.button("💾 Speichern", use_container_width=True):
                        if doc_title and doc_content:
                            existing = get_kb_items()
                            has_conflict, conflict_note = check_conflict(doc_title, doc_content, existing)
                            save_kb_item(doc_type2, doc_title, doc_content, "", 5)
                            if has_conflict:
                                st.warning(f"⚠️ Möglicher Widerspruch: {conflict_note}")
                            else:
                                st.success("✅ Gespeichert!")
                            st.rerun()
                        else:
                            st.error("Titel und Inhalt pflicht!")
                st.markdown("</div>", unsafe_allow_html=True)

            # TAB 2: YOUTUBE
            with tab2:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🎥 Mehrere YouTube Videos auf einmal laden</div>
                    <div style='font-size:13px; color:#555; margin-bottom:12px; line-height:1.6;'>
                        Eine URL pro Zeile. Claude analysiert alle Videos und extrahiert Marketing-Strategien.<br>
                        <span style='color:#444;'>💡 Empfohlen: Alex Hormozi, Gary Vee, Neil Patel, Lenny Rachitsky</span>
                    </div>""", unsafe_allow_html=True)

                yt_urls = st.text_area(
                    "YouTube URLs (eine pro Zeile)",
                    placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/watch?v=...",
                    height=120,
                    label_visibility="collapsed"
                )

                st.markdown("""
                <div style='font-size:12px; color:#333; margin-bottom:12px;'>
                🔴 Empfohlene Kanäle für VIKIphone B2B Marketing:<br>
                • Alex Hormozi — $100M Offers, Lead Gen<br>
                • Gary Vaynerchuk — Social Media B2B<br>
                • Neil Patel — SEO & Content Marketing<br>
                • Lenny Rachitsky — SaaS Growth Strategies<br>
                • Justin Welsh — LinkedIn B2B Content
                </div>
                """, unsafe_allow_html=True)

                if st.button("🎥 Alle Videos analysieren", use_container_width=True):
                    if yt_urls.strip():
                        existing = get_kb_items()
                        results = analyze_youtube_urls(yt_urls)
                        for r in results:
                            has_conflict, conflict_note = check_conflict(
                                f"YouTube: {r['url']}", r['content'], existing)
                            save_kb_item("YOUTUBE_STRATEGIE", f"YouTube: {r['video_id']}", r['content'], r['url'], 7)
                            if has_conflict:
                                st.warning(f"⚠️ Widerspruch erkannt: {conflict_note}")
                        if results:
                            st.success(f"✅ {len(results)} Videos analysiert & gespeichert!")
                            st.rerun()
                        else:
                            st.error("Keine gültigen YouTube URLs gefunden!")
                    else:
                        st.error("Bitte URLs eingeben!")
                st.markdown("</div>", unsafe_allow_html=True)

            # TAB 3: INTERNET RECHERCHE
            with tab3:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🌐 Automatische Internet-Recherche</div>
                    <div style='font-size:13px; color:#555; margin-bottom:16px; line-height:1.6;'>
                        Tavily durchsucht das Internet nach den besten B2B SaaS Marketing-Strategien.<br>
                        Claude destilliert das Wissen speziell für VIKIphone.
                    </div>
                    <div style='font-size:12px; color:#333; margin-bottom:16px;'>
                    Sucht nach:<br>
                    • Best B2B SaaS marketing strategies 2026<br>
                    • Voice AI product marketing<br>
                    • B2B growth hacking techniques<br>
                    • Copywriting frameworks (PAS, AIDA, Hook-Story-Offer)<br>
                    • Cold outreach strategies<br>
                    • Content marketing für SaaS
                    </div>""", unsafe_allow_html=True)

                if st.button("🌐 Internet nach Strategien durchsuchen", use_container_width=True):
                    with st.spinner("Recherchiere Marketing-Strategien..."):
                        content = research_marketing_strategies()
                        if content:
                            existing = get_kb_items()
                            has_conflict, conflict_note = check_conflict(
                                "Internet Marketing Strategien", content, existing)
                            save_kb_item(
                                "INTERNET_RECHERCHE",
                                f"Marketing Strategien — {datetime.now().strftime('%d.%m.%Y')}",
                                content, "", 8)
                            if has_conflict:
                                st.warning(f"⚠️ Widerspruch: {conflict_note}")
                            st.success("✅ Strategien gespeichert!")
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # KB ITEMS ANZEIGEN
            st.markdown("<div class='viki-divider'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:12px;'>Gespeicherte Inhalte ({len(kb_items)})</div>", unsafe_allow_html=True)

            if kb_items:
                icon_map = {"YOUTUBE_STRATEGIE":"🎥","PRODUKT":"📦","STRATEGIE":"🧠",
                            "ZIELGRUPPE":"👥","WETTBEWERB":"🎯","INTERNET_RECHERCHE":"🌐",
                            "PDF":"📄","SONSTIGES":"📄"}
                badge_map_kb = {"YOUTUBE_STRATEGIE":"kb-youtube","PRODUKT":"kb-produkt",
                                "STRATEGIE":"kb-strategie","INTERNET_RECHERCHE":"kb-internet",
                                "PDF":"kb-pdf","ZIELGRUPPE":"kb-zielgruppe","WETTBEWERB":"kb-wettbewerb"}

                for item in kb_items:
                    item_id,type_,title,content,source_url,weight,has_conflict,conflict_note,created_at = item
                    icon = icon_map.get(type_,"📄")
                    bc = badge_map_kb.get(type_,"kb-produkt")
                    weight_pct = int((weight/10)*100)

                    col_item, col_del = st.columns([10,1])
                    with col_item:
                        conflict_html = f'<div class="conflict-warning">⚠️ Möglicher Widerspruch: {conflict_note}</div>' if has_conflict else ""
                        with st.expander(f"{icon} {title} · Gewicht: {weight}/10 · {created_at[:10]}"):
                            st.markdown(f"""
                            <span class='kb-badge {bc}'>{type_}</span>
                            {conflict_html}
                            <div class='kb-weight-bar'><div class='kb-weight-fill' style='width:{weight_pct}%;'></div></div>
                            <div style='font-size:11px; color:#444; margin-bottom:8px;'>Gewichtung: {weight}/10</div>
                            <div style='font-size:13px; color:#888; line-height:1.6;'>{content[:600]}...</div>
                            """, unsafe_allow_html=True)
                            if source_url:
                                st.markdown(f"[🔗 Quelle]({source_url})")
                            new_weight = st.slider("Gewichtung anpassen", 1, 10, weight, key=f"w_{item_id}")
                            if new_weight != weight:
                                update_kb_weight(item_id, new_weight)
                                st.rerun()
                    with col_del:
                        if st.button("🗑", key=f"del_{item_id}"):
                            delete_kb_item(item_id)
                            st.rerun()
            else:
                st.markdown("<div style='text-align:center; padding:40px; color:#333; font-size:14px;'>Noch leer · Lade Docs, Videos oder starte Internet-Recherche</div>", unsafe_allow_html=True)

        # ============================================================
        # GROWTH HACKER
        # ============================================================
        elif "Growth Hacker" in agent:
            st.markdown("<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:4px;'>🧠 Growth Hacker</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px; color:#555; margin-bottom:16px;'>Scout-Daten + Knowledge Base → Konkrete Kampagnen-Strategien</div>", unsafe_allow_html=True)

            if len(kb_items) == 0:
                st.warning("⚠️ Knowledge Base leer! Lade erst Docs & Videos.")
            elif count == 0:
                st.warning("⚠️ Keine Scout-Daten! Starte zuerst den Scout.")
            else:
                if st.button("🧠 Kampagnen-Strategien generieren", use_container_width=True):
                    with st.spinner("Growth Hacker analysiert..."):
                        st.session_state.strategies = run_growth_hacker()

                if st.session_state.strategies:
                    for i, strat in enumerate(st.session_state.strategies):
                        st.markdown(f"""<div class='content-card' style='border-left:3px solid #29B6F6;'>
                            <div style='font-family: Plus Jakarta Sans; font-size:16px; font-weight:700; color:#fff; margin-bottom:12px;'>
                                {i+1}. {strat.get('strategie_name','')}
                            </div>
                            <div style='display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;'>
                                <div><div style='font-size:11px; color:#444; margin-bottom:4px;'>METHODE</div>
                                    <div style='font-size:13px; color:#888;'>{strat.get('gelernte_methode','')}</div></div>
                                <div><div style='font-size:11px; color:#444; margin-bottom:4px;'>ZIELGRUPPE</div>
                                    <div style='font-size:13px; color:#888;'>{strat.get('zielgruppe','')}</div></div>
                            </div>
                            <div style='background:rgba(41,182,246,0.05); border:1px solid rgba(41,182,246,0.1); border-radius:8px; padding:12px; margin-bottom:12px;'>
                                <div style='font-size:11px; color:#444; margin-bottom:4px;'>KERN-BOTSCHAFT</div>
                                <div style='font-size:14px; color:#fff; font-weight:500;'>{strat.get('kern_botschaft','')}</div>
                            </div>
                            <div style='font-size:11px; color:#444; margin-bottom:6px;'>CONTENT IDEEN</div>
                            {"".join([f'<div style="font-size:13px; color:#888; margin-bottom:4px;">→ {idea}</div>' for idea in strat.get('content_ideen',[])])}
                        </div>""", unsafe_allow_html=True)

                        platforms = strat.get("plattformen", ["LinkedIn","Instagram"])
                        sel_platform = st.selectbox(f"Platform für Strategie {i+1}", platforms, key=f"p_{i}")
                        if st.button(f"✍️ Content für {sel_platform} erstellen", key=f"c_{i}"):
                            with st.spinner("Creator schreibt..."):
                                content = run_creator(strat, sel_platform)
                                if content:
                                    save_content_draft(sel_platform, strat.get("strategie_name",""), content, strat.get("kern_botschaft",""))
                                    st.success("✅ Content erstellt → Creator & Freigabe")

        # ============================================================
        # CREATOR & FREIGABE
        # ============================================================
        elif "Creator" in agent:
            st.markdown("<div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:4px;'>✍️ Creator & Freigabe</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px; color:#555; margin-bottom:16px;'>Content-Entwürfe prüfen, bearbeiten und freigeben</div>", unsafe_allow_html=True)

            drafts = get_content_drafts()
            pending_d = [d for d in drafts if d[5]=="pending"]
            approved_d = [d for d in drafts if d[5]=="approved"]

            if pending_d:
                st.markdown(f"""<div class='section-header'>
                    <div class='section-icon' style='background:rgba(255,152,0,0.1);'>⏳</div>
                    <div class='section-title-text'>Warten auf Freigabe</div>
                    <div class='section-count'>{len(pending_d)} Entwürfe</div>
                </div>""", unsafe_allow_html=True)
                p_icons = {"LinkedIn":"💼","Instagram":"📸","Newsletter":"📧","Blog":"📝"}
                for draft in pending_d:
                    did,platform,title,content,strategy,status,created_at = draft
                    st.markdown(f"""<div class='content-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                            <span class='content-platform'>{p_icons.get(platform,'📄')} {platform}</span>
                            <span class='pending-badge'>⏳ Ausstehend</span>
                        </div>
                        <div style='font-size:14px; font-weight:600; color:#fff; margin-bottom:8px;'>{title}</div>
                        <div class='content-text'>{content}</div>
                        <div style='font-size:11px; color:#444; margin-top:10px;'>Strategie: {strategy}</div>
                    </div>""", unsafe_allow_html=True)
                    ca, cd = st.columns([1,1])
                    with ca:
                        if st.button("✅ Freigeben", key=f"ap_{did}"):
                            approve_content(did); st.rerun()
                    with cd:
                        if st.button("🗑 Löschen", key=f"dl_{did}"):
                            delete_content(did); st.rerun()

            if approved_d:
                st.markdown(f"""<div class='section-header' style='margin-top:24px;'>
                    <div class='section-icon' style='background:rgba(76,175,80,0.1);'>✅</div>
                    <div class='section-title-text'>Freigegeben</div>
                    <div class='section-count'>{len(approved_d)}</div>
                </div>""", unsafe_allow_html=True)
                for draft in approved_d:
                    did,platform,title,content,strategy,status,created_at = draft
                    st.markdown(f"""<div class='content-card' style='opacity:0.7;'>
                        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                            <span style='font-size:13px; font-weight:600; color:#fff;'>{title} · {platform}</span>
                            <span class='approve-badge'>✅ Freigegeben</span>
                        </div>
                        <div class='content-text' style='font-size:12px;'>{content[:200]}...</div>
                    </div>""", unsafe_allow_html=True)

            if not drafts:
                st.markdown("<div style='text-align:center; padding:60px; color:#333; font-size:14px;'>Noch keine Entwürfe · Starte den Growth Hacker</div>", unsafe_allow_html=True)

        else:
            labels = {
                "Nischen-Spezialist": ("🏥", "Content für Arztpraxen, Handwerker, Kanzleien"),
                "SEO-Architekt": ("🔍", "Keyword-Research & SEO-optimierte Artikel"),
            }
            for key, (icon, desc) in labels.items():
                if key in agent:
                    st.markdown(f"""<div class='coming-soon'>
                        <div style='font-size:40px; margin-bottom:16px;'>{icon}</div>
                        <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>{key}</div>
                        <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>{desc}</div>
                        <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 2</span>
                    </div>""", unsafe_allow_html=True)

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
