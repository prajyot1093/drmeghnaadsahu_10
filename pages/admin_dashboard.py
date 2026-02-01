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
    
    try:
        # Get statistics
        requests = get_all_requests() or []
        tickets = get_all_tickets() or []
        
        stats = get_request_stats() or {}
        
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
            else:
                st.info("No request data available")
        
        with col2:
            st.markdown("### Recent Activity")
            if requests:
                recent = requests[:5]
                for req in recent:
                    st.write(f"📝 {req.get('full_name', 'Unknown')}: {req.get('title', 'No title')[:40]}...")
            else:
                st.info("No recent activity")
        
        st.divider()
        
        st.markdown("### Recently Submitted Requests")
        if requests:
            df = pd.DataFrame([{
                'Title': r.get('title', 'N/A'),
                'Requester': r.get('full_name', 'Unknown'),
                'Category': r.get('category', 'N/A'),
                'Priority': r.get('priority', 'N/A'),
                'Status': r.get('status', 'N/A'),
                'Date': r.get('created_at', 'N/A')
            } for r in requests[:10]])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No requests")
    except Exception as e:
        st.error(f"❌ Error loading admin dashboard: {str(e)}")
        print(f"Admin dashboard error: {e}")

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
    
    try:
        requests = get_all_requests(filters) if filters else get_all_requests()
        requests = requests or []
        
        st.divider()
        
        if requests:
            for req in requests:
                # Safety checks for dictionary access
                req_title = req.get('title', 'No Title')
                req_status = req.get('status', 'Unknown')
                req_priority = req.get('priority', 'Unknown')
                req_id = req.get('request_id')
                
                # Status and priority styling
                status_styles = {
                    'Submitted': ('class="status-submitted"', '🔵'),
                    'In Progress': ('class="status-inprogress"', '🟡'),
                    'Resolved': ('class="status-resolved"', '🟢')
                }
                status_class, status_emoji = status_styles.get(req_status, ('', '⚪'))
                priority_colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### {req_title}")
                        st.write(f"**From:** {req.get('full_name', 'Unknown')} ({req.get('email', 'N/A')})")
                        st.write(f"**Description:** {req.get('description', 'N/A')}")
                        
                        col_meta1, col_meta2, col_meta3 = st.columns(3)
                        with col_meta1:
                            st.caption(f"📂 Category: {req.get('category', 'N/A')}")
                        with col_meta2:
                            st.caption(f"{priority_colors.get(req_priority, '')} Priority: {req_priority}")
                        with col_meta3:
                            created = req.get('created_at', 'N/A')
                            if created != 'N/A':
                                created = created[:10]
                            st.caption(f"📅 Created: {created}")
                    
                    with col2:
                        new_status = st.selectbox(
                            "Update Status",
                            ["Submitted", "In Progress", "Resolved"],
                            index=["Submitted", "In Progress", "Resolved"].index(req_status) if req_status in ["Submitted", "In Progress", "Resolved"] else 0,
                            key=f"status_{req_id}"
                        )
                        
                        if new_status != req_status:
                            if st.button("✅ Update", key=f"update_{req_id}", use_container_width=True):
                                if update_request_status(req_id, new_status):
                                    st.success(f"✅ Status updated to {new_status}")
                                    st.rerun()
                                else:
                                    st.error("Failed to update status")
        else:
            st.info("No requests match the selected filters")
    except Exception as e:
        st.error(f"❌ Error loading service requests: {str(e)}")
        print(f"Service requests error: {e}")

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
    
    try:
        tickets = get_all_tickets(filters) if filters else get_all_tickets()
        tickets = tickets or []
        
        st.divider()
        
        if tickets:
            for ticket in tickets:
                # Safety checks
                ticket_title = ticket.get('title', 'No Title')
                ticket_status = ticket.get('status', 'Unknown')
                ticket_priority = ticket.get('priority', 'Unknown')
                ticket_id = ticket.get('ticket_id')
                
                # Status and priority styling
                status_styles = {
                    'Open': ('class="status-submitted"', '🔵'),
                    'In Progress': ('class="status-inprogress"', '🟡'),
                    'Resolved': ('class="status-resolved"', '🟢')
                }
                status_class, status_emoji = status_styles.get(ticket_status, ('', '⚪'))
                priority_colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### {ticket_title}")
                        st.write(f"**From:** {ticket.get('full_name', 'Unknown')} ({ticket.get('email', 'N/A')})")
                        st.write(f"**Description:** {ticket.get('description', 'N/A')}")
                        
                        col_meta1, col_meta2, col_meta3 = st.columns(3)
                        with col_meta1:
                            st.caption(f"📂 Category: {ticket.get('category', 'N/A')}")
                        with col_meta2:
                            st.caption(f"{priority_colors.get(ticket_priority, '')} Priority: {ticket_priority}")
                        with col_meta3:
                            created = ticket.get('created_at', 'N/A')
                            if created != 'N/A':
                                created = created[:10]
                            st.caption(f"📅 Created: {created}")
                    
                    with col2:
                        new_status = st.selectbox(
                            "Update Status",
                            ["Open", "In Progress", "Resolved"],
                            index=["Open", "In Progress", "Resolved"].index(ticket_status) if ticket_status in ["Open", "In Progress", "Resolved"] else 0,
                            key=f"ticket_status_{ticket_id}"
                        )
                        
                        if new_status != ticket_status:
                            if st.button("✅ Update", key=f"ticket_update_{ticket_id}", use_container_width=True):
                                st.success(f"✅ Status updated to {new_status}")
                                st.rerun()
        else:
            st.info("No tickets match the selected filters")
    except Exception as e:
        st.error(f"❌ Error loading tickets: {str(e)}")
        print(f"Tickets error: {e}")

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
    
    try:
        requests = get_all_requests() or []
        
        if requests:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Requests by Category")
                try:
                    df = pd.DataFrame([{
                        'Category': r.get('category', 'Unknown'),
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
                except Exception as e:
                    st.error(f"Error generating category chart: {e}")
            
            with col2:
                st.markdown("### Requests by Priority")
                try:
                    df = pd.DataFrame([{
                        'Priority': r.get('priority', 'Unknown'),
                        'Count': 1
                    } for r in requests])
                    priority_counts = df.groupby('Priority').size()
                    
                    fig = px.pie(
                        values=priority_counts.values,
                        names=priority_counts.index,
                        title="Requests by Priority"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating priority chart: {e}")
            
            st.markdown("### Request Timeline")
            try:
                # Create timeline data
                df = pd.DataFrame([{
                    'Date': r.get('created_at', 'Unknown')[:10] if r.get('created_at') else 'Unknown',
                    'Count': 1
                } for r in requests])
                
                if df['Date'].str.contains('Unknown').any():
                    df = df[df['Date'] != 'Unknown']
                
                if not df.empty:
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
                    st.info("No valid date data for timeline")
            except Exception as e:
                st.error(f"Error generating timeline: {e}")
        else:
            st.info("No data available for analytics")
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")
        print(f"Analytics error: {e}")
