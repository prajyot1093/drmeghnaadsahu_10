"""
Professional ERP System Database Module
Based on Academic Research Paper Requirements
Includes: Registration, Academic Management, Results Analysis, Performance Tracking, 
Placement Prediction, Financial Management
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from contextlib import contextmanager
import hashlib

# Ensure data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, 'erp_system.db')

# Constants
ROLES = ['student', 'faculty', 'admin']
ACADEMIC_STATUSES = ['Active', 'Inactive', 'On Leave', 'Graduated']
FEE_STATUSES = ['Pending', 'Partial', 'Paid', 'Overdue']
SEMESTERS = list(range(1, 9))
GRADE_SCALE = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}

def get_connection():
    """Get database connection with proper configuration"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize comprehensive ERP database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Enhanced Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            role TEXT NOT NULL CHECK(role IN ('student', 'faculty', 'admin')),
            is_active BOOLEAN DEFAULT 1,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Enhanced Student Profile
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            roll_number TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL,
            cgpa REAL DEFAULT 0.0,
            phone TEXT,
            address TEXT,
            father_name TEXT,
            mother_name TEXT,
            dob TEXT,
            admission_date TEXT,
            academic_status TEXT DEFAULT 'Active',
            cet_rank TEXT,
            admission_quota TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')
    
    # Academic Marks (IA Marks) - Core for Performance Analysis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS academic_marks (
            marks_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            semester INTEGER NOT NULL,
            internal_marks REAL,
            external_marks REAL,
            total_marks REAL,
            percentage REAL,
            grade TEXT,
            gpa REAL,
            recorded_by INTEGER,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (recorded_by) REFERENCES users(user_id),
            UNIQUE(user_id, subject, semester)
        )
    ''')
    
    # University Results - External Result Integration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS university_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            usn TEXT,
            total_marks REAL,
            pass_marks REAL,
            percentage REAL,
            sgpa REAL,
            result_status TEXT,
            published_date TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, semester)
        )
    ''')
    
    # Service Requests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Submitted',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')
    
    # Semester Registration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS semester_registrations (
            registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            current_semester INTEGER NOT NULL,
            desired_semester INTEGER NOT NULL,
            cgpa_required REAL,
            status TEXT DEFAULT 'Pending',
            approved_by INTEGER,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (approved_by) REFERENCES users(user_id)
        )
    ''')
    
    # Exam Registration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exam_registrations (
            exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exam_name TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            subject TEXT NOT NULL,
            exam_marks REAL,
            status TEXT DEFAULT 'Registered',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Attendance Tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            semester INTEGER NOT NULL,
            total_classes INTEGER DEFAULT 0,
            attended_classes INTEGER DEFAULT 0,
            attendance_percentage REAL DEFAULT 0.0,
            recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, subject, semester)
        )
    ''')
    
    # Fee Management
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            amount_due REAL NOT NULL,
            amount_paid REAL DEFAULT 0.0,
            fee_status TEXT DEFAULT 'Pending',
            due_date TEXT,
            paid_date TEXT,
            transaction_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, semester)
        )
    ''')
    
    # Support Tickets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            resolved_by INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (resolved_by) REFERENCES users(user_id)
        )
    ''')
    
    # Faculty Profile
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty_profiles (
            faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            employee_id TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            designation TEXT,
            qualification TEXT,
            phone TEXT,
            address TEXT,
            specialization TEXT,
            joined_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')
    
    # Placement Records - For Placement Prediction
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS placement_records (
            placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_name TEXT,
            package REAL,
            position TEXT,
            placement_date TEXT,
            placement_status TEXT,
            eligibility_criteria_met BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Performance Metrics - For Analytics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            sgpa REAL,
            cgpa REAL,
            attendance_percentage REAL,
            placement_eligible BOOLEAN,
            predicted_placement REAL,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, semester)
        )
    ''')
    
    conn.commit()
    conn.close()

# ============================================================================
# USER MANAGEMENT
# ============================================================================

def add_user(email: str, password: str, full_name: str, role: str, phone: str = None) -> bool:
    """Add new user with validation"""
    if not all([email, password, full_name, role]):
        return False
    
    if role not in ROLES:
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            cursor.execute('''
                INSERT INTO users (email, password, full_name, role, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (email.lower(), hashed_password, full_name.strip(), role, phone))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def get_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate user"""
    if not email or not password:
        return None
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            cursor.execute('''
                SELECT * FROM users WHERE LOWER(email) = ? AND password = ? AND is_active = 1
            ''', (email.lower(), hashed_password))
            user = cursor.fetchone()
        
        if user:
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?', (user['user_id'],))
            conn.commit()
        
        return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Get user by ID"""
    if not user_id:
        return None
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ? AND is_active = 1', (user_id,))
            user = cursor.fetchone()
        return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None

