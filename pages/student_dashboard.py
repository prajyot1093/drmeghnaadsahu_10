"""
Student Dashboard Page
Displays student dashboard with various features
"""

import streamlit as st
from modules.database import (
    get_student_profile, update_student_profile, 
    get_user_requests, submit_service_request,
    get_user_tickets, submit_ticket
)

def show_student_page(page, user_id):
    """Display student dashboard based on selected page"""
    
    if page == "Dashboard":
        show_dashboard_home(user_id)
    elif page == "Profile":
        show_profile(user_id)
    elif page == "Service Requests":
        show_student_requests(user_id)
    elif page == "Tickets":
        show_student_tickets(user_id)
    elif "Analytics" in page:
        from modules.analytics import show_performance_dashboard
        st.markdown("## 📊 Performance Analytics")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Track your academic performance and progress over time</p>", unsafe_allow_html=True)
        show_performance_dashboard(user_id)
    elif "Document" in page:
        from modules.documents import show_document_manager
        st.markdown("## 📄 My Documents")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Manage and access your important documents</p>", unsafe_allow_html=True)
        show_document_manager(user_id)
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
    elif "GPA" in page:
        from modules.gpa import show_gpa_calculator
        st.markdown("## 🎯 GPA Calculator")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Calculate your Grade Point Average</p>", unsafe_allow_html=True)
        show_gpa_calculator(user_id)
    elif "Export" in page:
        from modules.export import show_data_export
        st.markdown("## 📥 Export My Data")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Download your data in various formats</p>", unsafe_allow_html=True)
        show_data_export(user_id)
    elif "Notification" in page:
        from modules.notifications import show_notifications
        st.markdown("## 🔔 My Notifications")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Stay updated with important alerts</p>", unsafe_allow_html=True)
        show_notifications(user_id)
    elif "Search" in page:
        from modules.search import show_advanced_search
        st.markdown("## 🔍 Advanced Search")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Search through all your academic records</p>", unsafe_allow_html=True)
        show_advanced_search(user_id)
    elif "Fee" in page:
        from modules.fees import show_fee_management
        st.markdown("## 💰 My Fee Details")
        st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>View and manage your fee payments</p>", unsafe_allow_html=True)
        show_fee_management(user_id)

