import streamlit as st
from modules.database import init_database
from modules.auth import initialize_session, is_authenticated, get_current_user, logout
import pages.auth_page as auth_page
import pages.student_dashboard as student_dashboard
import pages.admin_dashboard as admin_dashboard

# Page configuration
st.set_page_config(
    page_title="Unified Service Management Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()

# Initialize session
initialize_session()

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-top: 3px solid #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🎓 Unified Service Management Portal")
    
    # Check if user is authenticated
    if not is_authenticated():
        auth_page.show_auth_page()
    else:
        user = get_current_user()
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"### Welcome, {user['name']}!")
            st.markdown(f"**Role:** {user['role']}")
            
            st.divider()
            
            if user['role'] == 'student':
                st.markdown("### Student Dashboard")
                page = st.radio(
                    "Navigation",
                    ["Dashboard", "Profile", "My Requests", "Admission", "Exam Registration", "Submit Ticket"],
                    key="student_nav"
                )
            else:
                st.markdown("### Admin Dashboard")
                page = st.radio(
                    "Navigation",
                    ["Dashboard", "Service Requests", "Tickets", "Admission Requests", "Analytics"],
                    key="admin_nav"
                )
            
            st.divider()
            
            if st.button("🚪 Logout", key="logout_btn"):
                logout()
                st.rerun()
        
        # Route to appropriate page
        if user['role'] == 'student':
            student_dashboard.show_student_page(page)
        else:
            admin_dashboard.show_admin_page(page)

if __name__ == "__main__":
    main()
