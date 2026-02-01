import streamlit as st
from modules.database import get_db_connection

def calculate_gpa(marks_dict):
    """Calculate GPA from marks"""
    if not marks_dict:
        return 0.0
    
    total_points = 0
    credit_hours = 0
    
    for subject, (marks, credits) in marks_dict.items():
        grade_point = get_grade_point(marks)
        total_points += grade_point * credits
        credit_hours += credits
    
    return round(total_points / credit_hours, 2) if credit_hours > 0 else 0.0

def get_grade_point(percentage):
    """Get grade point from percentage"""
    if percentage >= 90:
        return 4.0  # A+
    elif percentage >= 80:
        return 3.7  # A
    elif percentage >= 70:
        return 3.3  # B+
    elif percentage >= 60:
        return 3.0  # B
    elif percentage >= 50:
        return 2.0  # C
    else:
        return 0.0  # F

def get_cumulative_gpa(user_id):
    """Get cumulative GPA for student"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AVG(percentage) FROM exam_results WHERE user_id = ?
            """, (user_id,))
            avg_percentage = cursor.fetchone()[0] or 0
            return round(get_grade_point(avg_percentage) * 4 / 4, 2)
    except:
        return 0.0

def show_gpa_calculator(user_id):
    """Display GPA calculator UI"""
    st.markdown("### 📊 GPA Calculator")
    
    current_gpa = get_cumulative_gpa(user_id)
    st.metric("Cumulative GPA", f"{current_gpa:.2f}/4.0")
    
    st.divider()
    
    # GPA Calculation Tool
    st.subheader("Calculate GPA")
    
    num_subjects = st.slider("Number of Subjects", 1, 8, 4)
    
    subjects_data = {}
    
    cols = st.columns(3)
    for i in range(num_subjects):
        col_idx = i % 3
        with cols[col_idx]:
            subject_name = st.text_input(f"Subject {i+1}", key=f"subj_{i}")
            marks = st.number_input(f"Marks {i+1}", min_value=0.0, max_value=100.0, key=f"marks_{i}")
            credits = st.number_input(f"Credits {i+1}", min_value=1.0, max_value=4.0, value=1.0, step=0.5, key=f"credits_{i}")
            
            if subject_name:
                subjects_data[subject_name] = (marks, credits)
    
    if st.button("Calculate GPA"):
        if subjects_data:
            calculated_gpa = calculate_gpa(subjects_data)
            st.success(f"✅ Your GPA: **{calculated_gpa:.2f}/4.0**")
            
            # Show grade distribution
            st.subheader("Grade Distribution")
            grade_info = []
            for subject, (marks, credits) in subjects_data.items():
                grade_point = get_grade_point(marks)
                grade = ['F', 'C', 'B', 'B+', 'A', 'A+'][int(grade_point)]
                grade_info.append({
                    'Subject': subject,
                    'Marks': f"{marks:.1f}%",
                    'Credits': credits,
                    'Grade': grade,
                    'Grade Points': grade_point
                })
            
            import pandas as pd
            df = pd.DataFrame(grade_info)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Please enter at least one subject")
    
    st.info("💡 GPA Calculation: Sum of (Grade Point × Credits) ÷ Total Credits")
