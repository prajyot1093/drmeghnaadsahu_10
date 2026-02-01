import streamlit as st
from modules.auth import login, register, is_authenticated
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """Validate password strength"""
    return len(password) >= 6

def show_auth_page():
    """Display authentication page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <h2>🎓 Welcome to Service Portal</h2>
                <p>Manage your academic requests and track your progress</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for login and registration
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.markdown("### Student / Admin Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.warning("⚠️ Please enter email and password")
                elif not validate_email(email):
                    st.error("❌ Please enter a valid email address")
                elif login(email, password):
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
            
            # Demo credentials
            with st.expander("Demo Credentials"):
                st.info("""
                **Student:**
                - Email: student@example.com
                - Password: student123
                
                **Admin:**
                - Email: admin@example.com
                - Password: admin123
                """)
        
        with tab2:
            st.markdown("### Create New Account")
            
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_role = st.selectbox("Account Type", ["student", "admin"], key="reg_role")
            
            if st.button("Register", use_container_width=True, type="primary"):
                # Validation
                if not all([reg_email, reg_password, reg_confirm_password, reg_name]):
                    st.error("❌ Please fill in all fields")
                elif not validate_email(reg_email):
                    st.error("❌ Please enter a valid email address")
                elif not validate_password(reg_password):
                    st.error("❌ Password must be at least 6 characters")
                elif reg_password != reg_confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(reg_name.strip()) < 2:
                    st.error("❌ Name must be at least 2 characters")
                elif register(reg_email, reg_password, reg_name, reg_role):
                    st.success("✅ Registration successful! Please login with your credentials.")
                else:
                    st.error("❌ Email already exists or registration failed")

# Add demo users if they don't exist
def add_demo_users():
    """Add demo users for testing"""
    from modules.database import add_user
    add_user("student@example.com", "student123", "John Doe", "student")
    add_user("admin@example.com", "admin123", "Admin User", "admin")
