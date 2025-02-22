# common.py
import streamlit as st
from streamlit_supabase_auth import login_form
import os

def init_session_state():
    if "session" not in st.session_state:
        # Do NOT force a login call here. Instead, just set it to None.
        st.session_state.session = None
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    # Optionally, set a flag to prevent auto re-login after sign-out.
    if "allow_auto_login" not in st.session_state:
        st.session_state.allow_auto_login = True

def perform_login():
    """Wrapper to call login_form only if auto-login is allowed."""
    if st.session_state.allow_auto_login:
        session = login_form(
            url=os.getenv("SUPABASE_URL"),
            apiKey=os.getenv("SUPABASE_ANON_KEY"),
            providers=["google"],
        )
        if session:
            st.session_state.session = session
            st.session_state.show_login = False
    return st.session_state.session

def sign_out():
    """Sign out both pages by resetting session state."""
    st.session_state.session = None
    st.session_state.show_login = False
    # Disable auto-login if you want the user to remain signed out.
    st.session_state.allow_auto_login = False
