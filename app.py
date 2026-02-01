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

# DayNight Admin Inspired Design System
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* ===== CSS Variables - DayNight Inspired ===== */
        :root {
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #06b6d4;
            
            --background: #f8fafc;
            --surface: #ffffff;
            --surface-hover: #f1f5f9;
            
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --text-tertiary: #94a3b8;
            
            --border: #e2e8f0;
            --border-light: #f1f5f9;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            
            --radius-sm: 0.375rem;
            --radius: 0.5rem;
            --radius-md: 0.75rem;
            --radius-lg: 1rem;
        }
        
        /* ===== Base Styles ===== */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main {
            background: var(--background);
            padding: 1.5rem;
        }
        
        .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }
        
        /* ===== Typography ===== */
        h1, h2, h3 {
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em !important;
        }
        
        h1 {
            font-size: 2.25rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        h2 {
            font-size: 1.875rem !important;
            margin-bottom: 1rem !important;
        }
        
        h3 {
            font-size: 1.5rem !important;
            margin-bottom: 0.75rem !important;
        }
        
        p, div, span {
            color: var(--text-secondary);
        }
        
        /* ===== Stat Cards (Metrics) ===== */
        .stMetric {
            background: var(--surface);
            padding: 1.5rem;
            border-radius: var(--radius-lg);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            transition: all 0.2s ease;
        }
        
        .stMetric:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }
        
        .stMetric label {
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
            font-size: 2.25rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
        }
        
        .stMetric [data-testid="stMetricDelta"] {
            font-size: 0.875rem !important;
        }
        
        /* ===== Cards ===== */
        .card, [data-testid="stVerticalBlock"] > div {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            transition: all 0.2s ease;
        }
        
        .card:hover {
            box-shadow: var(--shadow-md);
        }
        
        /* ===== Buttons ===== */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
            color: white;
            border: none;
            border-radius: var(--radius);
            padding: 0.625rem 1.25rem;
            font-weight: 600;
            font-size: 0.875rem;
            box-shadow: var(--shadow);
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, var(--accent-hover) 0%, #4338ca 100%);
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Secondary Button */
        .stButton > button[kind="secondary"] {
            background: var(--surface);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: var(--surface-hover);
        }
        
        /* ===== Form Inputs ===== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 0.625rem 0.875rem !important;
            color: var(--text-primary) !important;
            font-size: 0.875rem !important;
            transition: all 0.2s ease !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
            outline: none !important;
        }
        
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label,
        .stTextArea label {
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* ===== Sidebar ===== */
        [data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--border);
            padding: 1.5rem 1rem;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--text-primary);
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        [data-testid="stSidebar"] .stRadio > label:hover {
            background: var(--surface-hover);
            border-color: var(--accent);
        }
        
        [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
            background-color: var(--accent) !important;
        }
        
        /* ===== Tabs ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: var(--surface);
            padding: 0.5rem;
            border-radius: var(--radius);
            border: 1px solid var(--border);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border: none;
            border-radius: var(--radius-sm);
            padding: 0.625rem 1rem;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.2s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: var(--surface-hover);
            color: var(--text-primary);
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--accent) !important;
            color: white !important;
        }
        
        /* ===== Expanders ===== */
        .streamlit-expanderHeader {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 1rem !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            transition: all 0.2s ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: var(--surface-hover) !important;
            border-color: var(--accent) !important;
        }
        
        .streamlit-expanderContent {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-top: none !important;
            border-radius: 0 0 var(--radius) var(--radius) !important;
            padding: 1rem !important;
        }
        
        /* ===== Alerts & Messages ===== */
        .stAlert {
            border-radius: var(--radius) !important;
            border: 1px solid var(--border) !important;
            padding: 1rem !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stSuccess {
            background: #f0fdf4 !important;
            border-left: 4px solid var(--success) !important;
            color: #166534 !important;
        }
        
        .stInfo {
            background: #eff6ff !important;
            border-left: 4px solid var(--info) !important;
            color: #1e40af !important;
        }
        
        .stWarning {
            background: #fffbeb !important;
            border-left: 4px solid var(--warning) !important;
            color: #92400e !important;
        }
        
        .stError {
            background: #fef2f2 !important;
            border-left: 4px solid var(--danger) !important;
            color: #991b1b !important;
        }
        
        /* ===== Progress Bar ===== */
        .stProgress > div > div > div {
            background: var(--accent) !important;
        }
        
        /* ===== Data Tables ===== */
        .dataframe {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
        }
        
        .dataframe thead tr {
            background: var(--surface-hover) !important;
        }
        
        .dataframe thead th {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.75rem !important;
            letter-spacing: 0.05em;
            padding: 0.75rem !important;
        }
        
        .dataframe tbody td {
            padding: 0.75rem !important;
            color: var(--text-secondary) !important;
        }
        
        /* ===== Status Badges ===== */
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        /* ===== Custom Scrollbar ===== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--surface-hover);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: var(--radius);
        }
        
        /* ===== File Uploader ===== */
        [data-testid="stFileUploader"] {
            background: var(--surface);
            border: 2px dashed var(--border);
            border-radius: var(--radius-lg);
            padding: 2rem;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: var(--accent);
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Check if user is authenticated
    if not is_authenticated():
        auth_page.show_auth_page()
    else:
        user = get_current_user()
        
        # Top navigation bar
        st.markdown(f"""
            <div style="background: var(--surface); padding: 1rem 2rem; margin: -1rem -1rem 2rem; 
                        border-bottom: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <h2 style="margin: 0; color: var(--accent);">🎓 DayNight Admin</h2>
                        <span style="color: var(--text-tertiary);">|</span>
                        <span style="color: var(--text-secondary); font-weight: 500;">{user['role'].title()} Portal</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="color: var(--text-secondary); font-weight: 500;">👤 {user['name']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"""
                <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem;">
                    <div style="width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), var(--accent-hover)); 
                                margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; font-size: 2rem;">
                        👤
                    </div>
                    <h3 style="margin: 0.5rem 0 0.25rem; color: var(--text-primary);">{user['name']}</h3>
                    <p style="margin: 0; color: var(--text-secondary); font-size: 0.875rem; text-transform: uppercase; 
                              letter-spacing: 0.05em;">{user['role']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if user['role'] == 'student':
                st.markdown("**MENU**")
                page = st.radio(
                    "nav",
                    ["🏠 Dashboard", "👤 Profile", "📋 Service Requests", "🎫 Tickets",
                     "📊 Analytics", "📄 Documents", "📋 Attendance", "📝 Exams", 
                     "🎯 GPA Calculator", "📥 Export Data", "🔔 Notifications", 
                     "🔍 Search", "💰 Fee Management"],
                    key="student_nav",
                    label_visibility="collapsed"
                )
            else:
                st.markdown("**ADMIN MENU**")
                page = st.radio(
                    "nav",
                    ["🏠 Dashboard", "📋 Service Requests", "🎫 Tickets", 
                     "🎓 Admission Requests", "📊 Analytics", 
                     "📄 Documents", "📋 Attendance", "📝 Exams", 
                     "💰 Fees", "⚙️ Workflow"],
                    key="admin_nav",
                    label_visibility="collapsed"
                )
            
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True, type="secondary"):
                logout()
                st.rerun()
        
        # Route to appropriate page (clean up page name)
        page_clean = page.split(" ", 1)[-1]  # Remove emoji
        if user['role'] == 'student':
            student_dashboard.show_student_page(page_clean, user['id'])
        else:
            admin_dashboard.show_admin_page(page_clean)

if __name__ == "__main__":
    main()
