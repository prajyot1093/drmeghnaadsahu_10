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

# Custom CSS with improved color schema
st.markdown("""
    <style>
        /* Modern Color Palette */
        :root {
            --primary: #2563eb;
            --primary-light: #3b82f6;
            --primary-dark: #1e40af;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #06b6d4;
            --bg-light: #f8fafc;
            --border-light: #e2e8f0;
        }
        
        .main {
            padding-top: 2rem;
            background-color: #ffffff;
        }
        
        /* Metrics with gradient backgrounds */
        .stMetric {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 1.25rem;
            border-radius: 0.75rem;
            border-left: 5px solid #2563eb;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            box-shadow: 0 4px 6px rgba(37,99,235,0.1);
            border-left-color: #3b82f6;
        }
        
        /* Card styling */
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-top: 4px solid #2563eb;
            transition: box-shadow 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 4px 12px rgba(37,99,235,0.12);
        }
        
        /* Status badge colors */
        .status-submitted {
            background-color: #dbeafe;
            color: #1e40af;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 500;
        }
        
        .status-inprogress {
            background-color: #fef3c7;
            color: #92400e;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 500;
        }
        
        .status-resolved {
            background-color: #dcfce7;
            color: #166534;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 500;
        }
        
        /* Sidebar styling */
        .sidebar {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #1e40af;
            box-shadow: 0 4px 8px rgba(37,99,235,0.2);
        }
        
        /* Headers styling */
        h1, h2, h3 {
            color: #1e293b;
            font-weight: 600;
        }
        
        /* Divider styling */
        hr {
            border-color: #e2e8f0;
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
                    ["Dashboard", "Profile", "My Requests", "Admission", "Exam Registration", "Submit Ticket", "📊 Analytics", "📄 Documents", "📋 Attendance", "📝 Exams", "🎯 GPA", "📥 Export", "🔔 Notifications", "🔍 Search", "💰 Fees"],
                    key="student_nav"
                )
            else:
                st.markdown("### Admin Dashboard")
                page = st.radio(
                    "Navigation",
                    ["Dashboard", "Service Requests", "Tickets", "Admission Requests", "Analytics", "📄 Documents", "📋 Attendance", "📝 Exams", "💰 Fees", "⚙️ Workflow"],
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
