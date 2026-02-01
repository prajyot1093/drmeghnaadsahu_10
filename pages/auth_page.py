import streamlit as st
from modules.auth import login, register, is_authenticated

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
                if email and password:
                    if login(email, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.warning("Please enter email and password")
            
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
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_role = st.selectbox("Account Type", ["student", "admin"], key="reg_role")
            
            if st.button("Register", use_container_width=True, type="primary"):
                if reg_email and reg_password and reg_name:
                    if register(reg_email, reg_password, reg_name, reg_role):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Email already exists or registration failed")
                else:
                    st.warning("Please fill in all fields")

# Add demo users if they don't exist
def add_demo_users():
    """Add demo users for testing"""
    from modules.database import add_user
    add_user("student@example.com", "student123", "John Doe", "student")
    add_user("admin@example.com", "admin123", "Admin User", "admin")
