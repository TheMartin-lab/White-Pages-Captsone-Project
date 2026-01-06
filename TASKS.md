# Project Tasks & Progress

Based on the current project status documented in README.md.

## Completed Features

### 1. Role-Based Access Control (RBAC)
- [x] Define User roles: Reader, Journalist, Editor.
- [x] Implement permissions:
  - Reader: View published articles, subscribe.
  - Journalist: Create/Edit own articles.
  - Editor: Approve/Delete all articles.

### 2. Article Management Workflow
- [x] Create Article model with `approved` status.
- [x] Implement Journalist draft creation.
- [x] Implement Editor approval dashboard.
- [x] Implement public/subscribed feeds.

### 3. User Registration & Onboarding
- [x] User registration form with role selection.
- [x] Profile fields (First Name, Last Name).
- [x] Subscription pre-selection for Readers.

### 4. Subscriptions & Feeds
- [x] Publisher model and relationships.
- [x] Personalized "Subscribed Feed" endpoint/view.
- [x] Public Feed for general access.

### 5. API & Integration
- [x] REST API using Django Rest Framework.
- [x] Token Authentication.
- [x] Endpoints: `/api/articles/`, `/api/articles/subscribed/`.

### 6. Infrastructure
- [x] Database Setup (SQLite).
- [x] Unit Tests.
- [x] Seeding Script (`seed_stranger_things`).

## Future / Pending
- [ ] Deployment configuration.
- [ ] Advanced search functionality.
- [ ] Email notifications for newsletters.
