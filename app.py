import streamlit as st
import anthropic
import json
import sqlite3
import os
from datetime import datetime
import urllib.request
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
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text-secondary) !important; font-family: 'Inter', sans-serif !important;
    font-size: 12px !important; font-weight: 500 !important;
    text-transform: none !important; letter-spacing: 0 !important;
}

::-webkit-scrollbar { width: 4px; }
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

.lead-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px; margin-bottom: 12px;
}
.score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 44px; height: 44px; border-radius: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 800;
}
.score-high { background: rgba(76,175,80,0.15); color: #4CAF50; border: 1px solid rgba(76,175,80,0.3); }
.score-mid  { background: rgba(255,152,0,0.15); color: #FF9800; border: 1px solid rgba(255,152,0,0.3); }
.score-low  { background: rgba(244,67,54,0.15); color: #f44336; border: 1px solid rgba(244,67,54,0.3); }

.info-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 8px; margin: 12px 0;
}
.info-item {
    background: #0a0a0a; border: 1px solid #1e1e1e;
    border-radius: 8px; padding: 10px 12px;
}
.info-item-label { font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.info-item-value { font-size: 13px; color: #fff; font-weight: 500; }
.info-item-value.highlight { color: #29B6F6; }
.info-item-value.name { color: #4FC3F7; font-weight: 700; }

.email-box {
    background: #0a0a0a; border: 1px solid #1e1e1e;
    border-radius: 8px; padding: 16px; margin-top: 4px;
}
.email-subject {
    font-size: 13px; font-weight: 600; color: var(--viki-blue);
    padding-bottom: 10px; margin-bottom: 10px;
    border-bottom: 1px solid #1e1e1e;
}
.email-text {
    font-size: 13px; color: #777; line-height: 1.7;
    white-space: pre-wrap; font-family: 'Inter', sans-serif;
}

.config-section {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 20px; margin-bottom: 12px;
}
.config-label { font-size: 13px; font-weight: 600; color: #fff; margin-bottom: 12px; }

.page-header {
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px;
    font-weight: 700; color: #fff; margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: #666; margin-bottom: 24px; }
.viki-divider { height: 1px; background: #1e1e1e; margin: 20px 0; }

.live-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.3);
    color: #4CAF50; border-radius: 20px; padding: 3px 10px; font-size: 11px; font-weight: 600;
}
.pending-badge   { display:inline-flex; background:rgba(255,152,0,0.1); border:1px solid rgba(255,152,0,0.3); color:#FF9800; border-radius:20px; padding:3px 10px; font-size:11px; font-weight:600; }
.approved-badge  { display:inline-flex; background:rgba(76,175,80,0.1); border:1px solid rgba(76,175,80,0.3); color:#4CAF50; border-radius:20px; padding:3px 10px; font-size:11px; font-weight:600; }
.contacted-badge { display:inline-flex; background:rgba(41,182,246,0.1); border:1px solid rgba(41,182,246,0.3); color:#29B6F6; border-radius:20px; padding:3px 10px; font-size:11px; font-weight:600; }
.demo-badge      { display:inline-flex; background:rgba(156,39,176,0.1); border:1px solid rgba(156,39,176,0.3); color:#9C27B0; border-radius:20px; padding:3px 10px; font-size:11px; font-weight:600; }
.rejected-badge  { display:inline-flex; background:rgba(244,67,54,0.1); border:1px solid rgba(244,67,54,0.3); color:#f44336; border-radius:20px; padding:3px 10px; font-size:11px; font-weight:600; }

.coming-soon {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 60px; text-align: center;
}

.dedup-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(0,188,212,0.1); border: 1px solid rgba(0,188,212,0.3);
    color: #00BCD4; border-radius: 20px; padding: 3px 10px; font-size: 11px; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================
def init_db():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS demo_config (
        id INTEGER PRIMARY KEY,
        zielgruppen TEXT,
        regionen TEXT,
        min_score INTEGER DEFAULT 7,
        email_stil TEXT DEFAULT 'professionell',
        daily_limit INTEGER DEFAULT 10,
        absender_name TEXT DEFAULT 'VIKIphone Team',
        absender_email TEXT DEFAULT '',
        updated_at TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firmenname TEXT,
        zielgruppe TEXT,
        ort TEXT,
        adresse TEXT,
        telefon TEXT,
        email TEXT,
        website TEXT,
        entscheider_name TEXT,
        entscheider_titel TEXT,
        bewertungen_anzahl INTEGER DEFAULT 0,
        bewertungen_score REAL DEFAULT 0,
        score INTEGER DEFAULT 0,
        score_begruendung TEXT,
        email_betreff TEXT,
        email_text TEXT,
        kaltakquise_notiz TEXT,
        status TEXT DEFAULT 'pending',
        notiz TEXT,
        created_at TEXT
    )""")

    # Bereits gesehene Firmen für Deduplizierung
    c.execute("""CREATE TABLE IF NOT EXISTS seen_leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fingerprint TEXT UNIQUE,
        created_at TEXT
    )""")

    c.execute("SELECT COUNT(*) FROM demo_config")
    if c.fetchone()[0] == 0:
        zg = json.dumps([
            "Arztpraxis", "Zahnarztpraxis", "Physiotherapie",
            "Handwerksbetrieb", "Anwaltskanzlei"
        ])
        reg = json.dumps([
            "München", "Hamburg", "Berlin", "Frankfurt",
            "Köln", "Stuttgart", "Düsseldorf", "Wien"
        ])
        c.execute("""INSERT INTO demo_config
            (zielgruppen,regionen,min_score,email_stil,daily_limit,
             absender_name,absender_email,updated_at)
            VALUES (?,?,7,'professionell',10,'VIKIphone Team','',?)""",
            (zg, reg, datetime.now().isoformat()))
    conn.commit(); conn.close()

def get_config():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT * FROM demo_config WHERE id=1")
    row = c.fetchone(); conn.close()
    if row:
        return {
            "zielgruppen": json.loads(row[1]),
            "regionen": json.loads(row[2]),
            "min_score": row[3],
            "email_stil": row[4],
            "daily_limit": row[5],
            "absender_name": row[6],
            "absender_email": row[7],
        }
    return {}

def save_config(zg, reg, min_score, stil, limit, name, email):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""UPDATE demo_config SET
        zielgruppen=?,regionen=?,min_score=?,email_stil=?,
        daily_limit=?,absender_name=?,absender_email=?,updated_at=? WHERE id=1""",
        (json.dumps(zg), json.dumps(reg), min_score, stil,
         limit, name, email, datetime.now().isoformat()))
    conn.commit(); conn.close()

def make_fingerprint(firmenname, ort):
    """Eindeutiger Fingerabdruck für Deduplizierung"""
    raw = f"{firmenname.lower().strip()}-{ort.lower().strip()}"
    raw = re.sub(r'[^a-z0-9äöü]', '', raw)
    return raw

def is_duplicate(firmenname, ort):
    fp = make_fingerprint(firmenname, ort)
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT id FROM seen_leads WHERE fingerprint=?", (fp,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def mark_seen(firmenname, ort):
    fp = make_fingerprint(firmenname, ort)
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO seen_leads (fingerprint,created_at) VALUES (?,?)",
                  (fp, datetime.now().isoformat()))
        conn.commit()
    except: pass
    conn.close()

def save_lead(lead):
    fn = lead.get("firmenname","")
    ort = lead.get("ort","")
    if not fn or is_duplicate(fn, ort):
        return False
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("""INSERT INTO leads
        (firmenname,zielgruppe,ort,adresse,telefon,email,website,
         entscheider_name,entscheider_titel,bewertungen_anzahl,
         bewertungen_score,score,score_begruendung,
         email_betreff,email_text,kaltakquise_notiz,status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'pending',?)""",
        (fn, lead.get("zielgruppe",""), ort,
         lead.get("adresse",""), lead.get("telefon",""),
         lead.get("email",""), lead.get("website",""),
         lead.get("entscheider_name",""), lead.get("entscheider_titel",""),
         lead.get("bewertungen_anzahl",0), lead.get("bewertungen_score",0),
         lead.get("score",0), lead.get("score_begruendung",""),
         lead.get("email_betreff",""), lead.get("email_text",""),
         lead.get("kaltakquise_notiz",""),
         datetime.now().isoformat()))
    conn.commit(); conn.close()
    mark_seen(fn, ort)
    return True

def get_leads(status=None, limit=100):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    if status:
        c.execute("""SELECT * FROM leads WHERE status=?
            ORDER BY score DESC, id DESC LIMIT ?""", (status, limit))
    else:
        c.execute("SELECT * FROM leads ORDER BY score DESC, id DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close()
    return rows

def update_lead(lead_id, status, notiz=""):
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("UPDATE leads SET status=?, notiz=? WHERE id=?", (status, notiz, lead_id))
    conn.commit(); conn.close()

def get_counts():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT status, COUNT(*) FROM leads GROUP BY status")
    rows = c.fetchall(); conn.close()
    return {r[0]:r[1] for r in rows}

def get_today_count():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM leads WHERE created_at LIKE ?", (f"{today}%",))
    n = c.fetchone()[0]; conn.close()
    return n

def get_seen_count():
    conn = sqlite3.connect("vikiphone_os.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM seen_leads")
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
# API HELPERS
# ============================================================
def get_keys():
    ak = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY",""))
    tk = st.secrets.get("TAVILY_API_KEY", os.environ.get("TAVILY_API_KEY",""))
    return ak, tk

def tavily_search(query, api_key, max_results=5):
    try:
        payload = json.dumps({
            "api_key": api_key, "query": query,
            "search_depth": "advanced", "max_results": max_results,
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.tavily.com/search", data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8")).get("results", [])
    except:
        return []

def parse_json(text):
    if not text: return []
    for delimiter in ["```json", "```"]:
        if delimiter in text:
            parts = text.split(delimiter)
            if len(parts) > 1:
                text = parts[1].split("```")[0].strip()
                break
    try:
        result = json.loads(text)
        return result if isinstance(result, list) else []
    except:
        return []

# ============================================================
# DEMO HUNTER AGENT
# ============================================================
def run_demo_hunter(zielgruppen, regionen, min_score, email_stil, daily_limit, absender_name):
    ak, tk = get_keys()
    if not ak: st.error("⚠ ANTHROPIC_API_KEY fehlt!"); return 0
    if not tk: st.error("⚠ TAVILY_API_KEY fehlt!"); return 0

    client = anthropic.Anthropic(api_key=ak)
    status_box = st.empty()
    progress = st.progress(0)

    today_count = get_today_count()
    remaining = daily_limit - today_count
    seen_total = get_seen_count()

    if remaining <= 0:
        st.warning(f"⚠ Tageslimit erreicht! Morgen wieder verfügbar.")
        return 0

    saved_count = 0
    skipped_dupes = 0
    search_num = 0
    total_searches = len(zielgruppen) * min(len(regionen), 4)

    stil_guide = {
        "professionell": "Formal, respektvoll, Sie-Form, klar strukturiert",
        "locker": "Freundlich, persönlich, du-Form, nahbar",
        "direkt": "Sehr kurz, auf den Punkt, kein Smalltalk, max 80 Wörter",
    }.get(email_stil, "professionell")

    for zielgruppe in zielgruppen:
        for region in regionen[:4]:
            if saved_count >= remaining:
                break

            search_num += 1
            progress.progress(min(int((search_num/total_searches)*70), 70))
            status_box.markdown(f"🔍 Suche **{zielgruppe}** in **{region}** · {saved_count} neue Leads · {skipped_dupes} bereits bekannt")

            # Verschiedene Suchstrategien für Abwechslung
            import random
            search_variants = [
                f"{zielgruppe} {region} Telefon Kontakt",
                f"{zielgruppe} {region} Inhaber Ansprechpartner",
                f"{zielgruppe} {region} Bewertungen Google",
                f"{zielgruppe} {region} Praxis Betrieb",
                f"Impressum {zielgruppe} {region}",
            ]
            # Zufällige Auswahl für Abwechslung
            selected_queries = random.sample(search_variants, min(2, len(search_variants)))

            raw_results = []
            for query in selected_queries:
                results = tavily_search(query, tk, 5)
                for r in results:
                    if r.get("title") and r.get("url"):
                        raw_results.append({
                            "title": r.get("title",""),
                            "url": r.get("url",""),
                            "content": r.get("content","")[:500]
                        })

            if not raw_results:
                continue

            progress.progress(min(int((search_num/total_searches)*70)+15, 88))
            status_box.markdown(f"🧠 Claude analysiert **{zielgruppe}** in **{region}**...")

            prompt = f"""Du bist der Demo-Hunter für VIKIphone (KI-Telefonassistenz SaaS).

VIKIphone löst: Verpasste Anrufe, unbesetzte Rezeptionen, teure Call-Center.
USPs: 24/7 KI-Assistent, Zero-Latency, DSGVO Medical Mode, Festnetz-Rufnummer.

ZIELGRUPPE: {zielgruppe} in {region}
GEFUNDENE WEB-DATEN:
{json.dumps(raw_results[:8], ensure_ascii=False, indent=2)}

Extrahiere konkrete Unternehmen und erstelle qualifizierte Leads.

FÜR JEDEN LEAD EXTRAHIERE:
1. Firmenname (exakt wie gefunden)
2. Adresse/Straße (falls vorhanden)
3. Telefonnummer (WICHTIG — suche genau im Content)
4. E-Mail (falls vorhanden)
5. Website URL
6. Entscheider-Name (Dr. Name, Inhaber, Chef — aus Impressum/Website)
7. Entscheider-Titel (Dr., Dipl., Inhaber, GF etc.)
8. Google Bewertungen (Anzahl + Score falls erwähnt)

SCORE KRITERIEN (1-10):
+3 Kein KI-Telefonassistent erkennbar
+2 Perfekte Zielgruppe ({zielgruppe})
+2 Telefonnummer gefunden (für Kaltakquise!)
+1 Entscheider-Name gefunden
+1 Bewertungen zeigen Erreichbarkeitsprobleme
+1 Kleine/mittlere Firma 1-20 Mitarbeiter

KALTAKQUISE NOTIZ:
Schreibe 1-2 Sätze was der Vertriebsmitarbeiter AM TELEFON als Einstieg sagen kann.
Spezifisch auf diese Firma. Nutze Entscheider-Name wenn vorhanden.
Beispiel: "Dr. Müller, ich rufe an weil Ihre Patienten Sie oft nicht erreichen..."

E-MAIL (zusätzlich zur Kaltakquise):
Stil: {stil_guide}
Absender: {absender_name} von VIKIphone
Max 130 Wörter, persönlich, spezifisch

JSON FORMAT:
[{{
    "firmenname": "Exakter Name",
    "zielgruppe": "{zielgruppe}",
    "ort": "{region}",
    "adresse": "Straße Hausnr, PLZ Stadt oder leer",
    "telefon": "+49... oder 0... oder leer",
    "email": "email@domain.de oder leer",
    "website": "https://... oder leer",
    "entscheider_name": "Dr. Max Mustermann oder leer",
    "entscheider_titel": "Inhaber / Dr. / GF oder leer",
    "bewertungen_anzahl": 0,
    "bewertungen_score": 0.0,
    "score": 8,
    "score_begruendung": "Telefon gefunden, kein KI-Tool erkennbar, Dr. Name im Impressum",
    "kaltakquise_notiz": "Dr. Schmidt, ich rufe an weil...",
    "email_betreff": "Ihr Telefon klingelt — wir nehmen ab",
    "email_text": "Vollständiger E-Mail Text..."
}}]

NUR Leads mit Score >= {min_score}.
MAXIMAL {min(remaining - saved_count, 3)} Leads.
NUR JSON — kein anderer Text."""

            try:
                msg = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=3500,
                    messages=[{"role":"user","content":prompt}])
                text = msg.content[0].text.strip()
                leads = parse_json(text)

                for lead in leads:
                    if lead.get("score",0) >= min_score:
                        if save_lead(lead):
                            saved_count += 1
                        else:
                            skipped_dupes += 1
            except Exception as e:
                continue

        if saved_count >= remaining:
            break

    progress.progress(100)
    status_box.markdown(f"✅ **Fertig!** {saved_count} neue Leads · {skipped_dupes} Duplikate übersprungen · {seen_total + saved_count} Firmen insgesamt gesehen")
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
            <div style='font-family: Plus Jakarta Sans; font-size:28px; font-weight:800; color:#29B6F6; margin-bottom:4px;'>VIKIphone</div>
            <div style='font-size:13px; color:#555;'>Company OS · Internal Dashboard</div>
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

        counts = get_counts()
        pending_n = counts.get("pending",0)

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
            "🎯  Demo-Hunter", "🛰  Support", "🗄  Backoffice", "👾  HR"
        ], label_visibility="collapsed")

        st.markdown("<div style='height:1px; background:#1e1e1e; margin:8px 16px;'></div>", unsafe_allow_html=True)

        if pending_n > 0:
            st.markdown(f"""
            <div style='margin:8px 16px; padding:10px 14px; background:rgba(255,152,0,0.08); border:1px solid rgba(255,152,0,0.3); border-radius:8px;'>
                <div style='font-size:12px; font-weight:600; color:#FF9800;'>⏳ {pending_n} Lead{'s' if pending_n>1 else ''} warten</div>
                <div style='font-size:11px; color:#555; margin-top:2px;'>Freigabe ausstehend</div>
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
            <span class='dedup-badge'>✓ Duplikat-Schutz aktiv</span>
        </div>
        <div class='page-sub'>Findet täglich neue VIKIphone-Kunden mit Telefon & Entscheider-Name</div>
        """, unsafe_allow_html=True)

        counts = get_counts()
        today = get_today_count()
        seen = get_seen_count()
        cfg = get_config()

        # METRIKEN
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        with c1:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon'>🎯</div>
                <div class='metric-number'>{sum(counts.values())}</div>
                <div class='metric-label'>Leads gesamt</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card' style='{"border-color:rgba(255,152,0,0.4);" if pending_n>0 else ""}'>
                <div class='metric-icon' style='background:rgba(255,152,0,0.1);'>⏳</div>
                <div class='metric-number' style='color:{"#FF9800" if pending_n>0 else "white"}'>{pending_n}</div>
                <div class='metric-label'>Ausstehend</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon' style='background:rgba(76,175,80,0.1);'>✅</div>
                <div class='metric-number' style='color:#4CAF50;'>{counts.get('approved',0)}</div>
                <div class='metric-label'>Freigegeben</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon' style='background:rgba(41,182,246,0.1);'>📧</div>
                <div class='metric-number' style='color:#29B6F6;'>{counts.get('contacted',0)}</div>
                <div class='metric-label'>Kontaktiert</div></div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon' style='background:rgba(156,39,176,0.1);'>🎯</div>
                <div class='metric-number' style='color:#9C27B0;'>{counts.get('demo',0)}</div>
                <div class='metric-label'>Demos</div></div>""", unsafe_allow_html=True)
        with c6:
            st.markdown(f"""<div class='metric-card'><div class='metric-icon' style='background:rgba(0,188,212,0.1);'>🔒</div>
                <div class='metric-number' style='color:#00BCD4;'>{seen}</div>
                <div class='metric-label'>Bereits gesehen</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        tab_run, tab_leads, tab_config = st.tabs([
            "▶ Agent starten", "📋 Leads & Kaltakquise", "⚙️ Konfiguration"
        ])

        # ============================================================
        # TAB 1: STARTEN
        # ============================================================
        with tab_run:
            col_left, col_right = st.columns([2,1])

            with col_left:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🔍 Was der Demo-Hunter macht</div>
                    <div style='font-size:13px; color:#555; line-height:2.2;'>
                        <span style='color:#29B6F6'>①</span> Sucht <b style='color:#fff'>neue</b> Unternehmen deiner Zielgruppen (Duplikate werden übersprungen)<br>
                        <span style='color:#29B6F6'>②</span> Extrahiert: Firmenname · Adresse · <b style='color:#4CAF50'>Telefonnummer</b> · <b style='color:#4FC3F7'>Entscheider-Name</b><br>
                        <span style='color:#29B6F6'>③</span> Claude bewertet jeden Lead (Score 1-10)<br>
                        <span style='color:#29B6F6'>④</span> Schreibt personalisierte E-Mail + <b style='color:#FF9800'>Kaltakquise-Einstieg</b> fürs Telefon<br>
                        <span style='color:#FF9800'>⑤</span> Du prüfst, gibst frei und kontaktierst selbst
                    </div>
                </div>""", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>📊 Aktuelle Einstellungen</div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style='font-size:13px; color:#555; line-height:2;'>
                    <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #1e1e1e;'>
                        <span>Zielgruppen</span><span style='color:#fff;'>{" · ".join(cfg.get("zielgruppen",[]))}</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #1e1e1e;'>
                        <span>Regionen</span><span style='color:#fff;'>{" · ".join(cfg.get("regionen",[])[:5])}</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #1e1e1e;'>
                        <span>Mindest-Score</span><span style='color:#29B6F6; font-weight:700;'>{cfg.get("min_score",7)}/10</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #1e1e1e;'>
                        <span>E-Mail Stil</span><span style='color:#fff;'>{cfg.get("email_stil","professionell").title()}</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; padding:6px 0;'>
                        <span>Tageslimit</span><span style='color:#fff;'>{today}/{cfg.get("daily_limit",10)} heute</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_right:
                remaining = cfg.get("daily_limit",10) - today
                st.markdown(f"""<div class='config-section'>
                    <div class='config-label'>🚀 Starten</div>
                    <div style='font-size:13px; color:#555; line-height:1.9; margin-bottom:16px;'>
                        Noch <span style='color:#29B6F6; font-weight:700;'>{remaining}</span> Leads heute möglich<br>
                        <span style='color:#00BCD4;'>✓ {seen} Firmen bereits bekannt</span><br>
                        → werden automatisch übersprungen<br><br>
                        Dauer: <span style='color:#fff;'>2-5 Minuten</span><br>
                        Ergebnis: <span style='color:#fff;'>5-10 neue Leads</span>
                    </div>
                """, unsafe_allow_html=True)

                if remaining > 0:
                    if st.button("▶ Neue Leads suchen", use_container_width=True):
                        n = run_demo_hunter(
                            cfg["zielgruppen"], cfg["regionen"],
                            cfg["min_score"], cfg["email_stil"],
                            cfg["daily_limit"], cfg["absender_name"]
                        )
                        if n > 0: st.rerun()
                else:
                    st.warning("Tageslimit erreicht!")

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(f"""<div class='config-section'>
                    <div class='config-label'>📈 Pipeline</div>
                    <div style='font-size:13px; line-height:2.2;'>
                        <div style='display:flex; justify-content:space-between;'><span style='color:#555;'>Neu gefunden</span><span style='color:#fff;'>{sum(counts.values())}</span></div>
                        <div style='display:flex; justify-content:space-between;'><span style='color:#555;'>Freigegeben</span><span style='color:#4CAF50;'>{counts.get("approved",0)}</span></div>
                        <div style='display:flex; justify-content:space-between;'><span style='color:#555;'>Kontaktiert</span><span style='color:#29B6F6;'>{counts.get("contacted",0)}</span></div>
                        <div style='display:flex; justify-content:space-between;'><span style='color:#555;'>Demo gebucht</span><span style='color:#9C27B0;'>{counts.get("demo",0)}</span></div>
                        <div style='display:flex; justify-content:space-between;'><span style='color:#555;'>Abgelehnt</span><span style='color:#f44336;'>{counts.get("rejected",0)}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        # ============================================================
        # TAB 2: LEADS
        # ============================================================
        with tab_leads:
            filter_col, search_col = st.columns([2,3])
            with filter_col:
                filter_status = st.radio("Filter", [
                    "⏳ Ausstehend", "✅ Freigegeben", "📧 Kontaktiert",
                    "🎯 Demo", "❌ Abgelehnt", "📋 Alle"
                ], horizontal=True, label_visibility="collapsed")

            status_map = {
                "⏳ Ausstehend":"pending", "✅ Freigegeben":"approved",
                "📧 Kontaktiert":"contacted", "🎯 Demo":"demo",
                "❌ Abgelehnt":"rejected", "📋 Alle":None
            }
            sel_status = status_map.get(filter_status)
            leads = get_leads(status=sel_status, limit=100)

            st.markdown(f"<div style='font-size:12px; color:#333; margin:8px 0 12px;'>{len(leads)} Leads</div>", unsafe_allow_html=True)

            status_badges = {
                "pending":   "<span class='pending-badge'>⏳ Ausstehend</span>",
                "approved":  "<span class='approved-badge'>✅ Freigegeben</span>",
                "contacted": "<span class='contacted-badge'>📧 Kontaktiert</span>",
                "demo":      "<span class='demo-badge'>🎯 Demo</span>",
                "rejected":  "<span class='rejected-badge'>❌ Abgelehnt</span>",
            }

            if leads:
                for lead in leads:
                    (lid, fn, zg, ort, adresse, tel, email, website,
                     entsch_name, entsch_titel, bew_anz, bew_score,
                     score, score_begr, email_betreff, email_text,
                     kalt_notiz, lstatus, notiz, created_at) = lead

                    score_class = "score-high" if score>=8 else "score-mid" if score>=6 else "score-low"
                    sbadge = status_badges.get(lstatus,"")

                    # Entscheider hervorheben
                    entsch_html = ""
                    if entsch_name:
                        entsch_html = f"<span style='color:#4FC3F7; font-weight:700;'>👤 {entsch_titel} {entsch_name}</span>"

                    tel_html = f"<span style='color:#4CAF50; font-weight:700;'>📞 {tel}</span>" if tel else "<span style='color:#333;'>📞 –</span>"

                    with st.expander(f"{'👤 ' if entsch_name else ''}{fn} · {ort} · Score {score}/10 {'📞' if tel else ''}"):
                        col_a, col_b = st.columns([1,1])

                        with col_a:
                            st.markdown(f"""
                            <div style='display:flex; align-items:center; gap:12px; margin-bottom:16px;'>
                                <div class='score-badge {score_class}'>{score}</div>
                                <div style='flex:1;'>
                                    <div style='font-size:15px; font-weight:700; color:#fff;'>{fn}</div>
                                    <div style='font-size:12px; color:#555; margin-top:2px;'>{zg} · {ort} · {created_at[:10]}</div>
                                </div>
                                {sbadge}
                            </div>
                            <div class='info-grid'>
                                <div class='info-item'>
                                    <div class='info-item-label'>Telefon</div>
                                    <div class='info-item-value highlight'>{tel or '–'}</div>
                                </div>
                                <div class='info-item'>
                                    <div class='info-item-label'>Entscheider</div>
                                    <div class='info-item-value name'>{f"{entsch_titel} {entsch_name}".strip() if entsch_name else '–'}</div>
                                </div>
                                <div class='info-item'>
                                    <div class='info-item-label'>E-Mail</div>
                                    <div class='info-item-value'>{email or '–'}</div>
                                </div>
                                <div class='info-item'>
                                    <div class='info-item-label'>Adresse</div>
                                    <div class='info-item-value'>{adresse or ort}</div>
                                </div>
                                <div class='info-item'>
                                    <div class='info-item-label'>Bewertungen</div>
                                    <div class='info-item-value'>{f"⭐ {bew_score} ({bew_anz})" if bew_anz else "–"}</div>
                                </div>
                                <div class='info-item'>
                                    <div class='info-item-label'>Website</div>
                                    <div class='info-item-value'>{f'<a href="{website}" target="_blank" style="color:#29B6F6;">🔗 Link</a>' if website else "–"}</div>
                                </div>
                            </div>
                            <div style='background:#0a0a0a; border:1px solid #1e1e1e; border-radius:8px; padding:12px; margin-top:8px;'>
                                <div style='font-size:10px; color:#444; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;'>Score Begründung</div>
                                <div style='font-size:12px; color:#555;'>{score_begr}</div>
                            </div>
                            """, unsafe_allow_html=True)

                            # KALTAKQUISE NOTIZ
                            if kalt_notiz:
                                st.markdown(f"""
                                <div style='background:rgba(255,152,0,0.05); border:1px solid rgba(255,152,0,0.2); border-left:3px solid #FF9800; border-radius:8px; padding:12px; margin-top:8px;'>
                                    <div style='font-size:10px; color:#FF9800; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;'>📞 KALTAKQUISE EINSTIEG</div>
                                    <div style='font-size:13px; color:#ccc; font-style:italic;'>"{kalt_notiz}"</div>
                                </div>
                                """, unsafe_allow_html=True)

                        with col_b:
                            st.markdown(f"""
                            <div style='font-size:11px; color:#444; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;'>✉️ PERSONALISIERTE E-MAIL</div>
                            <div class='email-box'>
                                <div class='email-subject'>📧 {email_betreff}</div>
                                <div class='email-text'>{email_text}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        # AKTIONEN
                        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                        if lstatus == "pending":
                            ba, bb, bc = st.columns(3)
                            with ba:
                                if st.button("✅ Freigeben", key=f"a_{lid}"):
                                    update_lead(lid, "approved"); st.rerun()
                            with bb:
                                if st.button("📧 Kontaktiert", key=f"c_{lid}"):
                                    update_lead(lid, "contacted"); st.rerun()
                            with bc:
                                if st.button("❌ Ablehnen", key=f"r_{lid}"):
                                    update_lead(lid, "rejected"); st.rerun()

                        elif lstatus == "approved":
                            ba, bb = st.columns(2)
                            with ba:
                                if st.button("📧 Als kontaktiert", key=f"c2_{lid}"):
                                    update_lead(lid, "contacted"); st.rerun()
                            with bb:
                                if st.button("🎯 Demo gebucht!", key=f"d_{lid}"):
                                    update_lead(lid, "demo"); st.rerun()

                        elif lstatus == "contacted":
                            if st.button("🎯 Demo gebucht!", key=f"d2_{lid}"):
                                update_lead(lid, "demo"); st.rerun()

                        if notiz:
                            st.markdown(f"<div style='font-size:12px; color:#444; margin-top:6px;'>📝 {notiz}</div>", unsafe_allow_html=True)

            else:
                st.markdown("""
                <div style='text-align:center; padding:60px; color:#333; font-size:14px;'>
                    Keine Leads in dieser Kategorie
                </div>
                """, unsafe_allow_html=True)

        # ============================================================
        # TAB 3: KONFIGURATION
        # ============================================================
        with tab_config:
            cfg = get_config()
            col1, col2 = st.columns([1,1])

            with col1:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🎯 Zielgruppen</div>
                    <div style='font-size:12px; color:#444; margin-bottom:12px;'>
                        Eine Zielgruppe pro Zeile — du kannst alles frei eingeben!
                    </div>
                """, unsafe_allow_html=True)

                zg_text = st.text_area(
                    "Zielgruppen",
                    value="\n".join(cfg.get("zielgruppen",[])),
                    height=180,
                    placeholder="Arztpraxis\nZahnarztpraxis\nHandwerksbetrieb\noder was auch immer du willst...",
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>📍 Regionen / Städte</div>
                    <div style='font-size:12px; color:#444; margin-bottom:12px;'>
                        Eine Stadt pro Zeile — DACH oder weltweit
                    </div>
                """, unsafe_allow_html=True)

                reg_text = st.text_area(
                    "Regionen",
                    value="\n".join(cfg.get("regionen",[])),
                    height=180,
                    placeholder="München\nBerlin\nHamburg\nWien\nZürich...",
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("""<div class='config-section'>
                    <div class='config-label'>⚙️ Agent Einstellungen</div>
                """, unsafe_allow_html=True)

                min_score = st.slider("Mindest-Score", 1, 10, cfg.get("min_score",7),
                    help="Nur Leads ab diesem Score werden gespeichert")
                daily_limit = st.slider("Tageslimit", 5, 100, cfg.get("daily_limit",10))
                email_stil = st.selectbox("E-Mail Stil",
                    ["professionell","locker","direkt"],
                    index=["professionell","locker","direkt"].index(cfg.get("email_stil","professionell")))
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>✉️ Absender</div>
                """, unsafe_allow_html=True)
                absender_name = st.text_input("Dein Name", value=cfg.get("absender_name","VIKIphone Team"))
                absender_email = st.text_input("Deine E-Mail", value=cfg.get("absender_email",""), placeholder="dein@email.de")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""<div class='config-section'>
                    <div class='config-label'>🔒 Duplikat-Schutz</div>
                    <div style='font-size:13px; color:#555; line-height:1.8;'>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <span style='color:#00BCD4;'>{seen}</span> Firmen bereits gesehen<br>
                    → werden nie nochmal vorgeschlagen
                    </div></div>
                """, unsafe_allow_html=True)

                if st.button("🗑 Duplikat-Speicher leeren", use_container_width=True):
                    conn = sqlite3.connect("vikiphone_os.db")
                    c = conn.cursor()
                    c.execute("DELETE FROM seen_leads")
                    conn.commit(); conn.close()
                    st.success("✅ Duplikat-Speicher geleert — alle Firmen können neu gefunden werden!")
                    st.rerun()

            if st.button("💾 Konfiguration speichern", use_container_width=True):
                new_zg = [z.strip() for z in zg_text.split("\n") if z.strip()]
                new_reg = [r.strip() for r in reg_text.split("\n") if r.strip()]
                save_config(new_zg, new_reg, min_score, email_stil, daily_limit, absender_name, absender_email)
                st.success("✅ Gespeichert!")

    # COMING SOON
    elif "Support" in seite:
        st.markdown("<div class='page-header'>Support</div><div class='page-sub'>E-Mail Assistenz</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:40px; margin-bottom:16px;'>🛰</div>
            <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>Ticket-Master</div>
            <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>IMAP E-Mail Analyse & automatische Antwort-Entwürfe</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)

    elif "Backoffice" in seite:
        st.markdown("<div class='page-header'>Backoffice</div><div class='page-sub'>Rechnungen & Finanzdaten</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:40px; margin-bottom:16px;'>🗄</div>
            <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>Beleg-Nerd</div>
            <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>PDF Rechnungen → automatische CSV Extraktion</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 3</span>
        </div>""", unsafe_allow_html=True)

    elif "HR" in seite:
        st.markdown("<div class='page-header'>HR & Recruiting</div><div class='page-sub'>Bewerbermanagement</div>", unsafe_allow_html=True)
        st.markdown("""<div class='coming-soon'>
            <div style='font-size:40px; margin-bottom:16px;'>👾</div>
            <div style='font-family: Plus Jakarta Sans; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;'>CV-Scanner</div>
            <div style='font-size:13px; color:#555; max-width:400px; margin:0 auto 16px;'>Lebenslauf Matching & Interview-Fragen</div>
            <span style='background:rgba(41,182,246,0.1); color:#29B6F6; border-radius:20px; padding:4px 16px; font-size:12px; font-weight:600;'>Coming Soon · Phase 4</span>
        </div>""", unsafe_allow_html=True)
