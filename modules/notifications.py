import streamlit as st
from datetime import datetime
from modules.database import get_db_connection

def init_notifications_table():
    """Initialize notifications table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT,
                type TEXT DEFAULT 'info',
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()

def create_notification(user_id, title, message, notif_type="info"):
    """Create a new notification"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notifications (user_id, title, message, type)
                VALUES (?, ?, ?, ?)
            """, (user_id, title, message, notif_type))
            conn.commit()
            return True
    except Exception as e:
        print(f"Notification error: {str(e)}")
        return False

def get_unread_notifications(user_id):
    """Get unread notifications"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, message, type, created_at FROM notifications
                WHERE user_id = ? AND is_read = 0 ORDER BY created_at DESC
            """, (user_id,))
            return cursor.fetchall()
    except:
        return []

def get_all_notifications(user_id, limit=50):
    """Get all notifications"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, message, type, is_read, created_at FROM notifications
                WHERE user_id = ? ORDER BY created_at DESC LIMIT ?
            """, (user_id, limit))
            return cursor.fetchall()
    except:
        return []

def mark_as_read(notif_id):
    """Mark notification as read"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
            conn.commit()
            return True
    except:
        return False

def show_notifications(user_id):
    """Display notifications UI"""
    st.markdown("### 🔔 Notifications")
    
    unread_count = len(get_unread_notifications(user_id))
    st.write(f"**{unread_count} unread notifications**")
    
    st.divider()
    
    # Show notifications
    notifications = get_all_notifications(user_id)
    
    if notifications:
        for notif in notifications:
            notif_id, title, message, notif_type, is_read, created_at = notif
            
            # Color based on type
            type_icons = {
                'success': '✅',
                'warning': '⚠️',
                'error': '❌',
                'info': 'ℹ️'
            }
            
            read_style = "" if is_read else "**"
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{read_style}{type_icons.get(notif_type, '📢')} {title}{read_style}")
                    st.caption(message)
                with col2:
                    st.caption(created_at[:10])
                with col3:
                    if not is_read:
                        if st.button("Mark Read", key=f"notif_{notif_id}"):
                            mark_as_read(notif_id)
                            st.rerun()
    else:
        st.info("No notifications yet")
