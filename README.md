# Capstone News Application

## Project Overview

This is a comprehensive Django-based news application developed as a Capstone project. The system is designed to manage the lifecycle of news articles, from creation by journalists to approval by editors and consumption by readers. It features a robust role-based access control (RBAC) system, subscription management, a RESTful API, and is powered by a production-grade MariaDB database.

## Features & Functions

### 1. Role-Based Access Control (RBAC)
The application defines three distinct user roles with specific permissions:
- **Reader**: Can view published articles, subscribe to publishers or journalists, and manage their own profile. Readers cannot create or edit articles.
- **Journalist**: Can create, update, and delete their own articles. Articles created by journalists are initially marked as unapproved and require editor review.
- **Editor**: Has broad administrative powers. Editors can view all articles (including unapproved ones), approve articles for publication, and delete any article.

### 2. Article Management Workflow
- **Creation**: Journalists write articles which are saved as drafts (unapproved).
- **Approval**: Editors review unapproved articles via a dedicated dashboard and approve them.
- **Publication**: Once approved, articles become visible to Readers and appear in public feeds.

### 3. User Registration & Onboarding
- **Sign Up**: New users can register and select their desired role (Reader, Journalist, Editor).
- **Profile Customization**: Users can set their First Name, Last Name, and other details during registration.
- **Subscription Setup**: During registration, Readers can pre-select subscriptions to recommended Publishers (e.g., "Hawkins Gazette") and Journalists.

### 4. Subscriptions & Feeds
- **Personalized Feed**: Readers have a "Subscribed Feed" showing articles only from the Publishers and Journalists they follow.
- **Public Feed**: A general feed displays all approved articles for non-logged-in users or general browsing.
- **Newsletters**: The system supports creating newsletters that aggregate multiple articles.

### 5. API & Integration
- **REST API**: Built with Django Rest Framework (DRF), exposing endpoints for articles, users, and subscriptions.
- **Token Authentication**: Secure API access using DRF Tokens.
- **Endpoints**:
    - `GET /api/articles/`: List all approved articles.
    - `GET /api/articles/subscribed/`: List articles based on user subscriptions.
    - `POST /api/articles/`: Create new articles (Journalist/Editor only).

## Planning & Architecture

### Tech Stack
- **Backend**: Python, Django 6.0
- **API**: Django Rest Framework (DRF)
- **Database**: MariaDB (Production-grade SQL database)
- **Driver**: PyMySQL (Pure Python MySQL client)
- **Frontend**: Django Templates, Bootstrap 5.1.3
- **Version Control**: Git

### Database Models
- **User**: Extended Custom User model with `role` field and Many-to-Many relationships for subscriptions (`subscriptions_to_publishers`, `subscriptions_to_journalists`).
- **Publisher**: Represents a media house or publication entity.
- **Article**: Core content model with `approved` status, linked to `Author` (User) and `Publisher`.
- **Newsletter**: Aggregates articles for distribution.

### Key Files & Directories
- `news_app/`: Project settings and configuration.
- `articles/`: Logic for article management, views, and API viewsets.
- `users/`: User management, registration views, and role definitions.
- `publications/`: Publisher model and logic.
- `templates/`: HTML templates for the frontend interface.

## Getting Started

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- MariaDB 12.1+ (Installed locally)

### Database Setup
The project is configured to use a local MariaDB instance on port **3307**. Configuration is managed via the `.env` file.

1.  **Initialize Local Database:**
    Use the provided PowerShell script to start the database using the portable `local_db` directory.
    ```powershell
    # Start the local MariaDB server (Portable script)
    .\start_db.ps1
    ```

2.  **Environment Configuration:**
    A `.env` file is included with default development settings. You can modify this file to change database credentials, ports, or secret keys without editing the code.
    ```env
    DB_PORT=3307
    DB_USER=django_user
    DB_PASSWORD=password
    ```

3.  **Configure Database User (First Run Only):**
    The project expects a user `django_user` with password `password` and a database named `capstone_news_db`.
    ```sql
    CREATE DATABASE IF NOT EXISTS capstone_news_db;
    CREATE OR REPLACE USER 'django_user'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON capstone_news_db.* TO 'django_user'@'localhost';
    FLUSH PRIVILEGES;
    ```

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd "Capstone project django"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

### Usage

1. **Seed Initial Data:**
   Populate the database with sample data (Stranger Things articles, publishers, and users).
   ```bash
   python manage.py seed_stranger_things
   ```

2. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

3. **Login Credentials:**
   The seeding script creates the following accounts:
   
   | Role | Username | Password |
   |------|----------|----------|
   | **Superuser** | `admin` | `password123` |
   | **Journalist** | `reporter1` | `news123!` |
   | **Journalist** | `reporter2` | `news123!` |

4. **Accessing the App:**
   - **Home**: `http://127.0.0.1:8000/`
   - **Register**: `http://127.0.0.1:8000/users/register/`
   - **Admin Panel**: `http://127.0.0.1:8000/admin/`

### Running in IDEs

#### Visual Studio (2019/2022)
1.  Open Visual Studio.
2.  Select **"Open a Local Folder"**.
3.  Navigate to and select the project folder.
4.  Visual Studio should automatically detect the Python environment (if not, select it from the dropdown).
5.  Open `manage.py` and click the **Start** button (green play icon) or right-click `manage.py` and select **Start Debugging**.

#### Visual Studio Code
1.  Open the folder in VS Code.
2.  Install the **Python** extension.
3.  Select your Python interpreter (Ctrl+Shift+P -> "Python: Select Interpreter").
4.  Press **F5** to start the server (a `launch.json` is provided).

---

### project repository
https://github.com/hyperiondev-bootcamps/JO25080018810/tree/main/Level%202%20-%20Introduction%20to%20Software%20Engineering/M06T08%20%E2%80%93%20Capstone%20Project%20%E2%80%93%20News%20Application

joshua martin