# ============================================================================
# STUDENT MANAGEMENT
# ============================================================================

def update_student_profile(user_id: int, profile_data: Dict) -> bool:
    """Update or create student profile"""
    if not user_id or not profile_data:
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT profile_id FROM student_profiles WHERE user_id = ?', (user_id,))
            profile = cursor.fetchone()
            
            if profile:
                cursor.execute('''
                    UPDATE student_profiles SET
                    roll_number = ?, department = ?, semester = ?, cgpa = ?,
                    phone = ?, address = ?, father_name = ?, mother_name = ?, dob = ?,
                    admission_date = ?, academic_status = ?, cet_rank = ?, admission_quota = ?,
                    updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (
                    profile_data.get('roll_number'),
                    profile_data.get('department'),
                    profile_data.get('semester'),
                    profile_data.get('cgpa', 0),
                    profile_data.get('phone'),
                    profile_data.get('address'),
                    profile_data.get('father_name'),
                    profile_data.get('mother_name'),
                    profile_data.get('dob'),
                    profile_data.get('admission_date'),
                    profile_data.get('academic_status', 'Active'),
                    profile_data.get('cet_rank'),
                    profile_data.get('admission_quota'),
                    user_id
                ))
            else:
                cursor.execute('''
                    INSERT INTO student_profiles 
                    (user_id, roll_number, department, semester, cgpa, phone, address, 
                     father_name, mother_name, dob, admission_date, academic_status, 
                     cet_rank, admission_quota)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    profile_data.get('roll_number'),
                    profile_data.get('department'),
                    profile_data.get('semester', 1),
                    profile_data.get('cgpa', 0),
                    profile_data.get('phone'),
                    profile_data.get('address'),
                    profile_data.get('father_name'),
                    profile_data.get('mother_name'),
                    profile_data.get('dob'),
                    profile_data.get('admission_date'),
                    profile_data.get('academic_status', 'Active'),
                    profile_data.get('cet_rank'),
                    profile_data.get('admission_quota')
                ))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False

def get_student_profile(user_id: int) -> Optional[Dict]:
    """Get student profile"""
    if not user_id:
        return None
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM student_profiles WHERE user_id = ?', (user_id,))
            profile = cursor.fetchone()
        return dict(profile) if profile else None
    except Exception as e:
        print(f"Error getting student profile: {e}")
        return None

