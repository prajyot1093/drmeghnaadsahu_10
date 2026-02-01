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
    
    # Safety check for user
    if not user or not user['user_id']:
        st.error("❌ User session expired. Please login again.")
        return
    
    st.markdown("## 📊 Student Dashboard")
    
    try:
        user_requests = get_user_requests(user['user_id']) or []
        user_tickets = get_user_tickets(user['user_id']) or []
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Service Requests", value=len(user_requests))
        
        with col2:
            st.metric(label="Active Tickets", value=len(user_tickets))
        
        with col3:
            st.metric(label="Profile Status", value="Complete")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Recent Requests")
            requests = user_requests[:3]
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
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")
        print(f"Dashboard error: {e}")

def show_profile():
    """Show and edit student profile"""
    user = get_current_user()
    
    # Safety check for user
    if not user or not user['user_id']:
        st.error("❌ User session expired. Please login again.")
        return
    
    st.markdown("## 👤 Student Profile")
    
    try:
        profile = get_student_profile(user['user_id'])
        
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                roll_number = st.text_input(
                    "Roll Number",
                    value=profile['roll_number'] if profile and profile.get('roll_number') else "",
                    key="roll_number"
                )
                department = st.selectbox(
                    "Department",
                    ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical"],
                    index=0,
                    key="department"
                )
                semester = st.number_input(
                    "Semester",
                    min_value=1,
                    max_value=8,
                    value=profile['semester'] if profile and profile.get('semester') else 1,
                    key="semester"
                )
                cgpa = st.number_input(
                    "CGPA",
                    min_value=0.0,
                    max_value=10.0,
                    value=float(profile['cgpa']) if profile and profile.get('cgpa') else 0.0,
                    step=0.1,
                    key="cgpa"
                )
            
            with col2:
                phone = st.text_input(
                    "Phone Number",
                    value=profile['phone'] if profile and profile.get('phone') else "",
                    key="phone"
                )
                
                # Safely parse date
                dob_value = None
                if profile and profile.get('dob'):
                    try:
                        dob_value = datetime.strptime(profile['dob'], '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        dob_value = None
                
                dob = st.date_input(
                    "Date of Birth",
                    value=dob_value,
                    key="dob"
                )
                
                father_name = st.text_input(
                    "Father's Name",
                    value=profile['father_name'] if profile and profile.get('father_name') else "",
                    key="father_name"
                )
                mother_name = st.text_input(
                    "Mother's Name",
                    value=profile['mother_name'] if profile and profile.get('mother_name') else "",
                    key="mother_name"
                )
            
            address = st.text_area(
                "Address",
                value=profile['address'] if profile and profile.get('address') else "",
                key="address"
            )
            
            if st.form_submit_button("Save Profile", use_container_width=True):
                # Validate required fields
                if not roll_number.strip():
                    st.error("❌ Roll number is required")
                elif not phone.strip() or len(phone.strip()) < 10:
                    st.error("❌ Valid phone number is required (at least 10 digits)")
                else:
                    profile_data = {
                        'roll_number': roll_number.strip(),
                        'department': department,
                        'semester': semester,
                        'cgpa': cgpa,
                        'phone': phone.strip(),
                        'address': address.strip(),
                        'father_name': father_name.strip(),
                        'mother_name': mother_name.strip(),
                        'dob': str(dob) if dob else None
                    }
                    if update_student_profile(user['user_id'], profile_data):
                        st.success("✅ Profile updated successfully!")
                    else:
                        st.error("❌ Failed to update profile")
    except Exception as e:
        st.error(f"❌ Error loading profile: {str(e)}")
        print(f"Profile error: {e}")

def show_my_requests():
    """Show user's service requests"""
    user = get_current_user()
    
    # Safety check for user
    if not user or not user['user_id']:
        st.error("❌ User session expired. Please login again.")
        return
    
    st.markdown("## 📋 My Service Requests")
    
    try:
        requests = get_user_requests(user['user_id']) or []
        
        if requests:
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                status_filter = st.multiselect(
                    "Filter by Status",
                    ["Submitted", "In Progress", "Resolved"],
                    default=["Submitted", "In Progress", "Resolved"]
                )
            
            filtered_requests = [r for r in requests if r['status'] in status_filter]
            
            if filtered_requests:
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
                            desc = req.get('description', '')[:100]
                            st.write(desc + ("..." if len(desc) == 100 else ""))
                        with col2:
                            st.markdown(f"<span {status_class}>{status_emoji} {req['status']}</span>", unsafe_allow_html=True)
                        with col3:
                            priority_colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
                            st.caption(f"{priority_colors.get(req['priority'], '')} {req['priority']}")
            else:
                st.info("No requests match the selected filters")
        else:
            st.info("No service requests yet")
    except Exception as e:
        st.error(f"❌ Error loading requests: {str(e)}")
        print(f"Requests error: {e}")

def show_admission():
    """Show admission and registration section"""
    st.markdown("## 📚 Admission & Registration")
    
    st.info("Manage your admission and semester registration requests")
    
    user = get_current_user()
    if not user or not user['user_id']:
        st.error("❌ User session expired. Please login again.")
        return
    
    with st.form("admission_form"):
        current_sem = st.number_input("Current Semester", min_value=1, max_value=7, value=1)
        desired_sem = st.number_input("Desired Semester", min_value=2, max_value=8, value=2)
        
        if st.form_submit_button("Submit Registration Request"):
            if desired_sem <= current_sem:
                st.error("❌ Desired semester must be higher than current semester")
            else:
                st.success("✅ Registration request submitted successfully!")

def show_exam_registration():
    """Show exam registration section"""
    st.markdown("## 📝 Exam Form Registration")
    
    user = get_current_user()
    if not user or not user['user_id']:
        st.error("❌ User session expired. Please login again.")
        return
    
    with st.form("exam_form"):
        exam_name = st.text_input("Exam Name", placeholder="e.g., Midterm Exam")
        exam_date = st.date_input("Exam Date")
        subject = st.text_input("Subject", placeholder="e.g., Mathematics")
        
        if st.form_submit_button("Register for Exam"):
            if not exam_name.strip() or not subject.strip():
                st.error("❌ Exam name and subject are required")
            else:
                st.success("✅ Exam registration submitted!")

def show_submit_ticket():
    """Show ticket submission form"""
    st.markdown("## 🎫 Submit Support Ticket")
    
    user = get_current_user()
    
    # Safety check for user
    if not user or not user['user_id']:
        st.error("❌ User session expired. Please login again.")
        return
    
    try:
        with st.form("ticket_form"):
            title = st.text_input("Ticket Title", placeholder="Briefly describe your issue")
            description = st.text_area("Description", placeholder="Provide details about your issue", min_chars=10)
            category = st.selectbox(
                "Category",
                ["Academic", "Admission", "Exam", "General", "Technical Support"]
            )
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            
            if st.form_submit_button("Submit Ticket", use_container_width=True):
                # Validate inputs
                if not title.strip():
                    st.error("❌ Ticket title is required")
                elif len(title.strip()) < 5:
                    st.error("❌ Ticket title must be at least 5 characters")
                elif not description.strip():
                    st.error("❌ Description is required")
                elif len(description.strip()) < 10:
                    st.error("❌ Description must be at least 10 characters")
                else:
                    if submit_ticket(user['user_id'], title, description, category, priority):
                        st.success("✅ Ticket submitted successfully! We'll get back to you soon.")
                    else:
                        st.error("❌ Failed to submit ticket. Please try again.")
    except Exception as e:
        st.error(f"❌ Error submitting ticket: {str(e)}")
        print(f"Ticket submission error: {e}")
