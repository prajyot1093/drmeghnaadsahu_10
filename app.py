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

# Custom CSS with improved color schema and visibility
st.markdown("""
    <style>
        /* Modern Color Palette with Better Contrast */
        :root {
            --primary: #2563eb;
            --primary-light: #3b82f6;
            --primary-dark: #1e40af;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #06b6d4;
            --bg-light: #f0f4f8;
            --bg-card: #ffffff;
            --border-light: #cbd5e1;
            --text-dark: #1e293b;
            --text-light: #475569;
        }
        
        /* Main background with subtle gradient */
        .main {
            padding-top: 2rem;
            background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
        }
        
        /* Improved Metrics with visible backgrounds */
        .stMetric {
            background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            padding: 1.5rem;
            border-radius: 0.875rem;
            border: 2px solid #e2e8f0;
            border-left: 6px solid #2563eb;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            transition: all 0.3s ease;
        }
        
        .stMetric label {
            color: #475569 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: #1e293b !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }
        
        .stMetric:hover {
            box-shadow: 0 4px 6px rgba(37,99,235,0.1);
            border-left-color: #3b82f6;
        }
        
        /* Enhanced Card styling with better visibility */
        .card {
            background-color: #ffffff;
            padding: 1.75rem;
            border-radius: 0.875rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 2px solid #e2e8f0;
            border-top: 5px solid #2563eb;
            transition: all 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 6px 20px rgba(37,99,235,0.15);
            border-top-color: #3b82f6;
            transform: translateY(-2px);
        }
        
        /* Container backgrounds */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > div {
            background: transparent;
        }
        
        /* Info boxes with visible backgrounds */
        .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: 0.75rem;
            padding: 1rem 1.25rem;
            border-left: 5px solid;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
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
        
        /* Enhanced Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #e0e7ff 100%);
            border-right: 2px solid #cbd5e1;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            background-color: #ffffff;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            margin: 0.25rem 0;
            border: 2px solid #e2e8f0;
            transition: all 0.2s ease;
        }
        
        [data-testid="stSidebar"] .stRadio > label:hover {
            background-color: #dbeafe;
            border-color: #2563eb;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #f1f5f9 !important;
            border: 2px solid #cbd5e1 !important;
            border-radius: 0.5rem !important;
            font-weight: 600 !important;
            color: #1e293b !important;
        }
        
        .streamlit-expanderContent {
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 0.5rem 0.5rem !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background-color: #f8fafc;
            padding: 0.5rem;
            border-radius: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            color: #475569;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white !important;
            border-color: #2563eb;
        }
        
        /* Enhanced Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea {
            background-color: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-radius: 0.5rem !important;
            padding: 0.75rem !important;
            color: #1e293b !important;
            font-size: 1rem !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
        }
        
        /* Button styling with better visibility */
        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            border: none;
            border-radius: 0.625rem;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            box-shadow: 0 2px 8px rgba(37,99,235,0.25);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
            box-shadow: 0 4px 12px rgba(37,99,235,0.35);
            transform: translateY(-2px);
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
