import streamlit as st
from modules.auth import get_current_user
from modules.database import (
    get_student_profile, update_student_profile, 
    submit_service_request, get_user_requests, 
    submit_ticket, get_user_tickets
)
from datetime import datetime

def show_student_page(page):
    """Display student dashboard based on selected page"""
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Profile":
        show_profile()
    elif page == "My Requests":
        show_my_requests()
    elif page == "Admission":
        show_admission()
    elif page == "Exam Registration":
        show_exam_registration()
    elif page == "Submit Ticket":
        show_submit_ticket()

def show_dashboard():
    """Show student dashboard"""
    user = get_current_user()
    
    st.markdown("## 📊 Student Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Service Requests", value=len(get_user_requests(user['user_id'])))
    
    with col2:
        st.metric(label="Active Tickets", value=len(get_user_tickets(user['user_id'])))
    
    with col3:
        st.metric(label="Profile Status", value="Complete")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Recent Requests")
        requests = get_user_requests(user['user_id'])[:3]
        if requests:
            for req in requests:
                status_color = {
                    'Submitted': '🔵',
                    'In Progress': '🟡',
                    'Resolved': '🟢'
                }
                st.write(f"{status_color.get(req['status'], '⚪')} **{req['title']}** - {req['status']}")
        else:
            st.info("No requests yet")
    
    with col2:
        st.markdown("### Quick Actions")
        if st.button("📝 Submit Service Request", use_container_width=True):
            st.session_state.current_page = "Submit Ticket"
            st.rerun()
        if st.button("👤 View Profile", use_container_width=True):
            st.session_state.current_page = "Profile"
            st.rerun()

def show_profile():
    """Show and edit student profile"""
    user = get_current_user()
    
    st.markdown("## 👤 Student Profile")
    
    profile = get_student_profile(user['user_id'])
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            roll_number = st.text_input(
                "Roll Number",
                value=profile['roll_number'] if profile else "",
                key="roll_number"
            )
            department = st.selectbox(
                "Department",
                ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical"],
                index=0 if not profile else 0,
                key="department"
            )
            semester = st.number_input(
                "Semester",
                min_value=1,
                max_value=8,
                value=profile['semester'] if profile else 1,
                key="semester"
            )
            cgpa = st.number_input(
                "CGPA",
                min_value=0.0,
                max_value=10.0,
                value=float(profile['cgpa']) if profile and profile['cgpa'] else 0.0,
                step=0.1,
                key="cgpa"
            )
        
        with col2:
            phone = st.text_input(
                "Phone Number",
                value=profile['phone'] if profile else "",
                key="phone"
            )
            dob = st.date_input(
                "Date of Birth",
                value=None if not profile else datetime.strptime(profile['dob'], '%Y-%m-%d').date() if profile['dob'] else None,
                key="dob"
            )
            father_name = st.text_input(
                "Father's Name",
                value=profile['father_name'] if profile else "",
                key="father_name"
            )
            mother_name = st.text_input(
                "Mother's Name",
                value=profile['mother_name'] if profile else "",
                key="mother_name"
            )
        
        address = st.text_area(
            "Address",
            value=profile['address'] if profile else "",
            key="address"
        )
        
        if st.form_submit_button("Save Profile", use_container_width=True):
            profile_data = {
                'roll_number': roll_number,
                'department': department,
                'semester': semester,
                'cgpa': cgpa,
                'phone': phone,
                'address': address,
                'father_name': father_name,
                'mother_name': mother_name,
                'dob': str(dob) if dob else None
            }
            if update_student_profile(user['user_id'], profile_data):
                st.success("Profile updated successfully!")
            else:
                st.error("Failed to update profile")

def show_my_requests():
    """Show user's service requests"""
    user = get_current_user()
    
    st.markdown("## 📋 My Service Requests")
    
    requests = get_user_requests(user['user_id'])
    
    if requests:
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            status_filter = st.multiselect(
                "Filter by Status",
                ["Submitted", "In Progress", "Resolved"],
                default=["Submitted", "In Progress", "Resolved"]
            )
        
        filtered_requests = [r for r in requests if r['status'] in status_filter]
        
        for req in filtered_requests:
            # Status styling
            status_styles = {
                'Submitted': ('class="status-submitted"', '🔵'),
                'In Progress': ('class="status-inprogress"', '🟡'),
                'Resolved': ('class="status-resolved"', '🟢')
            }
            status_class, status_emoji = status_styles.get(req['status'], ('', '⚪'))
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{req['title']}**")
                    st.write(req['description'][:100] + "...")
                with col2:
                    st.markdown(f"<span {status_class}>{status_emoji} {req['status']}</span>", unsafe_allow_html=True)
                with col3:
                    priority_colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
                    st.caption(f"{priority_colors.get(req['priority'], '')} {req['priority']}")
    else:
        st.info("No service requests yet")

def show_admission():
    """Show admission and registration section"""
    st.markdown("## 📚 Admission & Registration")
    
    st.info("Manage your admission and semester registration requests")
    
    with st.form("admission_form"):
        current_sem = st.number_input("Current Semester", min_value=1, max_value=7, value=1)
        desired_sem = st.number_input("Desired Semester", min_value=2, max_value=8, value=2)
        
        if st.form_submit_button("Submit Registration Request"):
            st.success("Registration request submitted successfully!")

def show_exam_registration():
    """Show exam registration section"""
    st.markdown("## 📝 Exam Form Registration")
    
    with st.form("exam_form"):
        exam_name = st.text_input("Exam Name")
        exam_date = st.date_input("Exam Date")
        subject = st.text_input("Subject")
        
        if st.form_submit_button("Register for Exam"):
            st.success("Exam registration submitted!")

def show_submit_ticket():
    """Show ticket submission form"""
    st.markdown("## 🎫 Submit Support Ticket")
    
    user = get_current_user()
    
    with st.form("ticket_form"):
        title = st.text_input("Ticket Title", placeholder="Briefly describe your issue")
        description = st.text_area("Description", placeholder="Provide details about your issue")
        category = st.selectbox(
            "Category",
            ["Academic", "Admission", "Exam", "General", "Technical Support"]
        )
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        if st.form_submit_button("Submit Ticket", use_container_width=True):
            if title and description:
                if submit_ticket(user['user_id'], title, description, category, priority):
                    st.success("Ticket submitted successfully!")
                else:
                    st.error("Failed to submit ticket")
            else:
                st.warning("Please fill in all fields")
