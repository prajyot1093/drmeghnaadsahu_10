import streamlit as st
import pandas as pd
from modules.database import get_db_connection

def search_records(user_id, query, search_type="all"):
    """Search across records"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            results = {}
            
            if search_type in ["all", "requests"]:
                cursor.execute("""
                    SELECT id, title, status, created_at FROM service_requests
                    WHERE user_id = ? AND (title LIKE ? OR description LIKE ?)
                    ORDER BY created_at DESC LIMIT 10
                """, (user_id, f"%{query}%", f"%{query}%"))
                requests = cursor.fetchall()
                if requests:
                    results['Service Requests'] = pd.DataFrame(requests, columns=['ID', 'Title', 'Status', 'Date'])
            
            if search_type in ["all", "tickets"]:
                cursor.execute("""
                    SELECT id, category, status, created_at FROM tickets
                    WHERE user_id = ? AND (category LIKE ? OR title LIKE ?)
                    ORDER BY created_at DESC LIMIT 10
                """, (user_id, f"%{query}%", f"%{query}%"))
                tickets = cursor.fetchall()
                if tickets:
                    results['Support Tickets'] = pd.DataFrame(tickets, columns=['ID', 'Category', 'Status', 'Date'])
            
            if search_type in ["all", "results"]:
                cursor.execute("""
                    SELECT id, exam_name, subject, percentage, grade FROM exam_results
                    WHERE user_id = ? AND (exam_name LIKE ? OR subject LIKE ?)
                    ORDER BY exam_date DESC LIMIT 10
                """, (user_id, f"%{query}%", f"%{query}%"))
                exams = cursor.fetchall()
                if exams:
                    results['Exam Results'] = pd.DataFrame(exams, columns=['ID', 'Exam', 'Subject', 'Percentage', 'Grade'])
            
            return results
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
        return {}

def filter_by_status(user_id, data_type, status):
    """Filter records by status"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if data_type == "requests":
                cursor.execute("""
                    SELECT id, title, status, created_at FROM service_requests
                    WHERE user_id = ? AND status = ? ORDER BY created_at DESC
                """, (user_id, status))
            elif data_type == "tickets":
                cursor.execute("""
                    SELECT id, category, status, created_at FROM tickets
                    WHERE user_id = ? AND status = ? ORDER BY created_at DESC
                """, (user_id, status))
            
            results = cursor.fetchall()
            return results
    except:
        return []

def show_advanced_search(user_id):
    """Display advanced search UI"""
    st.markdown("### 🔍 Advanced Search & Filter")
    
    # Search section
    st.subheader("Search")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search across all records")
    with col2:
        search_type = st.selectbox("Type", ["All", "Requests", "Tickets", "Results"])
    
    if search_query:
        search_type_map = {
            "All": "all",
            "Requests": "requests",
            "Tickets": "tickets",
            "Results": "results"
        }
        results = search_records(user_id, search_query, search_type_map[search_type])
        
        if results:
            for category, df in results.items():
                st.subheader(category)
                st.dataframe(df, use_container_width=True)
        else:
            st.info("No results found")
    
    st.divider()
    
    # Filter section
    st.subheader("Filter by Status")
    
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox("Filter by", ["Service Requests", "Support Tickets"])
    with col2:
        if filter_type == "Service Requests":
            status = st.selectbox("Status", ["Submitted", "In Progress", "Resolved"], key="req_status")
        else:
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved"], key="ticket_status")
    
    if st.button("Apply Filter", use_container_width=True):
        filter_type_map = {
            "Service Requests": "requests",
            "Support Tickets": "tickets"
        }
        results = filter_by_status(user_id, filter_type_map[filter_type], status)
        
        if results:
            st.subheader(f"{filter_type} - {status}")
            if filter_type == "Service Requests":
                df = pd.DataFrame(results, columns=['ID', 'Title', 'Status', 'Date'])
            else:
                df = pd.DataFrame(results, columns=['ID', 'Category', 'Status', 'Date'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f"No {filter_type.lower()} with status '{status}'")
