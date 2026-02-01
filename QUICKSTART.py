#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start Guide - Unified Service Management Portal
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║         Unified Service Management Portal - Quick Start Guide             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎓 WELCOME TO THE PORTAL!

This is a comprehensive service management system for educational institutions
built with Python and Streamlit. The system supports role-based access for both
students and administrators.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 PROJECT STRUCTURE:

📁 drmeghnaadsahu_10/
├── 📄 app.py                    → Main application entry point
├── 📄 init_app.py              → Database initialization
├── 📄 setup.py                 → Environment setup script
├── 📄 requirements.txt          → Python dependencies
├── 📄 README.md                → Comprehensive documentation
├── 📄 COMMIT_STRATEGY.md       → Git commit guide
│
├── 📁 modules/
│   ├── 📄 database.py          → SQLite database operations
│   └── 📄 auth.py              → Authentication & session management
│
├── 📁 pages/
│   ├── 📄 auth_page.py         → Login/Registration interface
│   ├── 📄 student_dashboard.py → Student interface
│   └── 📄 admin_dashboard.py   → Admin interface
│
├── 📁 data/
│   └── 📄 portal.db (auto-created) → SQLite database
│
└── 📁 assets/                  → Static files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  INSTALLATION & SETUP:

Option 1: Automated Setup (Recommended)
────────────────────────────────────────
1. Open PowerShell/Terminal in project directory
2. Run: python setup.py

Option 2: Manual Setup
──────────────────────
1. Create virtual environment:
   python -m venv venv
   venv\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Initialize database:
   python init_app.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 RUNNING THE APPLICATION:

1. Activate virtual environment (if not done):
   venv\\Scripts\\activate

2. Run Streamlit app:
   streamlit run app.py

3. Browser will open to: http://localhost:8501

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 DEMO ACCOUNTS:

Student Account:
  Email: student@example.com
  Password: student123

Admin Account:
  Email: admin@example.com
  Password: admin123

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 FEATURES:

Student Features:
  ✅ Dashboard with quick statistics
  ✅ Complete profile management
  ✅ Submit and track service requests
  ✅ Admission and semester registration
  ✅ Exam form registration
  ✅ Support ticket submission

Admin Features:
  ✅ System overview dashboard
  ✅ Service request management with filtering
  ✅ Support ticket management
  ✅ Admission request reviews
  ✅ Advanced analytics and reports
  ✅ Real-time statistics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 REQUEST CATEGORIES:

• Academic         - General academic issues
• Admission        - Admission and registration
• Exam             - Exam-related requests
• General          - General inquiries
• Technical Support - Technical issues

Priority Levels: Low, Medium, High
Status Workflow: Submitted → In Progress → Resolved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 TECHNOLOGY STACK:

Frontend:     Streamlit
Backend:      Python 3.8+
Database:     SQLite
Visualization: Plotly
Data:         Pandas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 TROUBLESHOOTING:

Issue: "Module not found"
→ Ensure you've run: pip install -r requirements.txt

Issue: "Database error"
→ Delete data/portal.db and run: python init_app.py

Issue: "Streamlit won't load"
→ Clear browser cache and restart server

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 USEFUL COMMANDS:

# Run tests/check setup
python init_app.py

# View git commit history
git log --oneline

# Deploy on Streamlit Cloud
# Push to GitHub and connect in Streamlit Cloud dashboard

# Docker deployment
docker build -t service-portal .
docker run -p 8501:8501 service-portal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ NEXT STEPS:

1. Review the complete README.md for detailed documentation
2. Check COMMIT_STRATEGY.md for git workflow
3. Run the application and test with demo accounts
4. Customize with your institution's details
5. Deploy to production environment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ NEED HELP?

1. Check README.md for comprehensive documentation
2. Review source code comments
3. Check Streamlit documentation: https://docs.streamlit.io
4. Contact development team

╔════════════════════════════════════════════════════════════════════════════╗
║                        Happy Building! 🚀 🎓                              ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