def get_all_students() -> List[Dict]:
    """Get all registered students"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.user_id, u.full_name, u.email, u.phone,
                       sp.roll_number, sp.department, sp.semester, sp.cgpa, sp.academic_status
                FROM users u
                LEFT JOIN student_profiles sp ON u.user_id = sp.user_id
                WHERE u.role = 'student' AND u.is_active = 1
                ORDER BY u.full_name
            ''')
            students = cursor.fetchall()
        return [dict(student) for student in students]
    except Exception as e:
        print(f"Error getting students: {e}")
        return []

# ============================================================================
# ACADEMIC MARKS & PERFORMANCE
# ============================================================================

def add_student_marks(user_id: int, subject: str, internal_marks: float, 
                     external_marks: float, semester: int, faculty_id: int = None) -> bool:
    """Add or update student academic marks"""
    if not all([user_id, subject, semester]):
        return False
    
    try:
        total_marks = (internal_marks or 0) + (external_marks or 0)
        percentage = (total_marks / 200 * 100) if total_marks > 0 else 0
        
        # Calculate grade
        if percentage >= 90:
            grade = 'A'
            gpa = 4.0
        elif percentage >= 80:
            grade = 'B'
            gpa = 3.0
        elif percentage >= 70:
            grade = 'C'
            gpa = 2.0
        elif percentage >= 60:
            grade = 'D'
            gpa = 1.0
        else:
            grade = 'F'
            gpa = 0.0
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT marks_id FROM academic_marks 
                WHERE user_id = ? AND subject = ? AND semester = ?
            ''', (user_id, subject, semester))
            
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('''
                    UPDATE academic_marks 
                    SET internal_marks = ?, external_marks = ?, total_marks = ?, 
                        percentage = ?, grade = ?, gpa = ?, recorded_at = CURRENT_TIMESTAMP
                    WHERE user_id = ? AND subject = ? AND semester = ?
                ''', (internal_marks, external_marks, total_marks, percentage, grade, 
                      gpa, user_id, subject, semester))
            else:
                cursor.execute('''
                    INSERT INTO academic_marks 
                    (user_id, subject, semester, internal_marks, external_marks, 
                     total_marks, percentage, grade, gpa, recorded_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, subject, semester, internal_marks, external_marks, 
                      total_marks, percentage, grade, gpa, faculty_id))
            
            conn.commit()
        
        # Update performance metrics
        update_student_performance_metrics(user_id, semester)
        return True
    except Exception as e:
        print(f"Error adding marks: {e}")
        return False

def get_student_marks(user_id: int, semester: int = None) -> List[Dict]:
    """Get student marks"""
    if not user_id:
        return []
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if semester:
                cursor.execute('''
                    SELECT * FROM academic_marks 
                    WHERE user_id = ? AND semester = ?
                    ORDER BY subject
                ''', (user_id, semester))
            else:
                cursor.execute('''
                    SELECT * FROM academic_marks 
                    WHERE user_id = ?
                    ORDER BY semester DESC, subject
                ''', (user_id,))
            marks = cursor.fetchall()
        return [dict(mark) for mark in marks]
    except Exception as e:
        print(f"Error getting marks: {e}")
        return []

def update_student_performance_metrics(user_id: int, semester: int) -> bool:
    """Calculate and update performance metrics"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get all marks for this semester
            cursor.execute('''
                SELECT AVG(gpa) as avg_gpa, AVG(percentage) as avg_percentage
                FROM academic_marks 
                WHERE user_id = ? AND semester = ?
            ''', (user_id, semester))
            
            result = cursor.fetchone()
            sgpa = result['avg_gpa'] or 0.0
            
            # Get cumulative GPA
            cursor.execute('''
                SELECT AVG(gpa) as cgpa FROM academic_marks WHERE user_id = ?
            ''', (user_id,))
            
            cgpa_result = cursor.fetchone()
            cgpa = cgpa_result['cgpa'] or 0.0
            
            # Get attendance
            cursor.execute('''
                SELECT AVG(attendance_percentage) as avg_attendance
                FROM attendance WHERE user_id = ? AND semester = ?
            ''', (user_id, semester))
            
            att_result = cursor.fetchone()
            attendance = att_result['avg_attendance'] or 0.0
            
            # Placement eligibility
            placement_eligible = (sgpa >= 2.0 and attendance >= 75.0)
            
            # Check if record exists
            cursor.execute('''
                SELECT metric_id FROM performance_metrics 
                WHERE user_id = ? AND semester = ?
            ''', (user_id, semester))
            
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE performance_metrics 
                    SET sgpa = ?, cgpa = ?, attendance_percentage = ?, 
                        placement_eligible = ?
                    WHERE user_id = ? AND semester = ?
                ''', (sgpa, cgpa, attendance, placement_eligible, user_id, semester))
            else:
                cursor.execute('''
                    INSERT INTO performance_metrics 
                    (user_id, semester, sgpa, cgpa, attendance_percentage, placement_eligible)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, semester, sgpa, cgpa, attendance, placement_eligible))
            
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating metrics: {e}")
        return False

# ============================================================================
# ATTENDANCE MANAGEMENT
# ============================================================================

