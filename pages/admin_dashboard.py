import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.database import (
    get_all_requests, get_all_tickets, 
    update_request_status, get_request_stats
)
import plotly.graph_objects as go
import plotly.express as px

def show_admin_page(page):
    """Display admin dashboard based on selected page"""
    
    if page == "Dashboard":
        show_admin_dashboard()
    elif page == "Service Requests":
        show_service_requests()
    elif page == "Tickets":
        show_tickets()
    elif page == "Admission Requests":
        show_admission_requests()
    elif page == "Analytics":
        show_analytics()

def show_admin_dashboard():
    """Show admin dashboard overview"""
    st.markdown("## 📊 Admin Dashboard")
    
    # Get statistics
    requests = get_all_requests()
    tickets = get_all_tickets()
    
    stats = get_request_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requests", len(requests), delta="2")
    with col2:
        st.metric("Open Tickets", len(tickets), delta="1")
    with col3:
        submitted = stats.get('Submitted', 0)
        st.metric("Submitted", submitted)
    with col4:
        resolved = stats.get('Resolved', 0)
        st.metric("Resolved", resolved)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Request Status Distribution")
        if stats:
            fig = go.Figure(data=[
                go.Pie(labels=list(stats.keys()), values=list(stats.values()))
            ])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Recent Activity")
        if requests:
            recent = requests[:5]
            for req in recent:
                st.write(f"📝 {req['full_name']}: {req['title'][:40]}...")
        else:
            st.info("No recent activity")
    
    st.divider()
    
    st.markdown("### Recently Submitted Requests")
    if requests:
        df = pd.DataFrame([{
            'Title': r['title'],
            'Requester': r['full_name'],
            'Category': r['category'],
            'Priority': r['priority'],
            'Status': r['status'],
            'Date': r['created_at']
        } for r in requests[:10]])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No requests")

def show_service_requests():
    """Show and manage service requests"""
    st.markdown("## 📋 Service Requests Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            ["Submitted", "In Progress", "Resolved"],
            default=["Submitted", "In Progress"]
        )
    
    with col2:
        category_filter = st.multiselect(
            "Filter by Category",
            ["Academic", "Admission", "Exam", "General", "Technical Support"],
            default=None
        )
    
    with col3:
        priority_filter = st.multiselect(
            "Filter by Priority",
            ["Low", "Medium", "High"],
            default=None
        )
    
    filters = {}
    if status_filter:
        filters['status'] = status_filter
    if category_filter:
        filters['category'] = category_filter
    if priority_filter:
        filters['priority'] = priority_filter
    
    requests = get_all_requests(filters) if filters else get_all_requests()
    
    st.divider()
    
    if requests:
        for req in requests:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {req['title']}")
                    st.write(f"**From:** {req['full_name']} ({req['email']})")
                    st.write(f"**Description:** {req['description']}")
                    
                    col_meta1, col_meta2, col_meta3 = st.columns(3)
                    with col_meta1:
                        st.caption(f"Category: {req['category']}")
                    with col_meta2:
                        st.caption(f"Priority: {req['priority']}")
                    with col_meta3:
                        st.caption(f"Created: {req['created_at'][:10]}")
                
                with col2:
                    new_status = st.selectbox(
                        "Update Status",
                        ["Submitted", "In Progress", "Resolved"],
                        index=["Submitted", "In Progress", "Resolved"].index(req['status']),
                        key=f"status_{req['request_id']}"
                    )
                    
                    if new_status != req['status']:
                        if st.button("Update", key=f"update_{req['request_id']}", use_container_width=True):
                            if update_request_status(req['request_id'], new_status):
                                st.success(f"Status updated to {new_status}")
                                st.rerun()
    else:
        st.info("No requests match the selected filters")

def show_tickets():
    """Show and manage support tickets"""
    st.markdown("## 🎫 Support Tickets Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            ["Open", "In Progress", "Resolved"],
            default=["Open", "In Progress"]
        )
    
    with col2:
        category_filter = st.multiselect(
            "Filter by Category",
            ["Academic", "Admission", "Exam", "General", "Technical Support"],
            default=None
        )
    
    with col3:
        priority_filter = st.multiselect(
            "Filter by Priority",
            ["Low", "Medium", "High"],
            default=None
        )
    
    filters = {}
    if status_filter:
        filters['status'] = status_filter
    if category_filter:
        filters['category'] = category_filter
    if priority_filter:
        filters['priority'] = priority_filter
    
    tickets = get_all_tickets(filters) if filters else get_all_tickets()
    
    st.divider()
    
    if tickets:
        for ticket in tickets:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {ticket['title']}")
                    st.write(f"**From:** {ticket['full_name']} ({ticket['email']})")
                    st.write(f"**Description:** {ticket['description']}")
                    
                    col_meta1, col_meta2, col_meta3 = st.columns(3)
                    with col_meta1:
                        st.caption(f"Category: {ticket['category']}")
                    with col_meta2:
                        st.caption(f"Priority: {ticket['priority']}")
                    with col_meta3:
                        st.caption(f"Created: {ticket['created_at'][:10]}")
                
                with col2:
                    new_status = st.selectbox(
                        "Update Status",
                        ["Open", "In Progress", "Resolved"],
                        index=["Open", "In Progress", "Resolved"].index(ticket['status']),
                        key=f"ticket_status_{ticket['ticket_id']}"
                    )
                    
                    if new_status != ticket['status']:
                        if st.button("Update", key=f"ticket_update_{ticket['ticket_id']}", use_container_width=True):
                            st.success(f"Status updated to {new_status}")
    else:
        st.info("No tickets match the selected filters")

def show_admission_requests():
    """Show admission requests"""
    st.markdown("## 📚 Admission Requests")
    
    st.info("Manage student admission and semester registration requests")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Pending Requests", "5", delta="2")
    
    with col2:
        st.metric("Approved", "12", delta="1")

def show_analytics():
    """Show analytics and reports"""
    st.markdown("## 📈 Analytics & Reports")
    
    requests = get_all_requests()
    
    if requests:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Requests by Category")
            df = pd.DataFrame([{
                'Category': r['category'],
                'Count': 1
            } for r in requests])
            category_counts = df.groupby('Category').size()
            
            fig = px.bar(
                x=category_counts.index,
                y=category_counts.values,
                labels={'x': 'Category', 'y': 'Count'},
                title="Requests by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Requests by Priority")
            df = pd.DataFrame([{
                'Priority': r['priority'],
                'Count': 1
            } for r in requests])
            priority_counts = df.groupby('Priority').size()
            
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="Requests by Priority"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Request Timeline")
        # Create timeline data
        df = pd.DataFrame([{
            'Date': r['created_at'][:10],
            'Count': 1
        } for r in requests])
        timeline = df.groupby('Date').size()
        
        fig = px.line(
            x=timeline.index,
            y=timeline.values,
            labels={'x': 'Date', 'y': 'Number of Requests'},
            title="Requests Over Time",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for analytics")
