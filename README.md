# Team Task Manager

A production-ready role-based task management system built with Flask, SQLAlchemy, and SQLite3. Features comprehensive CRUD operations, priority management, and role-based access control for teams.

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [User Roles & Permissions](#user-roles--permissions)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Security Features](#security-features)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **Role-Based Authentication System**
  - Secure user registration and login
  - Session management with Flask-Login
  - Password hashing with Werkzeug
  
- **Task Management**
  - Full CRUD operations (Create, Read, Update, Delete)
  - Task priority levels (Low, Medium, High, Urgent)
  - Task status tracking (Pending, In Progress, Completed, Cancelled)
  - Due date management
  
- **Role-Based Access Control (RBAC)**
  - **Admin Role**: View all tasks, assign tasks to members, manage users
  - **Member Role**: Full CRUD on owned/assigned tasks
  
- **User Interface**
  - Responsive Bootstrap 5 design
  - Intuitive dashboards for both roles
  - Real-time form validation
  - Flash messaging for user feedback

## 🔧 System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- SQLite3 (included with Python)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/team-task-manager.git
cd team-task-manager
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///instance/database.db
```

**⚠️ Important**: Generate a secure secret key for production:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Initialize Database

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

## ⚙️ Configuration

The application uses different configurations for development and production environments defined in `config.py`:

### Development Configuration
- Debug mode enabled
- SQLite database in `instance/` folder
- Verbose error messages

### Production Configuration
- Debug mode disabled
- Environment-based secret key
- Database connection pooling
- Error logging enabled

## 🚀 Running the Application

### Development Server

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`

### Production Server

Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

## 📁 Project Structure

```
team_task_manager/
│
├── app/                        # Main application package
│   ├── __init__.py            # Flask app factory
│   ├── models.py              # Database models (User, Task)
│   ├── auth.py                # Authentication routes
│   ├── tasks.py               # Task management routes
│   ├── admin.py               # Admin-specific routes
│   ├── decorators.py          # Custom decorators (authorization)
│   ├── forms.py               # WTForms for validation
│   │
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── base.html          # Base template
│   │   ├── login.html         # Login page
│   │   ├── register.html      # Registration page
│   │   ├── dashboard.html     # User dashboard
│   │   ├── tasks/             # Task templates
│   │   │   ├── list.html
│   │   │   ├── create.html
│   │   │   ├── edit.html
│   │   │   └── view.html
│   │   └── admin/             # Admin templates
│   │       ├── dashboard.html
│   │       ├── users.html
│   │       └── assign_task.html
│   │
│   └── static/                # Static files
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
│
├── instance/                  # Instance-specific files
│   └── database.db           # SQLite database (auto-generated)
│
├── config.py                  # Configuration settings
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in git)
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 👥 User Roles & Permissions

### Admin Role

| Permission | Description |
|------------|-------------|
| View All Tasks | Read-only access to all tasks in the system |
| Assign Tasks | Assign tasks to any member |
| Manage Users | Create, edit, and deactivate user accounts |
| View Dashboard | Access to system-wide analytics |

**❌ Admins CANNOT:**
- Modify task content (title, description, priority)
- Delete tasks
- Perform CRUD operations on tasks

### Member Role

| Permission | Description |
|------------|-------------|
| Create Tasks | Create new tasks |
| View Own Tasks | View tasks created by or assigned to them |
| Edit Own Tasks | Modify tasks they own or are assigned to |
| Delete Own Tasks | Delete tasks they created or are assigned to |
| Update Status | Change task status and priority |

**❌ Members CANNOT:**
- View other members' tasks
- Assign tasks to others
- Access user management
- View admin dashboard

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'member',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_by INTEGER NOT NULL,
    assigned_to INTEGER,
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);
```

### Enumerations

**Priority Levels:**
- `low`
- `medium`
- `high`
- `urgent`

**Task Status:**
- `pending`
- `in_progress`
- `completed`
- `cancelled`

**User Roles:**
- `admin`
- `member`

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/register` | Display registration form | No |
| POST | `/register` | Create new user account | No |
| GET | `/login` | Display login form | No |
| POST | `/login` | Authenticate user | No |
| GET | `/logout` | End user session | Yes |

### Tasks (Member)

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| GET | `/tasks` | List user's tasks | Member |
| GET | `/tasks/create` | Display task creation form | Member |
| POST | `/tasks/create` | Create new task | Member |
| GET | `/tasks/<id>` | View task details | Member |
| GET | `/tasks/<id>/edit` | Display edit form | Member |
| POST | `/tasks/<id>/edit` | Update task | Member |
| POST | `/tasks/<id>/delete` | Delete task | Member |

### Admin

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| GET | `/admin/dashboard` | Admin overview | Admin |
| GET | `/admin/tasks` | View all tasks | Admin |
| GET | `/admin/users` | User management | Admin |
| POST | `/admin/assign` | Assign task to member | Admin |

## 🔐 Security Features

### Implemented Security Measures

1. **Password Security**
   - Passwords hashed using Werkzeug's `generate_password_hash`
   - bcrypt algorithm with salt rounds
   - Never stored in plain text

2. **CSRF Protection**
   - Flask-WTF CSRF tokens on all forms
   - Validates token on form submission
   - Prevents cross-site request forgery attacks

3. **SQL Injection Prevention**
   - SQLAlchemy ORM with parameterized queries
   - No raw SQL execution
   - Input sanitization

4. **Session Security**
   - Secure session cookies
   - HTTPOnly flag enabled
   - Session timeout configuration

5. **Authorization**
   - Decorator-based access control
   - Role verification on protected routes
   - Ownership validation for task operations

6. **Input Validation**
   - Server-side validation with WTForms
   - Type checking and length constraints
   - XSS prevention through template escaping

### Security Best Practices

```python
# Example: Password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Store
user.password_hash = generate_password_hash(password)

# Verify
check_password_hash(user.password_hash, password)
```

## 🧪 Testing

### Running Tests

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Test Structure

```
tests/
├── test_auth.py           # Authentication tests
├── test_tasks.py          # Task CRUD tests
├── test_admin.py          # Admin functionality tests
├── test_models.py         # Database model tests
└── conftest.py            # Test fixtures
```

## 🚢 Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production` in environment
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up HTTPS with SSL certificate
- [ ] Configure reverse proxy (Nginx/Apache)
- [ ] Set up logging and monitoring
- [ ] Enable database backups
- [ ] Configure firewall rules
- [ ] Set up error tracking (Sentry)

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

```bash
# Build and run
docker build -t team-task-manager .
docker run -p 8000:8000 team-task-manager
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/yourusername/team-task-manager/issues)
- **Email**: support@yourdomain.com
- **Documentation**: [Wiki](https://github.com/yourusername/team-task-manager/wiki)

## 🙏 Acknowledgments

- Flask framework and community
- SQLAlchemy ORM
- Bootstrap for UI components
- Contributors and testers

---

**Built with ❤️ using Flask**

Version: 1.0.0 | Last Updated: November 2025
