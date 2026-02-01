"""
Student Dashboard Page
Displays student dashboard with various features
"""

import streamlit as st
from modules.database import (
    get_user_profile, update_user_profile, 
    get_service_requests, create_service_request,
    get_tickets, create_ticket
)

def show_student_page(page, user_id):
    """Display student dashboard based on selected page"""
    
    if page == "Profile":
        show_profile(user_id)
    elif page == "Service Requests":
        show_student_requests(user_id)
    elif page == "Tickets":
        show_student_tickets(user_id)
    elif "Analytics" in page:
        from modules.analytics import show_performance_dashboard
        st.markdown("## 📊 Performance Analytics")
        show_performance_dashboard(user_id)
    elif "Document" in page:
        from modules.documents import show_document_manager
        st.markdown("## 📄 My Documents")
        show_document_manager(user_id)
    elif "Attendance" in page:
        from modules.attendance import show_attendance_tracker
        st.markdown("## 📋 My Attendance")
        show_attendance_tracker(user_id)
    elif "Exam" in page:
        from modules.exams import show_exam_results
        st.markdown("## 📝 My Exam Results")
        show_exam_results(user_id)
    elif "GPA" in page:
        from modules.gpa import show_gpa_calculator
        st.markdown("## 🎯 GPA Calculator")
        show_gpa_calculator(user_id)
    elif "Export" in page:
        from modules.export import show_data_export
        st.markdown("## 📥 Export My Data")
        show_data_export(user_id)
    elif "Notification" in page:
        from modules.notifications import show_notifications
        st.markdown("## 🔔 My Notifications")
        show_notifications(user_id)
    elif "Search" in page:
        from modules.search import show_advanced_search
        st.markdown("## 🔍 Advanced Search")
        show_advanced_search(user_id)
    elif "Fee" in page:
        from modules.fees import show_fee_management
        st.markdown("## 💰 My Fee Details")
        show_fee_management(user_id)

def show_profile(user_id):
    """Display and edit student profile"""
    st.markdown("## 👤 My Profile")
    
    profile = get_user_profile(user_id)
    
    if profile:
        # Display current info
        st.markdown("### Current Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Name:** {profile['full_name']}")
            st.info(f"**Email:** {profile['email']}")
            st.info(f"**Phone:** {profile['phone']}")
        
        with col2:
            st.info(f"**Course:** {profile['course']}")
            st.info(f"**Semester:** {profile['semester']}")
            st.info(f"**Roll No:** {profile['roll_number']}")
        
        # Edit form
        st.markdown("---")
        st.markdown("### Update Profile")
        
        with st.form("profile_form"):
            full_name = st.text_input("Full Name", value=profile['full_name'])
            email = st.text_input("Email", value=profile['email'])
            phone = st.text_input("Phone", value=profile['phone'])
            course = st.text_input("Course", value=profile['course'])
            semester = st.number_input("Semester", min_value=1, max_value=8, value=profile['semester'])
            roll_number = st.text_input("Roll Number", value=profile['roll_number'])
            
            submitted = st.form_submit_button("Update Profile")
            
            if submitted:
                if update_user_profile(user_id, full_name, email, phone, course, semester, roll_number):
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
                if create_service_request(user_id, request_type, description):
                    st.success("✅ Request submitted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to submit request")
    
    # Display existing requests
    st.markdown("### My Requests")
    requests = get_service_requests(user_id=user_id)
    
    if requests:
        for req in requests:
            status_color = {
                "Pending": "🟡",
                "Approved": "🟢",
                "Rejected": "🔴",
                "In Progress": "🔵"
            }.get(req['status'], "⚪")
            
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
                st.markdown("---")
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
                if create_ticket(user_id, subject, description, category, priority):
                    st.success("✅ Ticket created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to create ticket")
    
    # Display existing tickets
    st.markdown("### My Tickets")
    tickets = get_tickets(user_id=user_id)
    
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
                st.markdown("---")
    else:
        st.info("No support tickets yet")
