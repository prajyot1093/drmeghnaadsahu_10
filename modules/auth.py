import streamlit as st
from modules.database import get_user, add_user
from datetime import datetime

def initialize_session():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

def login(email: str, password: str) -> bool:
    """Authenticate user"""
    user = get_user(email, password)
    if user:
        st.session_state.user_id = user['user_id']
        st.session_state.user_email = user['email']
        st.session_state.user_role = user['role']
        st.session_state.user_name = user['full_name']
        st.session_state.logged_in = True
        return True
    return False

def logout():
    """Logout user"""
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.logged_in = False

def register(email: str, password: str, full_name: str, role: str) -> bool:
    """Register new user"""
    return add_user(email, password, full_name, role)

def is_authenticated() -> bool:
    """Check if user is logged in"""
    return st.session_state.get('logged_in', False)

def get_current_user() -> dict:
    """Get current logged in user info"""
    return {
        'user_id': st.session_state.get('user_id'),
        'email': st.session_state.get('user_email'),
        'role': st.session_state.get('user_role'),
        'name': st.session_state.get('user_name')
    }

def require_role(required_role: str):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_authenticated():
                st.warning("Please login first")
                return
            if st.session_state.user_role != required_role:
                st.error(f"This page requires {required_role} role")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
