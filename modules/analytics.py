import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from modules.database import get_db_connection

def get_analytics_data(user_id=None, days=30):
    """Get analytics data for dashboard"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get requests trend
            cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as count, status
                FROM service_requests
                WHERE created_at >= datetime('now', '-' || ? || ' days')
                GROUP BY DATE(created_at), status
                ORDER BY date
            """, (days,))
            requests_trend = pd.DataFrame(cursor.fetchall(), columns=['date', 'count', 'status'])
            
            # Get ticket distribution
            cursor.execute("""
                SELECT category, COUNT(*) as count, AVG(CASE WHEN status='Resolved' THEN 1 ELSE 0 END)*100 as resolution_rate
                FROM tickets
                WHERE created_at >= datetime('now', '-' || ? || ' days')
                GROUP BY category
            """, (days,))
            tickets_by_category = pd.DataFrame(cursor.fetchall(), columns=['category', 'count', 'resolution_rate'])
            
            # Get status distribution
            cursor.execute("""
                SELECT status, COUNT(*) as count FROM service_requests GROUP BY status
            """)
            status_dist = pd.DataFrame(cursor.fetchall(), columns=['status', 'count'])
            
            return {
                'requests_trend': requests_trend,
                'tickets_by_category': tickets_by_category,
                'status_distribution': status_dist
            }
    except Exception as e:
        st.error(f"Error fetching analytics: {str(e)}")
        return None

def create_request_trend_chart(data):
    """Create request trend chart"""
    if data.empty:
        return None
    fig = px.line(data, x='date', y='count', color='status', 
                  title='Service Requests Trend (Last 30 Days)',
                  markers=True, line_shape='spline')
    fig.update_layout(hovermode='x unified', height=400)
    return fig

def create_ticket_distribution_chart(data):
    """Create ticket distribution chart"""
    if data.empty:
        return None
    fig = px.bar(data, x='category', y='count',
                 title='Tickets by Category',
                 color='resolution_rate', color_continuous_scale='viridis')
    fig.update_layout(height=400)
    return fig

def create_status_pie_chart(data):
    """Create status distribution pie chart"""
    if data.empty:
        return None
    fig = px.pie(data, values='count', names='status',
                 title='Request Status Distribution')
    return fig

def show_advanced_analytics():
    """Display advanced analytics dashboard"""
    st.markdown("## 📊 Advanced Analytics Dashboard")
    
    # Time range selector
    col1, col2 = st.columns(2)
    with col1:
        days = st.slider("Select time range (days)", 7, 90, 30)
    
    analytics_data = get_analytics_data(days=days)
    
    if analytics_data:
        # Request trends
        st.subheader("Request Trends")
        trend_chart = create_request_trend_chart(analytics_data['requests_trend'])
        if trend_chart:
            st.plotly_chart(trend_chart, use_container_width=True)
        
        # Tickets and Status
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Tickets by Category")
            ticket_chart = create_ticket_distribution_chart(analytics_data['tickets_by_category'])
            if ticket_chart:
                st.plotly_chart(ticket_chart, use_container_width=True)
        
        with col2:
            st.subheader("Request Status")
            status_chart = create_status_pie_chart(analytics_data['status_distribution'])
            if status_chart:
                st.plotly_chart(status_chart, use_container_width=True)
        
        # Summary metrics
        st.divider()
        st.subheader("📈 Summary Metrics")
        
        total_requests = analytics_data['requests_trend']['count'].sum() if not analytics_data['requests_trend'].empty else 0
        total_tickets = analytics_data['tickets_by_category']['count'].sum() if not analytics_data['tickets_by_category'].empty else 0
        avg_resolution = analytics_data['tickets_by_category']['resolution_rate'].mean() if not analytics_data['tickets_by_category'].empty else 0
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Total Requests", int(total_requests))
        metric_col2.metric("Total Tickets", int(total_tickets))
        metric_col3.metric("Avg Resolution Rate", f"{avg_resolution:.1f}%")
