import streamlit as st
import os
import sqlite3
from datetime import datetime
from modules.database import get_db_connection

UPLOAD_FOLDER = "documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_documents_table():
    """Initialize documents table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                doc_type TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()

def upload_document(user_id, uploaded_file, doc_type="General"):
    """Upload document for a student"""
    try:
        if uploaded_file is not None:
            # Save file
            file_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_{datetime.now().timestamp()}_{uploaded_file.name}")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Store in database
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO documents (user_id, filename, file_path, doc_type)
                    VALUES (?, ?, ?, ?)
                """, (user_id, uploaded_file.name, file_path, doc_type))
                conn.commit()
            return True
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return False

def get_user_documents(user_id):
    """Get all documents for a user"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, filename, doc_type, uploaded_at FROM documents
                WHERE user_id = ? ORDER BY uploaded_at DESC
            """, (user_id,))
            return cursor.fetchall()
    except Exception as e:
        return []

def delete_document(doc_id):
    """Delete a document"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path FROM documents WHERE id = ?", (doc_id,))
            result = cursor.fetchone()
            if result:
                file_path = result[0]
                if os.path.exists(file_path):
                    os.remove(file_path)
                cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
                conn.commit()
                return True
    except Exception as e:
        st.error(f"Delete failed: {str(e)}")
    return False

def show_document_manager(user_id):
    """Display document management UI"""
    st.markdown("### 📄 Document Manager")
    
    # Upload section
    st.subheader("Upload Documents")
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)
    with col2:
        doc_type = st.selectbox("Document Type", ["ID Proof", "Address Proof", "Certificate", "Transcript", "Other"])
    
    if st.button("Upload Document", use_container_width=True):
        if uploaded_file:
            if upload_document(user_id, uploaded_file, doc_type):
                st.success("✅ Document uploaded successfully!")
                st.rerun()
        else:
            st.warning("Please select a file")
    
    # View documents
    st.subheader("Your Documents")
    documents = get_user_documents(user_id)
    if documents:
        for doc in documents:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"📄 {doc[1]} ({doc[2]})")
            with col2:
                st.caption(doc[3][:10])
            with col3:
                if st.button("🗑️", key=f"del_{doc[0]}"):
                    if delete_document(doc[0]):
                        st.success("Deleted!")
                        st.rerun()
    else:
        st.info("No documents uploaded yet")
