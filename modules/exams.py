import streamlit as st
import pandas as pd
from modules.database import get_db_connection

def init_exams_table():
    """Initialize exam results table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exam_name TEXT NOT NULL,
                subject TEXT,
                marks_obtained REAL,
                total_marks REAL DEFAULT 100,
                percentage REAL,
                grade TEXT,
                exam_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()

def add_exam_result(user_id, exam_name, subject, marks, total_marks=100):
    """Add exam result"""
    try:
        percentage = (marks / total_marks) * 100
        grade = get_grade(percentage)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO exam_results (user_id, exam_name, subject, marks_obtained, total_marks, percentage, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, exam_name, subject, marks, total_marks, percentage, grade))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Failed to add result: {str(e)}")
        return False

def get_grade(percentage):
    """Calculate grade from percentage"""
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    else:
        return 'F'

def get_exam_results(user_id):
    """Get all exam results for user"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exam_name, subject, marks_obtained, total_marks, percentage, grade, exam_date
                FROM exam_results WHERE user_id = ? ORDER BY exam_date DESC
            """, (user_id,))
            return cursor.fetchall()
    except:
        return []

def get_overall_performance(user_id):
    """Get overall exam performance"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_exams,
                    AVG(percentage) as avg_percentage,
                    MAX(percentage) as best_score,
                    MIN(percentage) as worst_score
                FROM exam_results WHERE user_id = ?
            """, (user_id,))
            result = cursor.fetchone()
            return result if result else (0, 0, 0, 0)
    except:
        return (0, 0, 0, 0)

def show_exam_results(user_id):
    """Display exam results UI"""
    st.markdown("### 📝 Exam Results")
    
    # Performance metrics
    total_exams, avg_percentage, best_score, worst_score = get_overall_performance(user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Exams", int(total_exams))
    col2.metric("Average Score", f"{avg_percentage:.1f}%")
    col3.metric("Best Score", f"{best_score:.1f}%")
    col4.metric("Worst Score", f"{worst_score:.1f}%")
    
    st.divider()
    
    # Add result (for admin)
    if st.checkbox("Add Exam Result"):
        col1, col2 = st.columns(2)
        with col1:
            exam_name = st.text_input("Exam Name")
            subject = st.text_input("Subject")
        with col2:
            marks = st.number_input("Marks Obtained", min_value=0.0, max_value=100.0)
            total = st.number_input("Total Marks", min_value=1.0, value=100.0)
        
        if st.button("Add Result"):
            if exam_name and subject:
                if add_exam_result(user_id, exam_name, subject, marks, total):
                    st.success("✅ Result added!")
                    st.rerun()
            else:
                st.warning("Please fill all fields")
    
    st.divider()
    
    # Display results
    st.subheader("Exam History")
    results = get_exam_results(user_id)
    if results:
        df = pd.DataFrame(results, columns=['Exam', 'Subject', 'Marks', 'Total', 'Percentage', 'Grade', 'Date'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No exam results yet")
