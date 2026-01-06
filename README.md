# Capstone News Application

## Project Overview

This is a comprehensive Django-based news application developed as a Capstone project. The system is designed to manage the lifecycle of news articles, from creation by journalists to approval by editors and consumption by readers. It features a robust role-based access control (RBAC) system, subscription management, and a RESTful API.

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
- **Database**: SQLite (default), extensible to PostgreSQL
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

3. **Accessing the App:**
   - **Home**: `http://127.0.0.1:8000/`
   - **Register**: `http://127.0.0.1:8000/users/register/`
   - **Login**: `http://127.0.0.1:8000/users/login/`

### Running Tests
To ensure system stability, run the unit tests:
```bash
python manage.py test
```
# https://github.com/hyperiondev-bootcamps/JO25080018810/tree/main/Level%202%20-%20Introduction%20to%20Software%20Engineering/M06T08%20%E2%80%93%20Capstone%20Project%20%E2%80%93%20News%20Application 
Joshua Martin
