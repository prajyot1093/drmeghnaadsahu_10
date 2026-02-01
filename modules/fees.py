import streamlit as st
from modules.database import get_db_connection

def init_fees_table():
    """Initialize fees table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                semester INTEGER,
                total_amount REAL,
                paid_amount REAL DEFAULT 0,
                status TEXT DEFAULT 'Pending',
                due_date DATE,
                paid_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()

def add_fee_record(user_id, semester, total_amount, due_date):
    """Add a fee record"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fees (user_id, semester, total_amount, due_date, status)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, semester, total_amount, due_date, 'Pending'))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Failed to add fee: {str(e)}")
        return False

def update_fee_payment(fee_id, paid_amount):
    """Update fee payment"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get current fee details
            cursor.execute("SELECT total_amount, paid_amount FROM fees WHERE id = ?", (fee_id,))
            result = cursor.fetchone()
            if not result:
                return False
            
            total, current_paid = result
            new_paid = current_paid + paid_amount
            status = 'Paid' if new_paid >= total else 'Partial'
            
            cursor.execute("""
                UPDATE fees SET paid_amount = ?, status = ?, paid_date = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_paid, status, fee_id))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Payment failed: {str(e)}")
        return False

def get_fee_details(user_id):
    """Get fee details for student"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, semester, total_amount, paid_amount, status, due_date FROM fees
                WHERE user_id = ? ORDER BY semester DESC
            """, (user_id,))
            return cursor.fetchall()
    except:
        return []

def get_fee_summary(user_id):
    """Get fee summary"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    SUM(total_amount) as total_due,
                    SUM(paid_amount) as total_paid,
                    SUM(total_amount - paid_amount) as outstanding
                FROM fees WHERE user_id = ?
            """, (user_id,))
            result = cursor.fetchone()
            return result if result else (0, 0, 0)
    except:
        return (0, 0, 0)

def show_fee_management(user_id):
    """Display fee management UI"""
    st.markdown("### 💰 Fee Management")
    
    # Fee summary
    total_due, total_paid, outstanding = get_fee_summary(user_id)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Due", f"₹{total_due:.2f}")
    col2.metric("Total Paid", f"₹{total_paid:.2f}")
    col3.metric("Outstanding", f"₹{outstanding:.2f}")
    
    st.divider()
    
    # Add fee record (for admin)
    if st.checkbox("Add Fee Record"):
        col1, col2, col3 = st.columns(3)
        with col1:
            semester = st.number_input("Semester", min_value=1, max_value=8)
        with col2:
            amount = st.number_input("Amount", min_value=0.0)
        with col3:
            due_date = st.date_input("Due Date")
        
        if st.button("Add Fee"):
            if add_fee_record(user_id, semester, amount, due_date):
                st.success("✅ Fee record added!")
                st.rerun()
    
    st.divider()
    
    # Payment section
    st.subheader("Make Payment")
    fee_details = get_fee_details(user_id)
    if fee_details:
        fee_options = [f"Sem {f[1]}: ₹{f[2]-f[3]} due" for f in fee_details if f[4] != 'Paid']
        if fee_options:
            selected_fee = st.selectbox("Select Fee", fee_options)
            fee_id = [f[0] for f in fee_details if f"Sem {f[1]}: ₹{f[2]-f[3]} due" == selected_fee][0]
            
            payment_amount = st.number_input("Payment Amount", min_value=0.0)
            
            if st.button("Make Payment", use_container_width=True):
                if update_fee_payment(fee_id, payment_amount):
                    st.success("✅ Payment recorded!")
                    st.rerun()
        else:
            st.success("✅ All fees paid!")
    
    st.divider()
    
    # Fee history
    st.subheader("Fee History")
    if fee_details:
        import pandas as pd
        df = pd.DataFrame(fee_details, columns=['ID', 'Semester', 'Total', 'Paid', 'Status', 'Due Date'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No fee records")
