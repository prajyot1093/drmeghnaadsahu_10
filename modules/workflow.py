import streamlit as st
from datetime import datetime
from modules.database import get_db_connection

def init_workflow_table():
    """Initialize workflow tracking table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER,
                ticket_id INTEGER,
                current_stage TEXT,
                progress_percentage INTEGER DEFAULT 0,
                assigned_to TEXT,
                notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(request_id) REFERENCES service_requests(id),
                FOREIGN KEY(ticket_id) REFERENCES tickets(id)
            )
        """)
        conn.commit()

def update_workflow_stage(request_id=None, ticket_id=None, stage='', progress=0, notes=''):
    """Update workflow stage"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO workflow_tracking (request_id, ticket_id, current_stage, progress_percentage, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (request_id, ticket_id, stage, progress, notes))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Workflow update failed: {str(e)}")
        return False

def get_workflow_status(request_id=None, ticket_id=None):
    """Get current workflow status"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if request_id:
                cursor.execute("""
                    SELECT current_stage, progress_percentage, notes, updated_at FROM workflow_tracking
                    WHERE request_id = ? ORDER BY updated_at DESC LIMIT 1
                """, (request_id,))
            else:
                cursor.execute("""
                    SELECT current_stage, progress_percentage, notes, updated_at FROM workflow_tracking
                    WHERE ticket_id = ? ORDER BY updated_at DESC LIMIT 1
                """, (ticket_id,))
            return cursor.fetchone()
    except:
        return None

def get_workflow_history(request_id=None, ticket_id=None):
    """Get workflow history"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if request_id:
                cursor.execute("""
                    SELECT current_stage, progress_percentage, notes, updated_at FROM workflow_tracking
                    WHERE request_id = ? ORDER BY updated_at DESC
                """, (request_id,))
            else:
                cursor.execute("""
                    SELECT current_stage, progress_percentage, notes, updated_at FROM workflow_tracking
                    WHERE ticket_id = ? ORDER BY updated_at DESC
                """, (ticket_id,))
            return cursor.fetchall()
    except:
        return []

def show_workflow_automation(request_id=None, ticket_id=None):
    """Display workflow automation UI"""
    st.markdown("### ⚙️ Workflow Automation")
    
    workflow_status = get_workflow_status(request_id, ticket_id)
    
    if workflow_status:
        stage, progress, notes, updated = workflow_status
        
        st.subheader("Current Status")
        col1, col2 = st.columns(2)
        col1.write(f"**Stage**: {stage}")
        col2.write(f"**Progress**: {progress}%")
        
        # Progress bar
        st.progress(min(progress / 100, 1.0))
        
        if notes:
            st.info(f"📝 Notes: {notes}")
        
        st.caption(f"Last updated: {updated}")
        
        st.divider()
    
    # Update workflow
    st.subheader("Update Workflow")
    
    col1, col2 = st.columns(2)
    with col1:
        stage = st.selectbox("Select Stage", [
            "Received",
            "Under Review",
            "In Progress",
            "Verification",
            "Completed",
            "Resolved"
        ])
    with col2:
        progress = st.slider("Progress %", 0, 100, value=workflow_status[1] if workflow_status else 0)
    
    notes_input = st.text_area("Additional Notes")
    
    if st.button("Update Status", use_container_width=True):
        if update_workflow_stage(request_id, ticket_id, stage, progress, notes_input):
            st.success("✅ Workflow updated!")
            st.rerun()
    
    st.divider()
    
    # Workflow history
    st.subheader("Workflow History")
    history = get_workflow_history(request_id, ticket_id)
    if history:
        import pandas as pd
        df = pd.DataFrame(history, columns=['Stage', 'Progress %', 'Notes', 'Updated At'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No workflow history yet")
