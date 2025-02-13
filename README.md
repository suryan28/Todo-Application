# Django Todo Application

## Introduction

This is a simple Todo application built using Django, a high-level Python web framework. It allows users to register, log in, and manage their tasks.

## Features

- **User authentication:** Users can register for an account and log in securely.
- **Task management:** Users can create, update, and delete tasks.
- **Responsive design:** The application is designed to work seamlessly across different devices.

## Technologies Used

- Python
- Django
- HTML
- CSS
- Bootstrap

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cis-suryan/todo-list-manager.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd todoapp
   ```
3. **Create virtual environment:**
   ```bash
   virtualenv -p python3.8 env_name
   ```
4. **Activate virtual environment:**
   ```bash
   source env_name/bin/activate
   ```
5. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
6. **Apply migrations to set up the database:**
   ```bash
   python manage.py migrate
   ```
7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
8. **Access the application in your web browser at:** `http://localhost:8000`.

## Usage

1. **Register for an account** by providing your username, email, and password.
2. **Log in** using your credentials.
3. Once logged in, you can **create new tasks** by entering a title and clicking the "Add" button.
4. **Update or delete** existing tasks using the provided options.
5. **Log out** when you're done using the application.

