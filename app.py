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
    page_icon="🎯",
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
.stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label {
    color: var(--text-secondary) !important; font-family: 'Inter', sans-serif !important;
    font-size: 12px !important; font-weight: 500 !important;
    text-transform: none !important; letter-spacing: 0 !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--viki-blue); }

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

.lead-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px; margin-bottom: 12px; transition: all 0.2s;
}
.lead-card:hover { border-color: #2a2a2a; background: var(--bg-card-hover); }
.lead-card-approved { border-color: rgba(76,175,80,0.3) !important; }
.lead-card-rejected { opacity: 0.4; }

.score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 40px; height: 40px; border-radius: 10px; font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 16px; font-weight: 800; flex-shrink: 0;
}
.score-high { background: rgba(76,175,80,0.15); color: #4CAF50; border: 1px solid rgba(76,175,80,0.3); }
.score-mid { background: rgba(255,152,0,0.15); color: #FF9800; border: 1px solid rgba(255,152,0,0.3); }
.score-low { background: rgba(244,67,54,0.15); color: #f44336; border: 1px solid rgba(244,67,54,0.3); }

.branche-badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
}
.badge-arzt { background: rgba(41,182,246,0.1); color: #29B6F6; }
.badge-zahnarzt { background: rgba(156,39,176,0.1); color: #9C27B0; }
.badge-handwerk { background: rgba(255,152,0,0.1); color: #FF9800; }
.badge-kanzlei { background: rgba(0,188,212,0.1); color: #00BCD4; }
.badge-physio { background: rgba(76,175,80,0.1); color: #4CAF50; }
.badge-sonstige { background: rgba(255,255,255,0.05); color: #888; }

.email-preview {
    background: #0a0a0a; border: 1px solid #1e1e1e; border-radius: 8px;
    padding: 16px; margin-top: 12px; font-size: 13px; color: #888;
    line-height: 1.7; white-space: pre-wrap; font-family: 'Inter', sans-serif;
}
.email-subject {
    font-size: 13px; font-weight: 600; color: var(--viki-blue);
    margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #1e1e1e;
}

.config-section {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 20px; margin-bottom: 12px;
}
.config-label {
    font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px;
}

.page-header {
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px;
    font-weight: 700; color: var(--text-primary); margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: var(--text-secondary); margin-bottom: 24px; }
.viki-divider { height: 1px; background: var(--border); margin: 20px 0; }

.section-header {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 0; margin-bottom: 12px; border-bottom: 1px solid var(--border);
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

.live-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.3);
    color: #4CAF50; border-radius: 20px; padding: 3px 10px;
    font-size: 11px; font-weight: 600;
}
.pending-badge {
    display: inline-flex; align-items: center;
    background: rgba(255,152,0,0.1); border: 1px solid rgba(255,152,0,0.3);
    color: #FF9800; border-radius: 20px; padding: 3px 10px;
    font-size: 11px; font-weight: 600;
}
.approved-badge {
    display: inline-flex; align-items: center;
    background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.3);
    color: #4CAF50; border-radius: 20px; padding: 3px 10px;
    font-size: 11px; font-weight: 600;
}
.rejected-badge {
    display: inline-flex; align-items: center;
    background: rgba(244,67,54,0.1); border: 1px solid rgba(244,67,54,0.3);
    color: #f44336; border-radius: 20px; padding: 3px 10px;
    font-size: 11px; font-weight: 600;
}

.coming-soon {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 40px; text-align: center;
}

.info-row {
    display: flex; align-items: center; gap: 8px;
    font-size: 13px; color: var(--text-secondary); margin-bottom: 6px;
}
.info-label {
    font-size: 11px; color: var(--text-muted); text-transform: uppercase;
    letter-spacing: 0.5px; font-weight: 600; min-width: 80px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================
def init_db():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()

    # Demo-Hunter Config
    c.execute("""CREATE TABLE IF NOT EXISTS demo_config (
        id INTEGER PRIMARY KEY,
        branchen TEXT,
        regionen TEXT,
        min_score INTEGER DEFAULT 7,
        email_stil TEXT DEFAULT 'professionell',
        daily_limit INTEGER DEFAULT 10,
        absender_name TEXT DEFAULT 'Vikiphone Team',
        absender_email TEXT DEFAULT '',
        updated_at TEXT
    )""")

    # Leads
    c.execute("""CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firmenname TEXT,
        branche TEXT,
        ort TEXT,
        region TEXT,
        website TEXT,
        telefon TEXT,
        email TEXT,
        bewertungen_anzahl INTEGER DEFAULT 0,
        bewertungen_score REAL DEFAULT 0,
        erreichbarkeit_problem INTEGER DEFAULT 0,
        mitarbeiter_schaetzung TEXT,
        score INTEGER DEFAULT 0,
        score_begruendung TEXT,
        email_betreff TEXT,
        email_text TEXT,
        status TEXT DEFAULT 'pending',
        notiz TEXT,
        created_at TEXT
    )""")

    # Default Config
    c.execute("SELECT COUNT(*) FROM demo_config")
    if c.fetchone()[0] == 0:
        branchen = json.dumps(["Arztpraxis","Zahnarztpraxis","Handwerksbetrieb","Anwaltskanzlei","Physiotherapie"])
        regionen = json.dumps(["München","Hamburg","Berlin","Frankfurt","Köln","Stuttgart","Düsseldorf","Wien","Zürich"])
        c.execute("""INSERT INTO demo_config
            (branchen,regionen,min_score,email_stil,daily_limit,absender_name,absender_email,updated_at)
            VALUES (?,?,7,'professionell',10,'VIKIphone Team','',?)""",
            (branchen, regionen, datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_demo_config():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT branchen,regionen,min_score,email_stil,daily_limit,absender_name,absender_email FROM demo_config WHERE id=1")
    row = c.fetchone(); conn.close()
    if row:
        return {
            "branchen": json.loads(row[0]),
            "regionen": json.loads(row[1]),
            "min_score": row[2],
            "email_stil": row[3],
            "daily_limit": row[4],
            "absender_name": row[5],
            "absender_email": row[6]
        }
    return {}

def save_demo_config(branchen, regionen, min_score, email_stil, daily_limit, absender_name, absender_email):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""UPDATE demo_config SET
        branchen=?,regionen=?,min_score=?,email_stil=?,
        daily_limit=?,absender_name=?,absender_email=?,updated_at=? WHERE id=1""",
        (json.dumps(branchen), json.dumps(regionen), min_score,
         email_stil, daily_limit, absender_name, absender_email,
         datetime.now().isoformat()))
    conn.commit(); conn.close()

def save_lead(lead):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    # Duplikat-Check
    c.execute("SELECT id FROM leads WHERE firmenname=? AND ort=?",
              (lead.get("firmenname",""), lead.get("ort","")))
    if c.fetchone():
        conn.close(); return False
    c.execute("""INSERT INTO leads
        (firmenname,branche,ort,region,website,telefon,email,
         bewertungen_anzahl,bewertungen_score,erreichbarkeit_problem,
         mitarbeiter_schaetzung,score,score_begruendung,
         email_betreff,email_text,status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'pending',?)""",
        (lead.get("firmenname",""), lead.get("branche",""),
         lead.get("ort",""), lead.get("region",""),
         lead.get("website",""), lead.get("telefon",""),
         lead.get("email",""), lead.get("bewertungen_anzahl",0),
         lead.get("bewertungen_score",0), lead.get("erreichbarkeit_problem",0),
         lead.get("mitarbeiter_schaetzung",""), lead.get("score",0),
         lead.get("score_begruendung",""), lead.get("email_betreff",""),
         lead.get("email_text",""), datetime.now().isoformat()))
    conn.commit(); conn.close()
    return True

def get_leads(status=None, limit=50):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    if status:
        c.execute("""SELECT id,firmenname,branche,ort,website,telefon,email,
            bewertungen_anzahl,bewertungen_score,erreichbarkeit_problem,
            mitarbeiter_schaetzung,score,score_begruendung,
            email_betreff,email_text,status,notiz,created_at
            FROM leads WHERE status=? ORDER BY score DESC, id DESC LIMIT ?""",
            (status, limit))
    else:
        c.execute("""SELECT id,firmenname,branche,ort,website,telefon,email,
            bewertungen_anzahl,bewertungen_score,erreichbarkeit_problem,
            mitarbeiter_schaetzung,score,score_begruendung,
            email_betreff,email_text,status,notiz,created_at
            FROM leads ORDER BY score DESC, id DESC LIMIT ?""", (limit,))
    rows = c.fetchall(); conn.close()
    return rows

def update_lead_status(lead_id, status, notiz=""):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("UPDATE leads SET status=?, notiz=? WHERE id=?", (status, notiz, lead_id))
    conn.commit(); conn.close()

def get_lead_counts():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT status, COUNT(*) FROM leads GROUP BY status")
    rows = c.fetchall(); conn.close()
    return {r[0]: r[1] for r in rows}

def get_today_count():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM leads WHERE created_at LIKE ?", (f"{today}%",))
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

def parse_json_response(text):
    if not text: return []
    if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
    try: return json.loads(text)
    except: return []

# ============================================================
# DEMO HUNTER AGENT
# ============================================================
def run_demo_hunter(branchen, regionen, min_score, email_stil, daily_limit, absender_name):
    ak, tk = get_api_keys()
    if not ak: st.error("⚠ ANTHROPIC_API_KEY fehlt!"); return 0
    if not tk: st.error("⚠ TAVILY_API_KEY fehlt!"); return 0

    client = anthropic.Anthropic(api_key=ak)
    status_box = st.empty()
    progress = st.progress(0)

    today_count = get_today_count()
    remaining = daily_limit - today_count
    if remaining <= 0:
        st.warning(f"⚠ Tageslimit von {daily_limit} Leads bereits erreicht!")
        return 0

    saved_count = 0
    total_searches = min(len(branchen) * len(regionen[:3]), remaining * 2)
    search_num = 0

    for branche in branchen:
        for region in regionen[:4]:
            if saved_count >= remaining:
                break

            search_num += 1
            progress.progress(min(int((search_num/total_searches)*60), 60))
            status_box.markdown(f"🔍 Suche **{branche}** in **{region}**...")

            # SCHRITT 1: Leads suchen
            queries = [
                f"{branche} {region} Kontakt",
                f"{branche} {region} Telefon Bewertungen",
            ]

            raw_leads = []
            for query in queries:
                results = tavily_search(query, tk, 4)
                for r in results:
                    if r.get("title") and r.get("url"):
                        raw_leads.append({
                            "title": r.get("title",""),
                            "url": r.get("url",""),
                            "content": r.get("content","")[:400]
                        })

            if not raw_leads:
                continue

            # SCHRITT 2: Claude qualifiziert & erstellt E-Mails
            progress.progress(min(int((search_num/total_searches)*60)+20, 85))
            status_box.markdown(f"🧠 Claude analysiert & schreibt E-Mails für **{branche} {region}**...")

            stil_guide = {
                "professionell": "Formal, respektvoll, klar strukturiert",
                "locker": "Freundlich, persönlich, nicht steif",
                "direkt": "Kurz, auf den Punkt, kein Smalltalk",
            }.get(email_stil, "Professionell")

            prompt = f"""Du bist der Demo-Hunter für VIKIphone (KI-Telefonassistenz, B2B SaaS).

VIKIphone USPs:
- 24/7 KI-Telefonassistent — kein verpasster Anruf mehr
- Zero-Latency (klingt wie echter Mensch)
- DSGVO Medical Mode (speziell für {branche})
- Dedizierte Festnetz-Rufnummer
- Einfache Integration

GEFUNDENE UNTERNEHMEN ({branche} in {region}):
{json.dumps(raw_leads[:8], ensure_ascii=False)}

Analysiere diese Ergebnisse und erstelle qualifizierte Leads.

Für jeden vielversprechenden Lead:
1. Extrahiere Firmenname, Website, Telefon (falls vorhanden)
2. Bewerte ob sie VIKIphone brauchen (Score 1-10)
3. Schreibe eine personalisierte E-Mail

Score-Kriterien:
- Hat keine sichtbare KI-Lösung (+3)
- Branche passt perfekt zu VIKIphone (+2)
- Erwähnung von Erreichbarkeitsproblemen (+2)
- Kleine/mittlere Praxis/Betrieb 2-20 MA (+2)
- Hat Website/Online-Präsenz (+1)

E-Mail Stil: {stil_guide}
Absender: {absender_name} von VIKIphone

WICHTIG für die E-Mail:
- Betreff: Persönlich & neugierig machend, max 60 Zeichen
- Kein generischer Text — spezifisch auf diese Firma eingehen
- Problem erwähnen das VIKIphone löst
- Kurze Demo anfragen (15 Minuten)
- Maximal 150 Wörter

Antworte NUR mit JSON-Array (max {min(remaining-saved_count, 3)} Leads):
[{{
    "firmenname": "Name der Firma",
    "branche": "{branche}",
    "ort": "{region}",
    "region": "Deutschland",
    "website": "URL oder leer",
    "telefon": "Telefonnummer oder leer",
    "email": "E-Mail oder leer",
    "bewertungen_anzahl": 0,
    "bewertungen_score": 0.0,
    "erreichbarkeit_problem": 0,
    "mitarbeiter_schaetzung": "2-5 / 5-10 / 10-20",
    "score": 8,
    "score_begruendung": "Warum dieser Score",
    "email_betreff": "Betreff der E-Mail",
    "email_text": "Vollständiger E-Mail Text"
}}]

Nur Leads mit Score >= {min_score}. NUR JSON."""

            try:
                msg = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=3000,
                    messages=[{"role":"user","content":prompt}])
                text = msg.content[0].text.strip()
                leads = parse_json_response(text)

                for lead in leads:
                    if lead.get("score",0) >= min_score:
                        if save_lead(lead):
                            saved_count += 1

            except Exception as e:
                continue

        if saved_count >= remaining:
            break

    progress.progress(100)
    status_box.markdown(f"✅ **Fertig!** {saved_count} neue qualifizierte Leads gefunden!")
    return saved_count

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

        counts = get_lead_counts()
        pending_count = counts.get("pending", 0)

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
            "🎯  Demo-Hunter",
            "🛰  Support",
            "🗄  Backoffice",
            "👾  HR"
        ], label_visibility="collapsed")

        st.markdown("<div style='height:1px; background:#1e1e1e; margin:8px 16px;'></div>", unsafe_allow_html=True)

        if pending_count > 0:
            st.markdown(f"""
            <div style='margin:8px 16px; padding:10px 14px;
                        background:rgba(255,152,0,0.08);
                        border:1px solid rgba(255,152,0,0.3); border-radius:8px;'>
                <div style='font-size:12px; font-weight:600; color:#FF9800;'>
                    ⏳ {pending_count} Lead{'s' if pending_count>1 else ''} warten
                </div>
                <div style='font-size:11px; color:#666; margin-top:2px;'>Freigabe ausstehend</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Sign out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # ============================================================
    # DEMO HUNTER
    # ============================================================
    if "Demo-Hunter" in seite:
        st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:2px;'>
            <div class='page-header'>Demo-Hunter</div>
            <span class='live-badge'>● LIVE</span>
        </div>
        <div class='page-sub'>Findet täglich neue VIKIphone-Kunden & schreibt personalisierte E-Mails</div>
        """, unsafe_allow_html=True)

        # METRIKEN
        counts = get_lead_counts()
        today = get_today_count()
        config = get_demo_config()

        c1,c2,c3,c4,c5 = st.columns(5)
        with c1:
            total = sum(counts.values())
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>🎯</div>
                <div class='metric-number'>{total}</div>
                <div class='metric-label'>Leads gesamt</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card' style='{"border-color:rgba(255,152,0,0.4);" if counts.get("pending",0)>0 else ""}'>
                <div class='metric-icon' style='background:rgba(255,152,0,0.1);'>⏳</div>
                <div class='metric-number' style='color:{"#FF9800" if counts.get("pending",0)>0 else "white"}'>{counts.get("pending",0)}</div>
                <div class='metric-label'>Ausstehend</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon' style='background:rgba(76,175,80,0.1);'>✅</div>
                <div class='metric-number' style='color:#4CAF50;'>{counts.get("approved",0)}</div>
                <div class='metric-label'>Freigegeben</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon' style='background:rgba(244,67,54,0.1);'>❌</div>
                <div class='metric-number'>{counts.get("rejected",0)}</div>
                <div class='metric-label'>Abgelehnt</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-icon'>📅</div>
                <div class='metric-number'>{today}</div>
                <div class='metric-label'>Heute gefunden</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # TABS
        tab_run, tab_leads, tab_config = st.tabs([
            "▶ Agent starten", "📋 Leads & E-Mails", "⚙️ Konfiguration"
        ])

        # ============================================================
        # TAB 1: AGENT STARTEN
        # ============================================================
        with tab_run:
            col_info, col_start = st.columns([2,1])

            with col_info:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🔍 So funktioniert der Demo-Hunter</div>
                    <div style='font-size:13px; color:#555; line-height:2;'>
                        <span style='color:#29B6F6'>①</span> Tavily durchsucht Google nach deinen Zielgruppen<br>
                        <span style='color:#29B6F6'>②</span> Claude analysiert jeden Treffer (Score 1-10)<br>
                        <span style='color:#29B6F6'>③</span> Nur Leads ab deinem Mindest-Score werden gespeichert<br>
                        <span style='color:#29B6F6'>④</span> Für jeden Lead schreibt Claude eine personalisierte E-Mail<br>
                        <span style='color:#FF9800'>⑤</span> Du prüfst & gibst frei — du sendest selbst
                    </div>
                </div>""", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>📊 Aktuelle Konfiguration</div>
                """, unsafe_allow_html=True)

                cfg = get_demo_config()
                st.markdown(f"""
                <div style='font-size:13px; color:#555; line-height:2;'>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #1e1e1e; padding:6px 0;'>
                        <span>Zielgruppen</span>
                        <span style='color:#fff;'>{', '.join(cfg.get('branchen',[]))}</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #1e1e1e; padding:6px 0;'>
                        <span>Regionen</span>
                        <span style='color:#fff;'>{', '.join(cfg.get('regionen',[])[:4])}...</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #1e1e1e; padding:6px 0;'>
                        <span>Mindest-Score</span>
                        <span style='color:#29B6F6; font-weight:600;'>{cfg.get('min_score',7)}/10</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #1e1e1e; padding:6px 0;'>
                        <span>E-Mail Stil</span>
                        <span style='color:#fff;'>{cfg.get('email_stil','professionell').title()}</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; padding:6px 0;'>
                        <span>Tageslimit</span>
                        <span style='color:#fff;'>{cfg.get('daily_limit',10)} Leads · {today} heute bereits</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_start:
                remaining = cfg.get('daily_limit',10) - today
                st.markdown(f"""<div class='config-section'>
                    <div class='config-label'>🎯 Demo-Hunter starten</div>
                    <div style='font-size:13px; color:#555; margin-bottom:16px; line-height:1.8;'>
                        Noch <span style='color:#29B6F6; font-weight:600;'>{remaining}</span> Leads
                        heute möglich.<br><br>
                        Dauer: ca. <span style='color:#fff;'>2-4 Minuten</span><br>
                        Ergebnis: <span style='color:#fff;'>5-10 qualifizierte Leads</span><br>
                        mit fertigen E-Mails
                    </div>
                """, unsafe_allow_html=True)

                if remaining > 0:
                    if st.button("▶ Jetzt Leads suchen", use_container_width=True):
                        cfg = get_demo_config()
                        new_leads = run_demo_hunter(
                            cfg["branchen"], cfg["regionen"],
                            cfg["min_score"], cfg["email_stil"],
                            cfg["daily_limit"], cfg["absender_name"]
                        )
                        if new_leads > 0:
                            st.rerun()
                else:
                    st.warning("Tageslimit erreicht!")
                    st.markdown(f"<div style='font-size:12px; color:#444;'>Morgen wieder verfügbar.</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # Schnell-Stats
                st.markdown(f"""<div class='config-section'>
                    <div class='config-label'>📈 Conversion</div>
                    <div style='font-size:13px; color:#555; line-height:2;'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>Gefunden</span><span style='color:#fff;'>{sum(counts.values())}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>Freigegeben</span><span style='color:#4CAF50;'>{counts.get('approved',0)}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>Kontaktiert</span><span style='color:#29B6F6;'>{counts.get('contacted',0)}</span>
                        </div>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>Demo gebucht</span><span style='color:#9C27B0;'>{counts.get('demo',0)}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

        # ============================================================
        # TAB 2: LEADS & E-MAILS
        # ============================================================
        with tab_leads:
            filter_status = st.radio(
                "Filter",
                ["⏳ Ausstehend", "✅ Freigegeben", "📧 Kontaktiert", "🎯 Demo", "❌ Abgelehnt", "📋 Alle"],
                horizontal=True,
                label_visibility="collapsed"
            )

            status_map = {
                "⏳ Ausstehend": "pending",
                "✅ Freigegeben": "approved",
                "📧 Kontaktiert": "contacted",
                "🎯 Demo": "demo",
                "❌ Abgelehnt": "rejected",
                "📋 Alle": None
            }
            selected_status = status_map.get(filter_status)
            leads = get_leads(status=selected_status, limit=50)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if leads:
                st.markdown(f"<div style='font-size:12px; color:#444; margin-bottom:12px;'>{len(leads)} Leads gefunden</div>", unsafe_allow_html=True)

                branche_icons = {
                    "Arztpraxis": "🏥", "Zahnarztpraxis": "🦷",
                    "Handwerksbetrieb": "🔧", "Anwaltskanzlei": "⚖️",
                    "Physiotherapie": "💪"
                }
                branche_badge = {
                    "Arztpraxis": "badge-arzt", "Zahnarztpraxis": "badge-zahnarzt",
                    "Handwerksbetrieb": "badge-handwerk", "Anwaltskanzlei": "badge-kanzlei",
                    "Physiotherapie": "badge-physio"
                }

                for lead in leads:
                    (lid, firmenname, branche, ort, website, telefon, email,
                     bew_anz, bew_score, err_prob, ma_schaetz, score,
                     score_begr, email_betreff, email_text, lstatus, notiz, created_at) = lead

                    score_class = "score-high" if score >= 8 else "score-mid" if score >= 6 else "score-low"
                    b_icon = branche_icons.get(branche, "🏢")
                    b_badge = branche_badge.get(branche, "badge-sonstige")

                    status_badge_html = {
                        "pending": "<span class='pending-badge'>⏳ Ausstehend</span>",
                        "approved": "<span class='approved-badge'>✅ Freigegeben</span>",
                        "contacted": "<span class='approved-badge'>📧 Kontaktiert</span>",
                        "demo": "<span class='approved-badge' style='color:#9C27B0; border-color:rgba(156,39,176,0.3); background:rgba(156,39,176,0.1);'>🎯 Demo</span>",
                        "rejected": "<span class='rejected-badge'>❌ Abgelehnt</span>",
                    }.get(lstatus, "")

                    website_html = f'<a href="{website}" target="_blank" style="color:#29B6F6; font-size:12px;">🔗 Website</a>' if website else ""

                    with st.expander(f"{b_icon} {firmenname} · {ort} · Score {score}/10"):
                        col_info2, col_email = st.columns([1,1])

                        with col_info2:
                            st.markdown(f"""
                            <div style='margin-bottom:12px; display:flex; align-items:center; gap:8px;'>
                                <div class='score-badge {score_class}'>{score}</div>
                                <div>
                                    <span class='branche-badge {b_badge}'>{branche}</span>
                                    <span style='font-size:11px; color:#444; margin-left:8px;'>{created_at[:10]}</span>
                                </div>
                                <div style='margin-left:auto;'>{status_badge_html}</div>
                            </div>
                            <div style='font-size:13px; color:#555; line-height:2;'>
                                <div class='info-row'><span class='info-label'>Firma</span><span style='color:#fff; font-weight:600;'>{firmenname}</span></div>
                                <div class='info-row'><span class='info-label'>Ort</span><span>{ort}</span></div>
                                <div class='info-row'><span class='info-label'>Branche</span><span>{branche}</span></div>
                                <div class='info-row'><span class='info-label'>Mitarbeiter</span><span>{ma_schaetz or '–'}</span></div>
                                <div class='info-row'><span class='info-label'>Telefon</span><span>{telefon or '–'}</span></div>
                                <div class='info-row'><span class='info-label'>E-Mail</span><span>{email or '–'}</span></div>
                                <div class='info-row'><span class='info-label'>Website</span>{website_html if website_html else '<span>–</span>'}</div>
                            </div>
                            <div style='margin-top:12px; background:#0a0a0a; border:1px solid #1e1e1e; border-radius:8px; padding:10px;'>
                                <div style='font-size:11px; color:#444; margin-bottom:4px;'>SCORE BEGRÜNDUNG</div>
                                <div style='font-size:12px; color:#666;'>{score_begr}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col_email:
                            st.markdown(f"""
                            <div style='font-size:11px; color:#444; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;'>FERTIGE E-MAIL</div>
                            <div class='email-subject'>📧 {email_betreff}</div>
                            <div class='email-preview'>{email_text}</div>
                            """, unsafe_allow_html=True)

                        # AKTIONS-BUTTONS
                        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

                        if lstatus == "pending":
                            ba, bb, bc = st.columns([1,1,1])
                            with ba:
                                if st.button("✅ Freigeben", key=f"app_{lid}"):
                                    update_lead_status(lid, "approved")
                                    st.rerun()
                            with bb:
                                if st.button("📧 Als kontaktiert markieren", key=f"con_{lid}"):
                                    update_lead_status(lid, "contacted")
                                    st.rerun()
                            with bc:
                                if st.button("❌ Ablehnen", key=f"rej_{lid}"):
                                    update_lead_status(lid, "rejected")
                                    st.rerun()

                        elif lstatus == "approved":
                            ba, bb = st.columns([1,1])
                            with ba:
                                if st.button("📧 Als kontaktiert", key=f"con2_{lid}"):
                                    update_lead_status(lid, "contacted")
                                    st.rerun()
                            with bb:
                                if st.button("🎯 Demo gebucht!", key=f"demo_{lid}"):
                                    update_lead_status(lid, "demo")
                                    st.rerun()

                        elif lstatus == "contacted":
                            if st.button("🎯 Demo gebucht!", key=f"demo2_{lid}"):
                                update_lead_status(lid, "demo")
                                st.rerun()

                        if notiz:
                            st.markdown(f"<div style='font-size:12px; color:#444; margin-top:8px;'>📝 {notiz}</div>", unsafe_allow_html=True)

            else:
                st.markdown("""
                <div style='text-align:center; padding:60px; color:#333; font-size:14px;'>
                    Noch keine Leads in dieser Kategorie<br>
                    <span style='font-size:12px;'>Starte den Demo-Hunter um Leads zu finden</span>
                </div>
                """, unsafe_allow_html=True)

        # ============================================================
        # TAB 3: KONFIGURATION
        # ============================================================
        with tab_config:
            cfg = get_demo_config()
            col_c1, col_c2 = st.columns([1,1])

            with col_c1:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🏥 Zielgruppen</div>
                """, unsafe_allow_html=True)

                alle_branchen = ["Arztpraxis","Zahnarztpraxis","Handwerksbetrieb",
                                 "Anwaltskanzlei","Physiotherapie","Steuerberater",
                                 "Architekturbüro","Versicherungsmakler","Immobilienmakler"]

                selected_branchen = st.multiselect(
                    "Welche Branchen soll der Agent durchsuchen?",
                    alle_branchen,
                    default=cfg.get("branchen", ["Arztpraxis","Zahnarztpraxis"]),
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>📍 Regionen</div>
                """, unsafe_allow_html=True)

                alle_regionen = ["München","Hamburg","Berlin","Frankfurt","Köln",
                                 "Stuttgart","Düsseldorf","Leipzig","Nürnberg","Bremen",
                                 "Wien","Graz","Zürich","Basel","Genf"]

                selected_regionen = st.multiselect(
                    "In welchen Städten suchen?",
                    alle_regionen,
                    default=cfg.get("regionen", ["München","Hamburg","Berlin"]),
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

            with col_c2:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>⚙️ Agent Einstellungen</div>
                """, unsafe_allow_html=True)

                min_score = st.slider(
                    "Mindest-Score (nur Leads ab diesem Score)",
                    1, 10, cfg.get("min_score",7),
                    help="Je höher, desto weniger aber bessere Leads"
                )

                daily_limit = st.slider(
                    "Tageslimit (max. Leads pro Tag)",
                    5, 50, cfg.get("daily_limit",10)
                )

                email_stil = st.selectbox(
                    "E-Mail Stil",
                    ["professionell","locker","direkt"],
                    index=["professionell","locker","direkt"].index(cfg.get("email_stil","professionell"))
                )
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>✉️ Absender</div>
                """, unsafe_allow_html=True)

                absender_name = st.text_input(
                    "Dein Name / Absender",
                    value=cfg.get("absender_name","VIKIphone Team")
                )
                absender_email = st.text_input(
                    "Deine E-Mail Adresse",
                    value=cfg.get("absender_email",""),
                    placeholder="dein@email.de"
                )
                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("💾 Konfiguration speichern", use_container_width=True):
                save_demo_config(
                    selected_branchen, selected_regionen,
                    min_score, email_stil, daily_limit,
                    absender_name, absender_email
                )
                st.success("✅ Konfiguration gespeichert!")

    # ============================================================
    # ANDERE MODULE — COMING SOON
    # ============================================================
    elif "Support" in seite:
        st.markdown("<div class='page-header'>Support</div><div class='page-sub'>E-Mail Assistenz & Ticket Management</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:40px; margin-bottom:16px;'>🛰</div>
            <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>Ticket-Master</div>
            <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>
                Liest dein Support-Postfach via IMAP, analysiert Stimmung und erstellt fertige Antwort-Entwürfe
            </div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px;
                         padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)

    elif "Backoffice" in seite:
        st.markdown("<div class='page-header'>Backoffice</div><div class='page-sub'>Rechnungen & Finanzdaten</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:40px; margin-bottom:16px;'>🗄</div>
            <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>Beleg-Nerd</div>
            <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>
                PDF Rechnungen hochladen → automatische Datenextraktion → CSV Export
            </div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px;
                         padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)

    elif "HR" in seite:
        st.markdown("<div class='page-header'>HR & Recruiting</div><div class='page-sub'>Bewerbermanagement</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:40px; margin-bottom:16px;'>👾</div>
            <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>CV-Scanner</div>
            <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>
                Lebensläufe analysieren, Matching-Score berechnen & Interview-Fragen generieren
            </div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px;
                         padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 4</span>
        </div>""", unsafe_allow_html=True)
