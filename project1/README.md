# Simple Django Blog Project

This is a simple blogging platform built using Django, which allows users to create, edit, and delete blog posts, comment on posts, and follow other users. The project includes two applications: `blog` for managing blog-related features and `users` for managing user profiles and authentication.

## Features

- User Registration and Authentication
- User Profile Management
- Blog Post Creation, Editing, and Deletion
- Commenting on Posts
- Follow/Unfollow Users
- Simple Search Functionality
- Pagination for Blog Posts

## Requirements

- Python 3.x
- Django (latest stable version)
- A virtual environment for Python (recommended: `venv` or `virtualenv`)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up the Virtual Environment:**

   Create and activate a virtual environment:

   ```bash
   python -m venv myvenv
   myvenv\Scripts\activate
   ```

3. **Install Dependencies:**

   Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

   Note: Create a `requirements.txt` using `pip freeze > requirements.txt` after installing all dependencies.

4. **Apply Migrations:**

   Prepare your database by applying migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser:**

   Create a superuser account to access the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server:**

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

7. **Access the Application:**

   Visit `http://127.0.0.1:8000/` in your web browser to view the application.