import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'portal.db')

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Student Profile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            roll_number TEXT UNIQUE,
            department TEXT,
            semester INTEGER,
            cgpa REAL,
            phone TEXT,
            address TEXT,
            father_name TEXT,
            mother_name TEXT,
            dob TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Service Requests table
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
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Admission Registration table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admission_registrations (
            registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            current_sem INTEGER NOT NULL,
            desired_sem INTEGER NOT NULL,
            cgpa_required REAL,
            status TEXT DEFAULT 'Pending',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Exam Registration table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exam_registrations (
            exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exam_name TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            subject TEXT NOT NULL,
            status TEXT DEFAULT 'Submitted',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Tickets table
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
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(email: str, password: str, full_name: str, role: str) -> bool:
    """Add new user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (email, password, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', (email, password, full_name, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(email: str, password: str) -> Optional[Dict]:
    """Get user by email and password"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ? AND password = ?
    ''', (email, password))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def update_student_profile(user_id: int, profile_data: Dict) -> bool:
    """Update student profile"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE student_profiles SET
            roll_number = ?, department = ?, semester = ?, cgpa = ?,
            phone = ?, address = ?, father_name = ?, mother_name = ?, dob = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (
            profile_data.get('roll_number'),
            profile_data.get('department'),
            profile_data.get('semester'),
            profile_data.get('cgpa'),
            profile_data.get('phone'),
            profile_data.get('address'),
            profile_data.get('father_name'),
            profile_data.get('mother_name'),
            profile_data.get('dob'),
            user_id
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False

def get_student_profile(user_id: int) -> Optional[Dict]:
    """Get student profile"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM student_profiles WHERE user_id = ?
    ''', (user_id,))
    profile = cursor.fetchone()
    conn.close()
    return dict(profile) if profile else None

def submit_service_request(user_id: int, title: str, description: str, 
                          category: str, priority: str) -> bool:
    """Submit new service request"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_requests 
            (user_id, title, description, category, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, title, description, category, priority))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error submitting request: {e}")
        return False

def get_user_requests(user_id: int) -> List[Dict]:
    """Get all requests for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM service_requests WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))
    requests = cursor.fetchall()
    conn.close()
    return [dict(req) for req in requests]

def get_all_requests(filters: Dict = None) -> List[Dict]:
    """Get all requests with optional filters"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT sr.*, u.full_name, u.email FROM service_requests sr
        JOIN users u ON sr.user_id = u.user_id
        WHERE 1=1
    '''
    params = []
    
    if filters:
        if filters.get('status'):
            query += ' AND sr.status = ?'
            params.append(filters['status'])
        if filters.get('category'):
            query += ' AND sr.category = ?'
            params.append(filters['category'])
        if filters.get('priority'):
            query += ' AND sr.priority = ?'
            params.append(filters['priority'])
    
    query += ' ORDER BY sr.created_at DESC'
    
    cursor.execute(query, params)
    requests = cursor.fetchall()
    conn.close()
    return [dict(req) for req in requests]

def update_request_status(request_id: int, status: str) -> bool:
    """Update request status"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE service_requests 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE request_id = ?
        ''', (status, request_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating status: {e}")
        return False

def get_request_stats() -> Dict:
    """Get request statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT status, COUNT(*) as count FROM service_requests
        GROUP BY status
    ''')
    stats = {row['status']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    return stats

def submit_ticket(user_id: int, title: str, description: str, 
                 category: str, priority: str) -> bool:
    """Submit support ticket"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets 
            (user_id, title, description, category, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, title, description, category, priority))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error submitting ticket: {e}")
        return False

def get_user_tickets(user_id: int) -> List[Dict]:
    """Get all tickets for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tickets WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))
    tickets = cursor.fetchall()
    conn.close()
    return [dict(ticket) for ticket in tickets]

def get_all_tickets(filters: Dict = None) -> List[Dict]:
    """Get all tickets with optional filters"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT t.*, u.full_name, u.email FROM tickets t
        JOIN users u ON t.user_id = u.user_id
        WHERE 1=1
    '''
    params = []
    
    if filters:
        if filters.get('status'):
            query += ' AND t.status = ?'
            params.append(filters['status'])
        if filters.get('category'):
            query += ' AND t.category = ?'
            params.append(filters['category'])
        if filters.get('priority'):
            query += ' AND t.priority = ?'
            params.append(filters['priority'])
    
    query += ' ORDER BY t.created_at DESC'
    
    cursor.execute(query, params)
    tickets = cursor.fetchall()
    conn.close()
    return [dict(ticket) for ticket in tickets]
