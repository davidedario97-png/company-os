import streamlit as st
import yaml
import bcrypt

st.set_page_config(
    page_title="Company OS | Vikiphone",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Einfaches Login ohne streamlit-authenticator ---
USERS = {
    "admin": "admin123"
}

def check_login(username, password):
    if username in USERS and USERS[username] == password:
        return True
    return False

# Session State initialisieren
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🏢 Company OS")
        st.markdown("### Vikiphone Dashboard")
        st.markdown("---")
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        if st.button("🔐 Einloggen", use_container_width=True):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Falscher Benutzername oder Passwort")
        st.markdown("---")
        st.info("Standard: **admin** / **admin123**")

# --- DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("## 🏢 Company OS")
        st.markdown(f"👋 Willkommen, **{st.session_state.username}**!")
        st.markdown("---")
        seite = st.radio(
            "Navigation",
            ["📣 Marketing", "💼 Vertrieb", "🎧 Support", "📂 Backoffice", "👥 HR"]
        )
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.title(seite)
    st.markdown("---")
    st.info("🚧 Dieses Modul wird gerade gebaut. Kommt bald!")
