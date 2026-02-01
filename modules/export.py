import streamlit as st
import pandas as pd
from io import BytesIO
from modules.database import get_db_connection

def export_to_csv(user_id, export_type="all"):
    """Export data to CSV"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            data = {}
            
            if export_type in ["all", "results"]:
                cursor.execute("""
                    SELECT exam_name, subject, marks_obtained, percentage, grade FROM exam_results
                    WHERE user_id = ? ORDER BY exam_date DESC
                """, (user_id,))
                results = cursor.fetchall()
                if results:
                    data['Exam Results'] = pd.DataFrame(results, columns=['Exam', 'Subject', 'Marks', 'Percentage', 'Grade'])
            
            if export_type in ["all", "requests"]:
                cursor.execute("""
                    SELECT title, status, priority, created_at FROM service_requests
                    WHERE user_id = ? ORDER BY created_at DESC
                """, (user_id,))
                requests = cursor.fetchall()
                if requests:
                    data['Service Requests'] = pd.DataFrame(requests, columns=['Title', 'Status', 'Priority', 'Date'])
            
            if export_type in ["all", "tickets"]:
                cursor.execute("""
                    SELECT category, status, priority, created_at FROM tickets
                    WHERE user_id = ? ORDER BY created_at DESC
                """, (user_id,))
                tickets = cursor.fetchall()
                if tickets:
                    data['Support Tickets'] = pd.DataFrame(tickets, columns=['Category', 'Status', 'Priority', 'Date'])
            
            return data
    except Exception as e:
        st.error(f"Export failed: {str(e)}")
        return {}

def export_to_pdf_simple(user_id):
    """Generate simple PDF report"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT name, email FROM users WHERE user_id = ?", (user_id,))
            user_info = cursor.fetchone()
            
            cursor.execute("""
                SELECT COUNT(*) FROM service_requests WHERE user_id = ? AND status='Resolved'
            """, (user_id,))
            resolved_count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT AVG(percentage) FROM exam_results WHERE user_id = ?
            """, (user_id,))
            avg_marks = cursor.fetchone()[0] or 0
            
            report = f"""
STUDENT REPORT - {user_info[0]}
{'='*50}
Email: {user_info[1]}
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

STATISTICS
{'='*50}
Total Resolved Requests: {resolved_count}
Average Exam Score: {avg_marks:.2f}%
            """
            return report
    except:
        return ""

def show_export_manager(user_id):
    """Display export management UI"""
    st.markdown("### 📥 Export & Reports")
    
    # Export format selection
    col1, col2 = st.columns(2)
    with col1:
        export_format = st.selectbox("Export Format", ["CSV", "PDF"])
    with col2:
        export_type = st.selectbox("Data Type", ["All", "Exam Results", "Requests", "Tickets"])
    
    st.divider()
    
    if export_format == "CSV":
        if st.button("Generate CSV Export", use_container_width=True):
            data = export_to_csv(user_id, export_type.lower().replace(" results", "").replace(" ", "_"))
            if data:
                # Create Excel file with multiple sheets
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    for sheet_name, df in data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                output.seek(0)
                st.download_button(
                    label="📥 Download Excel",
                    data=output.getvalue(),
                    file_name=f"student_report_{user_id}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("No data to export")
    
    else:  # PDF
        if st.button("Generate PDF Report", use_container_width=True):
            report = export_to_pdf_simple(user_id)
            if report:
                st.download_button(
                    label="📥 Download PDF",
                    data=report.encode(),
                    file_name=f"student_report_{user_id}.txt",
                    mime="text/plain"
                )
            else:
                st.info("No data to generate report")
    
    st.info("💡 Export your academic records and requests in multiple formats for offline access")