def show_dashboard_home(user_id):
    """Show student dashboard home page"""
    profile = get_student_profile(user_id)
    
    if profile:
        # Welcome header
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, var(--accent), var(--accent-hover)); 
                        padding: 2rem; border-radius: var(--radius-lg); margin-bottom: 2rem; color: white;">
                <h1 style="color: white; margin: 0 0 0.5rem 0;">Welcome back, {profile['full_name']}! 👋</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 0;">Here's your academic overview</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Semester", profile['semester'], delta="Current")
        with col2:
            st.metric("Course", profile['course'][:15])
        with col3:
            requests = get_user_requests(user_id)
            st.metric("My Requests", len(requests) if requests else 0)
        with col4:
            tickets = get_user_tickets(user_id)
            st.metric("My Tickets", len(tickets) if tickets else 0)
        
        st.divider()
        
        # Recent activity
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📋 Recent Requests")
            requests = get_user_requests(user_id)
            if requests and len(requests) > 0:
                for req in requests[:3]:
                    st.markdown(f"""
                        <div style="background: var(--surface); padding: 1rem; border-radius: var(--radius); 
                                    border-left: 4px solid var(--accent); margin-bottom: 0.75rem;">
                            <div style="font-weight: 600; color: var(--text-primary);">{req['request_type']}</div>
                            <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem;">
                                {req['status']} • {req['created_at'][:10]}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent requests")
        
        with col2:
            st.markdown("### 🎫 Recent Tickets")
            tickets = get_user_tickets(user_id)
            if tickets and len(tickets) > 0:
                for ticket in tickets[:3]:
                    st.markdown(f"""
                        <div style="background: var(--surface); padding: 1rem; border-radius: var(--radius); 
                                    border-left: 4px solid var(--warning); margin-bottom: 0.75rem;">
                            <div style="font-weight: 600; color: var(--text-primary);">{ticket['subject']}</div>
                            <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem;">
                                {ticket['status']} • Priority: {ticket['priority']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent tickets")
    else:
        st.error("Profile not found")

def show_profile(user_id):
    """Display and edit student profile"""
    st.markdown("## 👤 My Profile")
    st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>View and update your personal information</p>", unsafe_allow_html=True)
    
    profile = get_student_profile(user_id)
    
    if profile:
        # Display current info with modern cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style="background: var(--surface); padding: 1.5rem; border-radius: var(--radius-lg); 
                            border: 1px solid var(--border); margin-bottom: 1rem;">
                    <h4 style="margin: 0 0 1rem 0; color: var(--text-primary);">Personal Information</h4>
            """, unsafe_allow_html=True)
            st.markdown(f"**Full Name:** {profile['full_name']}")
            st.markdown(f"**Email:** {profile['email']}")
            st.markdown(f"**Phone:** {profile['phone']}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style="background: var(--surface); padding: 1.5rem; border-radius: var(--radius-lg); 
                            border: 1px solid var(--border); margin-bottom: 1rem;">
                    <h4 style="margin: 0 0 1rem 0; color: var(--text-primary);">Academic Details</h4>
            """, unsafe_allow_html=True)
            st.markdown(f"**Course:** {profile['course']}")
            st.markdown(f"**Semester:** {profile['semester']}")
            st.markdown(f"**Roll Number:** {profile['roll_number']}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # Edit form with better styling
        st.markdown("### ✏️ Update Profile")
        
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name", value=profile['full_name'])
                email = st.text_input("Email Address", value=profile['email'])
                phone = st.text_input("Phone Number", value=profile['phone'])
            
            with col2:
                course = st.text_input("Course", value=profile['course'])
                semester = st.number_input("Semester", min_value=1, max_value=8, value=profile['semester'])
                roll_number = st.text_input("Roll Number", value=profile['roll_number'])
            
            submitted = st.form_submit_button("💾 Update Profile", use_container_width=True, type="primary")
            
            if submitted:
                profile_data = {
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                    'course': course,
                    'semester': semester,
                    'roll_number': roll_number
                }
                if update_student_profile(user_id, profile_data):
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update profile")
    else:
        st.error("Profile not found")

def show_student_requests(user_id):
    """Display and manage service requests"""
    st.markdown("## 📋 My Service Requests")
    
    # Create new request
    with st.expander("➕ Create New Request", expanded=False):
        with st.form("request_form"):
            request_type = st.selectbox(
                "Request Type",
                ["Bonafide Certificate", "Transfer Certificate", "Fee Receipt", 
                 "ID Card", "Library Card", "Other"]
            )
            description = st.text_area("Description", height=100)
            submitted = st.form_submit_button("Submit Request")
            
            if submitted and description:
                if submit_service_request(user_id, request_type, description):
                    st.success("✅ Request submitted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to submit request")
    
    # Display existing requests
    st.markdown("### 📋 My Requests")
    requests = get_user_requests(user_id)
    
    if requests:
        for req in requests:
            status_color = {
                "Pending": "🟡",
                "Approved": "🟢",
                "Rejected": "🔴",
                "In Progress": "🔵"
            }.get(req['status'], "⚪")
            
            # Add styled container for each request
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                     padding: 1.25rem; border-radius: 0.75rem; 
                     border: 2px solid #e2e8f0; border-left: 5px solid #2563eb;
                     box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;">
            """, unsafe_allow_html=True)
            
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{req['request_type']}**")
                    st.caption(req['description'][:100])
                with col2:
                    st.caption(f"Created: {req['created_at'][:10]}")
                with col3:
                    st.markdown(f"{status_color} {req['status']}")
                
                if req['admin_remarks']:
                    st.info(f"💬 Admin: {req['admin_remarks']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No service requests yet")

def show_student_tickets(user_id):
    """Display and manage support tickets"""
    st.markdown("## 🎫 My Support Tickets")
    
    # Create new ticket
    with st.expander("➕ Create New Ticket", expanded=False):
        with st.form("ticket_form"):
            subject = st.text_input("Subject")
            category = st.selectbox(
                "Category",
                ["Technical Issue", "Academic Query", "Fee Related", 
                 "Admission", "Hostel", "Library", "Other"]
            )
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            description = st.text_area("Description", height=150)
            submitted = st.form_submit_button("Submit Ticket")
            
            if submitted and subject and description:
                if submit_ticket(user_id, subject, description, category, priority):
                    st.success("✅ Ticket created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to create ticket")
    
    # Display existing tickets
    st.markdown("### 🎫 My Tickets")
    tickets = get_user_tickets(user_id)
    
    if tickets:
        for ticket in tickets:
            status_color = {
                "Open": "🔵",
                "In Progress": "🟡",
                "Resolved": "🟢",
                "Closed": "⚫"
            }.get(ticket['status'], "⚪")
            
            priority_icon = {
                "Low": "🟢",
                "Medium": "🟡",
                "High": "🔴"
            }.get(ticket['priority'], "⚪")
            
            # Add styled container for each ticket
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #fef3c7 5%, #ffffff 100%);
                     padding: 1.25rem; border-radius: 0.75rem;
                     border: 2px solid #e2e8f0; border-left: 5px solid #f59e0b;
                     box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;">
            """, unsafe_allow_html=True)
            
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{ticket['subject']}**")
                    st.caption(f"🏷️ {ticket['category']}")
                with col2:
                    st.caption(f"Created: {ticket['created_at'][:10]}")
                    st.caption(f"{priority_icon} {ticket['priority']} Priority")
                with col3:
                    st.markdown(f"{status_color} {ticket['status']}")
                
                with st.expander("View Details"):
                    st.markdown(f"**Description:** {ticket['description']}")
                    if ticket['admin_response']:
                        st.info(f"💬 Response: {ticket['admin_response']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No support tickets yet")
