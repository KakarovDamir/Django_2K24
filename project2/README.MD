# Student Management System

Welcome to the Student Management System, a comprehensive API designed to efficiently manage students, courses, attendance, grades, and user roles. This system is built using Django and Django Rest Framework, designed for extendability and ease of use.

## Features

- **User Management**: Register, authenticate, and manage users with roles such as Student, Teacher, and Admin.
- **Student Records**: Create, view, and update student profiles.
- **Course Management**: Manage courses and enroll students.
- **Grading System**: Add and update grades for students.
- **Attendance Tracking**: Record and manage attendance for students in courses.
- **Notification System**: Send emails for key actions like grade updates.
- **Asynchronous Tasks**: Powered by Celery for background task processing.

## Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone 
   cd StudentManagementSystem
   ```

2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** for accessing the admin interface:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Redis server** (ensure Redis is running):
   ```bash
   redis-server
   ```

7. **Run the Celery worker**:
   ```bash
   celery -A StudentManagementSystem worker --loglevel=info
   ```

8. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

### Usage

- Access the API at `http://localhost:8000/`.
- Use the admin panel at `http://localhost:8000/admin/` with your superuser credentials.
- Visit the API documentation (Swagger) at `http://localhost:8000/swagger/`.

## Testing

Run tests to ensure the application components work as expected:
```bash
python manage.py test
```