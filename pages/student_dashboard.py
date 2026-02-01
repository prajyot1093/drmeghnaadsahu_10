"""
Student Dashboard Page - Attendance, Exams, and Tickets Only
"""

import streamlit as st
from modules.database import get_user_tickets, submit_ticket

def show_student_page(page, user_id):
    """Display student dashboard based on selected page"""
    
    if page == "Dashboard":
        show_dashboard_home(user_id)
    elif "Attendance" in page:
        from modules.attendance import show_attendance_tracker
        st.markdown("## 📋 My Attendance")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>View your attendance records and statistics</p>", unsafe_allow_html=True)
        show_attendance_tracker(user_id)
    elif "Exam" in page:
        from modules.exams import show_exam_results
        st.markdown("## 📝 My Exam Results")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Check your exam scores and performance</p>", unsafe_allow_html=True)
        show_exam_results(user_id)
    elif page == "Tickets":
        show_student_tickets(user_id)
    elif page == "Complaints":
        show_student_tickets(user_id)  # Tickets serve as complaints

def show_dashboard_home(user_id):
    """Show student dashboard home page"""
    st.markdown("## 🏠 Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, var(--accent), var(--accent-hover)); 
                        padding: 2rem; border-radius: var(--radius-lg); color: white;">
                <h3 style="margin: 0 0 1rem 0;">📋 Attendance</h3>
                <p style="margin: 0;">Track your class attendance</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, var(--accent), var(--accent-hover)); 
                        padding: 2rem; border-radius: var(--radius-lg); color: white;">
                <h3 style="margin: 0 0 1rem 0;">📝 Exams</h3>
                <p style="margin: 0;">View exam results and scores</p>
            </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, var(--accent), var(--accent-hover)); 
                        padding: 2rem; border-radius: var(--radius-lg); color: white; margin-top: 1rem;">
                <h3 style="margin: 0 0 1rem 0;">🎫 Tickets</h3>
                <p style="margin: 0;">Submit and track your tickets</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, var(--accent), var(--accent-hover)); 
                        padding: 2rem; border-radius: var(--radius-lg); color: white; margin-top: 1rem;">
                <h3 style="margin: 0 0 1rem 0;">📧 Complaints</h3>
                <p style="margin: 0;">File and manage complaints</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.info("📌 Use the menu to navigate to different sections")

def show_student_tickets(user_id):
    """Display and manage support tickets and complaints"""
    st.markdown("## 🎫 My Support Tickets & Complaints")
    
    # Create new ticket
    with st.expander("➕ Create New Ticket/Complaint", expanded=False):
        with st.form("ticket_form"):
            subject = st.text_input("Subject", placeholder="Enter ticket/complaint subject")
            category = st.selectbox(
                "Category",
                ["Academic Query", "Fee Related", "Admission", 
                 "Hostel", "Library", "Other"]
            )
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            description = st.text_area("Description", height=150, placeholder="Describe your issue in detail")
            submitted = st.form_submit_button("Submit", use_container_width=True, type="primary")
            
            if submitted and subject and description:
                if submit_ticket(user_id, subject, description, category, priority):
                    st.success("✅ Ticket created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to create ticket")
            elif submitted:
                st.warning("⚠️ Please fill in all required fields")
    
    # Display existing tickets
    st.markdown("### 📋 My Tickets & Complaints")
    tickets = get_user_tickets(user_id)
    
    if tickets:
        for ticket in tickets:
            status_color = {
                "Open": "🔵",
                "In Progress": "🟡",
                "Resolved": "🟢",
                "Closed": "⚫"
            }.get(ticket.get('status', 'Open'), "⚪")
            
            priority_icon = {
                "Low": "🟢",
                "Medium": "🟡",
                "High": "🔴"
            }.get(ticket.get('priority', 'Medium'), "⚪")
            
            # Add styled container for each ticket
            st.markdown(f"""
                <div style="background: var(--surface); padding: 1.25rem; border-radius: var(--radius-lg);
                     border: 2px solid var(--border); border-left: 5px solid var(--accent);
                     margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">
                        {ticket.get('title', 'Ticket')}
                    </div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
                        Category: <strong>{ticket.get('category', 'N/A')}</strong> | 
                        Created: <strong>{ticket.get('created_at', 'N/A')[:10]}</strong>
                    </div>
                    <div style="display: flex; gap: 1rem;">
                        <span>{status_color} {ticket.get('status', 'Open')}</span>
                        <span>{priority_icon} {ticket.get('priority', 'Medium')} Priority</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📌 No tickets or complaints yet. Create one using the button above.")
