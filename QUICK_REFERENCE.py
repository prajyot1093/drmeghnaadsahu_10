#!/usr/bin/env python3
"""
UNIFIED SERVICE MANAGEMENT PORTAL
Quick Reference Card for Hackathon Project
"""

QUICK_REFERENCE = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     UNIFIED SERVICE MANAGEMENT PORTAL - QUICK REFERENCE     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🚀 QUICK START (3 STEPS)
━━━━━━━━━━━━━━━━━━━━━━

1. Setup:
   python setup.py

2. Run:
   streamlit run app.py

3. Login:
   Student: student@example.com / student123
   Admin: admin@example.com / admin123

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 KEY FILES
━━━━━━━━━

app.py                    → Main application
modules/auth.py           → Authentication
modules/database.py       → Database operations
pages/student_dashboard.py → Student UI
pages/admin_dashboard.py   → Admin UI
init_app.py              → Database initialization
requirements.txt         → Dependencies

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCUMENTATION
━━━━━━━━━━━━

README.md               Full documentation
TESTING.md              Test cases & procedures
DEPLOYMENT.md           Deployment guide
QUICKSTART.py           Setup instructions
COMMIT_STRATEGY.md      Git workflow
MILESTONES.md           Project timeline
ENHANCEMENTS.md         Future features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ FEATURES
━━━━━━━━━

Student:
  • Dashboard with metrics
  • Profile management
  • Service request tracking
  • Admission registration
  • Exam registration
  • Support tickets

Admin:
  • System overview
  • Request management
  • Advanced filtering
  • Analytics & reports
  • Ticket management
  • Visualizations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️ TECH STACK
━━━━━━━━━━

Frontend: Streamlit
Backend:  Python
Database: SQLite
Charts:   Plotly
Data:     Pandas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 STATUS
━━━━━━

Commits:    8/10 ✅
Progress:   80% ✅
Database:   ✅ Complete
Auth:       ✅ Complete
Student UI: ✅ Complete
Admin UI:   ✅ Complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 COMMON COMMANDS
━━━━━━━━━━━━━━━━

Install:         pip install -r requirements.txt
Initialize DB:   python init_app.py
Run App:         streamlit run app.py
View History:    git log --oneline
Check Files:     ls -la

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ FAQ
━━━━

Q: How to reset database?
A: Delete data/portal.db and run: python init_app.py

Q: Port already in use?
A: Create .streamlit/config.toml and change port

Q: How to test?
A: Read TESTING.md for complete test cases

Q: How to deploy?
A: See DEPLOYMENT.md for all options

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 DATABASE TABLES
━━━━━━━━━━━━━━

1. users              - User accounts
2. student_profiles  - Student info
3. service_requests  - Requests
4. tickets           - Support tickets
5. admission_registrations - Admissions
6. exam_registrations - Exam forms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 REQUEST CATEGORIES
━━━━━━━━━━━━━━━━

• Academic
• Admission
• Exam
• General
• Technical Support

Priority: Low, Medium, High
Status: Submitted, In Progress, Resolved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 NEXT STEPS
━━━━━━━━━━

1. Run application and test features
2. Execute test cases (TESTING.md)
3. Implement Commit 9 enhancements
4. Complete Commit 10 testing
5. Prepare deployment
6. Create presentation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 PROJECT GOALS
━━━━━━━━━━━━━

✅ Functional portal
✅ Role-based access
✅ Complete dashboard
✅ Database management
✅ Comprehensive docs
✅ Production ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 HELP
━━━━

See README.md for complete documentation
Check TESTING.md for test procedures
Review DEPLOYMENT.md for setup options
Examine code comments for details

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃            Ready to Build? Let's Go! 🚀                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

if __name__ == "__main__":
    print(QUICK_REFERENCE)
