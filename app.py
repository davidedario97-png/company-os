import streamlit as st
import yaml
import os
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Company OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- LOGIN ---
import streamlit_authenticator as stauth

credentials = {
    "usernames": {
        "admin": {
            "name": "Administrator",
            "password": "$2b$12$tgBi1dFDMBaDW5E8jAHBpuZL3NMgYkLpIZrnPkCBVkq0Z8YQkPqGy"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "company_os_cookie",
    "company_os_key_2024",
    30
)

name, authentication_status, username = authenticator.login("🔐 Company OS Login", "main")

if authentication_status == False:
    st.error("❌ Falscher Benutzername oder Passwort")
    st.info("Standard: **admin** / **admin123**")

elif authentication_status == None:
    st.warning("Bitte einloggen")
    st.info("Standard: **admin** / **admin123**")

elif authentication_status == True:
    # SIDEBAR
    with st.sidebar:
        st.markdown("## 🏢 Company OS")
        st.markdown(f"👋 Willkommen, **{name}**")
        st.markdown("---")
        
        seite = st.radio(
            "Navigation",
            ["📣 Marketing", "💼 Vertrieb", "🎧 Support", "📂 Backoffice", "👥 HR"]
        )
        
        st.markdown("---")
        authenticator.logout("🚪 Logout", "sidebar")

    # HAUPTBEREICH
    st.title(seite)
    st.markdown("---")
    st.info("🚧 Dieses Modul wird gerade gebaut. Kommt bald!")