def update_attendance(user_id: int, subject: str, semester: int, 
                     total_classes: int, attended_classes: int) -> bool:
    """Update attendance record"""
    if not all([user_id, subject, semester]):
        return False
    
    try:
        attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT attendance_id FROM attendance 
                WHERE user_id = ? AND subject = ? AND semester = ?
            ''', (user_id, subject, semester))
            
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE attendance 
                    SET total_classes = ?, attended_classes = ?, attendance_percentage = ?
                    WHERE user_id = ? AND subject = ? AND semester = ?
                ''', (total_classes, attended_classes, attendance_percentage, user_id, subject, semester))
            else:
                cursor.execute('''
                    INSERT INTO attendance 
                    (user_id, subject, semester, total_classes, attended_classes, attendance_percentage)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, subject, semester, total_classes, attended_classes, attendance_percentage))
            
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating attendance: {e}")
        return False

def get_student_attendance(user_id: int, semester: int = None) -> List[Dict]:
    """Get student attendance"""
    if not user_id:
        return []
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if semester:
                cursor.execute('''
                    SELECT * FROM attendance 
                    WHERE user_id = ? AND semester = ?
                    ORDER BY subject
                ''', (user_id, semester))
            else:
                cursor.execute('''
                    SELECT * FROM attendance 
                    WHERE user_id = ?
                    ORDER BY semester DESC, subject
                ''', (user_id,))
            attendance = cursor.fetchall()
        return [dict(att) for att in attendance]
    except Exception as e:
        print(f"Error getting attendance: {e}")
        return []

# ============================================================================
# FEE MANAGEMENT
# ============================================================================

def update_fee_record(user_id: int, semester: int, amount_due: float, amount_paid: float = 0) -> bool:
    """Update fee record"""
    if not all([user_id, semester, amount_due]):
        return False
    
    try:
        fee_status = 'Paid' if amount_paid >= amount_due else ('Partial' if amount_paid > 0 else 'Pending')
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT fee_id FROM fees WHERE user_id = ? AND semester = ?
            ''', (user_id, semester))
            
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE fees 
                    SET amount_due = ?, amount_paid = ?, fee_status = ?
                    WHERE user_id = ? AND semester = ?
                ''', (amount_due, amount_paid, fee_status, user_id, semester))
            else:
                cursor.execute('''
                    INSERT INTO fees (user_id, semester, amount_due, amount_paid, fee_status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, semester, amount_due, amount_paid, fee_status))
            
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating fees: {e}")
        return False

def get_student_fees(user_id: int) -> List[Dict]:
    """Get all fee records for student"""
    if not user_id:
        return []
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM fees WHERE user_id = ? ORDER BY semester
            ''', (user_id,))
            fees = cursor.fetchall()
        return [dict(fee) for fee in fees]
    except Exception as e:
        print(f"Error getting fees: {e}")
        return []

# ============================================================================
# PLACEMENT MANAGEMENT
# ============================================================================

def predict_placement_eligibility(user_id: int) -> Dict:
    """Predict placement eligibility based on performance"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get latest performance metrics
            cursor.execute('''
                SELECT sgpa, cgpa, attendance_percentage, placement_eligible
                FROM performance_metrics WHERE user_id = ?
                ORDER BY semester DESC LIMIT 1
            ''', (user_id,))
            
            metrics = cursor.fetchone()
            
            if metrics:
                return {
                    'sgpa': metrics['sgpa'],
                    'cgpa': metrics['cgpa'],
                    'attendance': metrics['attendance_percentage'],
                    'eligible': metrics['placement_eligible'],
                    'eligibility_score': (metrics['sgpa'] * 0.6 + metrics['attendance_percentage']/100 * 0.4) if metrics['sgpa'] else 0
                }
            return {'eligible': False, 'eligibility_score': 0}
    except Exception as e:
        print(f"Error predicting placement: {e}")
        return {'eligible': False}

# ============================================================================
# ANALYTICS & REPORTING
# ============================================================================

def get_departmental_analytics(department: str) -> Dict:
    """Get analytics for a department"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Total students
            cursor.execute('''
                SELECT COUNT(*) as count FROM student_profiles WHERE department = ?
            ''', (department,))
            total_students = cursor.fetchone()['count']
            
            # Average CGPA
            cursor.execute('''
                SELECT AVG(cgpa) as avg_cgpa FROM student_profiles WHERE department = ?
            ''', (department,))
            avg_cgpa = cursor.fetchone()['avg_cgpa'] or 0
            
            # Pass percentage (Grade != F)
            cursor.execute('''
                SELECT COUNT(*) as pass_count FROM academic_marks am
                JOIN student_profiles sp ON am.user_id = sp.user_id
                WHERE sp.department = ? AND am.grade != 'F'
            ''', (department,))
            pass_count = cursor.fetchone()['pass_count']
            
            cursor.execute('''
                SELECT COUNT(*) as total_marks FROM academic_marks am
                JOIN student_profiles sp ON am.user_id = sp.user_id
                WHERE sp.department = ?
            ''', (department,))
            total_marks = cursor.fetchone()['total_marks']
            
            pass_percentage = (pass_count / total_marks * 100) if total_marks > 0 else 0
            
            return {
                'total_students': total_students,
                'avg_cgpa': round(avg_cgpa, 2),
                'pass_percentage': round(pass_percentage, 2),
                'fail_percentage': round(100 - pass_percentage, 2)
            }
    except Exception as e:
        print(f"Error getting analytics: {e}")
        return {}
