import streamlit as st
from datetime import datetime
from modules.database import get_db_connection

def init_attendance_table():
    """Initialize attendance table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                status TEXT DEFAULT 'Present',
                subject TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()

def mark_attendance(user_id, date, status, subject="General"):
    """Mark attendance for student"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO attendance (user_id, date, status, subject)
                VALUES (?, ?, ?, ?)
            """, (user_id, date, status, subject))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Attendance marking failed: {str(e)}")
        return False

def get_attendance_summary(user_id, days=30):
    """Get attendance summary for user"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_classes,
                    SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present,
                    SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END) as absent,
                    ROUND(SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) as percentage
                FROM attendance
                WHERE user_id = ? AND date >= date('now', '-' || ? || ' days')
            """, (user_id, days))
            result = cursor.fetchone()
            return result if result else (0, 0, 0, 0.0)
    except:
        return (0, 0, 0, 0.0)

def get_attendance_records(user_id, limit=30):
    """Get attendance records for user"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT date, status, subject FROM attendance
                WHERE user_id = ? ORDER BY date DESC LIMIT ?
            """, (user_id, limit))
            return cursor.fetchall()
    except:
        return []

def show_attendance_tracker(user_id):
    """Display attendance tracking UI"""
    st.markdown("### 📋 Attendance Tracker")
    
    # Attendance Summary
    total, present, absent, percentage = get_attendance_summary(user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Classes", total)
    col2.metric("Present", present)
    col3.metric("Absent", absent)
    col4.metric("Attendance %", f"{percentage}%")
    
    st.divider()
    
    # Mark attendance (for admin)
    if st.checkbox("Mark Attendance"):
        col1, col2, col3 = st.columns(3)
        with col1:
            att_date = st.date_input("Date", value=datetime.today())
        with col2:
            att_status = st.selectbox("Status", ["Present", "Absent", "Leave"])
        with col3:
            subject = st.text_input("Subject")
        
        if st.button("Mark"):
            if mark_attendance(user_id, att_date, att_status, subject):
                st.success("✅ Attendance marked!")
                st.rerun()
    
    st.divider()
    
    # Attendance records
    st.subheader("Attendance Records")
    records = get_attendance_records(user_id)
    if records:
        import pandas as pd
        df = pd.DataFrame(records, columns=['Date', 'Status', 'Subject'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No attendance records yet")
