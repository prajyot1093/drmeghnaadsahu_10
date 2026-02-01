# Unified Service Management Portal

🎓 A comprehensive web-based service management system for educational institutions, built with Python and Streamlit.

## Features

### 👨‍🎓 Student Features
- **Dashboard**: Overview of submitted requests and quick statistics
- **Profile Management**: Complete academic profile with personal details
- **Service Requests**: Submit and track requests (Academic, Admission, Exam, etc.)
- **Admission & Registration**: Apply for semester advancement
- **Exam Registration**: Register for exams and manage exam forms
- **Support Tickets**: Create and track support tickets for technical issues

### 👨‍💼 Admin Features
- **Dashboard**: Real-time overview of all requests and system statistics
- **Service Requests Management**: View, filter, and update request status
- **Tickets Management**: Manage all support tickets
- **Admission Requests**: Review and approve admission applications
- **Analytics & Reports**: Comprehensive visualizations and insights
- **Advanced Filtering**: Filter by status, category, priority, and date

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Visualization**: Plotly
- **Data Processing**: Pandas

## Project Structure

```
drmeghnaadsahu_10/
├── app.py                      # Main application entry point
├── init_app.py                 # Initialization script with demo data
├── requirements.txt            # Python dependencies
├── modules/
│   ├── database.py            # Database operations
│   └── auth.py                # Authentication and session management
├── pages/
│   ├── auth_page.py           # Login and registration
│   ├── student_dashboard.py   # Student interface
│   └── admin_dashboard.py     # Admin interface
├── data/
│   └── portal.db              # SQLite database (auto-created)
└── assets/                    # Static files and resources
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or navigate to the project directory**
```bash
cd drmeghnaadsahu_10
```

2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the application with demo data**
```bash
python init_app.py
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Demo Credentials

### Student Account
- **Email**: student@example.com
- **Password**: student123

### Admin Account
- **Email**: admin@example.com
- **Password**: admin123

## Key Features in Detail

### Role-Based Access Control
- Separate dashboards for Students and Admins
- Session-based authentication
- Secure password storage
- Role-based navigation

### Service Request Lifecycle
- **Submitted**: Initial status when request is created
- **In Progress**: Admin is working on the request
- **Resolved**: Request has been completed

### Request Categories
- Academic
- Admission
- Exam
- General
- Technical Support

### Priority Levels
- Low
- Medium
- High

### Admin Dashboard Features
- Real-time statistics and metrics
- Status distribution pie charts
- Request timeline visualization
- Category-wise and priority-wise analysis
- Advanced filtering system
- Batch status updates

## Database Schema

### Users Table
- user_id (Primary Key)
- email (Unique)
- password
- full_name
- role (student/admin)
- created_at

### Student Profiles Table
- profile_id
- user_id (Foreign Key)
- roll_number
- department
- semester
- cgpa
- Academic and personal details

### Service Requests Table
- request_id
- user_id (Foreign Key)
- title, description
- category, priority
- status
- created_at, updated_at

### Tickets Table
- ticket_id
- user_id (Foreign Key)
- title, description
- category, priority
- status
- created_at, resolved_at

### Admission Registrations Table
- registration_id
- user_id (Foreign Key)
- current_sem, desired_sem
- status
- submitted_at, approved_at

### Exam Registrations Table
- exam_id
- user_id (Foreign Key)
- exam_name, exam_date
- subject
- status
- registered_at

## Workflow & User Stories

### Student Workflow
1. Login with credentials
2. Complete/update profile with academic details
3. Submit service requests for various needs
4. Track request status in real-time
5. Apply for admission/semester advancement
6. Register for exams
7. Submit support tickets for issues

### Admin Workflow
1. Login with admin credentials
2. View dashboard with system statistics
3. Filter and search service requests
4. Update request status
5. Manage support tickets
6. View analytics and reports
7. Monitor system usage patterns

## Future Enhancements

- Email notifications for status updates
- Document upload capability
- Advanced scheduling and calendar integration
- Payment gateway for fee submission
- Mobile application
- API development for third-party integration
- Analytics export to PDF/Excel
- Multi-language support
- Two-factor authentication

## API Documentation

All operations are managed through the database module:

```python
from modules.database import *

# User operations
get_user(email, password)
add_user(email, password, full_name, role)

# Profile operations
get_student_profile(user_id)
update_student_profile(user_id, profile_data)

# Request operations
submit_service_request(user_id, title, description, category, priority)
get_user_requests(user_id)
get_all_requests(filters)
update_request_status(request_id, status)

# Ticket operations
submit_ticket(user_id, title, description, category, priority)
get_user_tickets(user_id)
get_all_tickets(filters)
```

## Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set up environment variables if needed
4. Deploy

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

Build and run:
```bash
docker build -t service-portal .
docker run -p 8501:8501 service-portal
```

## Troubleshooting

### Database Connection Error
- Ensure `data` directory exists and is writable
- Check SQLite installation

### Streamlit Not Loading
- Clear browser cache
- Restart Streamlit server
- Check Python version compatibility

### Authentication Issues
- Verify demo credentials
- Clear session cache

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an GitHub issue or contact the development team.

---

**Status**: Active Development 🚀
**Last Updated**: February 2026
**Version**: 1.0.0
