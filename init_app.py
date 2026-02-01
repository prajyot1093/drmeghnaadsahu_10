"""
Initialization script to set up the application with demo data
"""
from modules.database import init_database, add_user, submit_service_request
from modules.documents import init_documents_table
from modules.attendance import init_attendance_table
from modules.exams import init_exams_table
from modules.notifications import init_notifications_table
from modules.fees import init_fees_table
from modules.workflow import init_workflow_table

def initialize_app():
    """Initialize database and add demo data"""
    print("Initializing database...")
    init_database()
    
    print("Initializing advanced features...")
    init_documents_table()
    init_attendance_table()
    init_exams_table()
    init_notifications_table()
    init_fees_table()
    init_workflow_table()
    
    print("Adding demo users...")
    # Add demo students
    add_user("student1@example.com", "student123", "Raj Kumar", "student")
    add_user("student2@example.com", "student123", "Priya Singh", "student")
    
    # Add demo admin
    add_user("admin@example.com", "admin123", "Admin User", "admin")
    
    print("Adding sample service requests...")
    # Add sample requests (user_id would be 1 for first student)
    submit_service_request(
        user_id=1,
        title="Exam Schedule Conflict",
        description="I have two exams scheduled at the same time",
        category="Exam",
        priority="High"
    )
    
    submit_service_request(
        user_id=1,
        title="Certificate Request",
        description="Need transfer certificate for higher studies",
        category="Academic",
        priority="Medium"
    )
    
    print("✅ Application initialized successfully!")

if __name__ == "__main__":
    initialize_app()
