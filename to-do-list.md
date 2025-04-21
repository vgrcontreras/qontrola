# To-Do List: Building the Task and Finance Management SaaS

This to-do list outlines the steps to develop a multi-tenant SaaS application for freelancers in Brazil to manage projects, tasks, clients, and finances (in BRL). The app uses a shared-database tenancy structure, secure authentication with `pwdlib` and `PyJWT`, and a modern tech stack (FastAPI, React, PostgreSQL).

## Phase 1: Project Setup and Core Infrastructure

### 1.1 Environment Setup
- [x] Initialize project repository on GitHub.
- [x] Set up Poetry for backend dependency management.
  - Install Python 3.12, FastAPI, SQLAlchemy (asyncio), Pydantic, Alembic, AsyncPG, PyJWT, pwdlib, Pytest, Ruff, Coverage.py.
- [ ] Configure Vite for frontend.
  - Install React 18, TypeScript, React Router, React Hook Form, Axios, Framer Motion, Lucide React, Tailwind CSS, DaisyUI.
- [ ] Set up Docker and Docker Compose for local development (PostgreSQL, FastAPI, React).
- [ ] Configure pre-commit hooks with Ruff for linting/formatting.
- [x] Set up MkDocs for API documentation.
- [ ] Configure Taskipy for task automation (e.g., `task test`, `task migrate`).

### 1.2 Database Setup
- [ ] Install and configure PostgreSQL locally via Docker.
- [ ] Create initial database schema using Alembic.
  - Tables: `tenants`, `users`, `refresh_tokens`, `clients`, `categories`, `projects`, `tasks`, `income`, `expenses`.
  - Add `tenant_id` to all tenant-specific tables for shared-database tenancy.
  - Add unique constraint on `categories (tenant_id, name)`.
- [ ] Write SQLAlchemy models for all tables.
- [ ] Test database connectivity with AsyncPG.

### 1.3 Authentication Setup
- [ ] Implement password hashing with `pwdlib` (Argon2).
  - Create utility functions for hashing and verifying passwords.
- [ ] Set up JWT authentication with `PyJWT`.
  - Create functions for generating access tokens (15-min expiry) and refresh tokens (7-day expiry).
- [ ] Implement FastAPI endpoints:
  - `/signup`: Create tenant and admin user, hash password, return access/refresh tokens.
  - `/login`: Verify credentials, return access/refresh tokens, store refresh token in `refresh_tokens`.
  - `/refresh`: Validate refresh token, issue new access token.
- [ ] Create FastAPI middleware to validate `tenant_id` from JWT on all protected routes.
- [ ] Test authentication endpoints with Pytest.

### 1.4 CI/CD Setup
- [ ] Configure GitHub Actions for CI/CD.
  - Run tests (Pytest) and linting (Ruff) on push/pull requests.
  - Build and deploy Docker images to a cloud provider (e.g., Railway, Fly.io) on merge to main.
- [ ] Set up test coverage reporting with Coverage.py (target 80%+ coverage).

## Phase 2: Core Features

### 2.1 Tenant and User Management
- [ ] Implement FastAPI endpoints for tenant management:
  - Update tenant profile (name, logo, address).
  - Get tenant details.
- [ ] Implement user management endpoints (Admin only):
  - Invite team member (create user with Member role).
  - Update/delete user.
- [ ] Create React components for:
  - Tenant profile settings form (React Hook Form, DaisyUI).
  - User management interface (list users, invite form).
- [ ] Enforce role-based access:
  - Admins: Full access.
  - Members: No access to financial data or user management.
- [ ] Test endpoints and UI with Pytest and manual testing.

### 2.2 Client Management
- [ ] Implement FastAPI endpoints:
  - CRUD operations for clients (create, read, update, delete).
  - Filter by `tenant_id`.
- [ ] Create React components:
  - Client list with search/filter (DaisyUI table).
  - Client CRUD forms (React Hook Form).
- [ ] Test endpoints and UI.

### 2.3 Project and Task Management
- [ ] Implement FastAPI endpoints:
  - CRUD for projects (name, description, client_id, status, dates, budget).
  - CRUD for tasks (title, description, status, priority, due_date, assignee_id, hours_spent).
  - Filter by `tenant_id` and project_id (for tasks).
- [ ] Create React components:
  - Project list and CRUD forms.
  - Task Kanban board (drag-and-drop with Framer Motion).
  - Task list view and CRUD forms.
  - Time tracking input for tasks/projects.
- [ ] Implement calendar view using FullCalendar (React).
  - Display task due dates and project deadlines.
- [ ] Enforce role-based access:
  - Members only access assigned tasks/projects.
- [ ] Test endpoints and UI.

### 2.4 Finance Management
- [ ] Implement FastAPI endpoints:
  - CRUD for categories (name, type: income/expense, tenant_id).
  - CRUD for income (amount, date, description, category_id, project_id).
  - CRUD for expenses (amount, date, description, category_id, project_id, receipt_url).
  - Calculate project profitability (income - expenses).
  - Aggregate company-level finances (sum income/expenses).
- [ ] Create React components:
  - Category management interface (CRUD forms).
  - Income/expense entry forms (with category dropdown).
  - Financial overview (project and company level).
- [ ] Integrate AWS S3 for receipt uploads.
- [ ] Enforce role-based access:
  - Admins only for financial data and categories.
- [ ] Test endpoints and UI.

## Phase 3: Reporting and Usability 

### 3.1 Reporting and Analytics
- [ ] Implement FastAPI endpoints:
  - Profit/loss per project (income - expenses).
  - Cash flow (net cash over time).
  - Income/expense by category.
  - Hour value (net profit ÷ hours worked).
- [ ] Create React components:
  - Dashboard with Chart.js (bar for income/expenses, line for cash flow).
  - Report pages with export options (CSV/PDF).
- [ ] Implement PDF generation (e.g., using `reportlab` or `weasyprint`).
- [ ] Test endpoints and UI.


### 3.2 Usability Features
- [ ] Implement search and filter functionality:
  - FastAPI endpoints for searching projects, tasks, clients.
  - React components for search bar and filter dropdowns.
- [ ] Add in-app notifications for due dates (React component).
- [ ] Ensure responsive design with Tailwind CSS/DaisyUI:
  - Test on desktop, tablet, and mobile.
- [ ] Implement data export (CSV) for clients, projects, and financial data.
- [ ] Test usability features.
- **Estimated Duration**: 2 weeks

## Phase 4: Security, Testing, and Deployment (3-4 weeks)

### 4.1 Security
- [ ] Validate tenant isolation:
  - Ensure all SQLAlchemy queries filter by `tenant_id`.
  - Test middleware for `tenant_id` validation.
- [ ] Implement LGPD compliance:
  - Endpoints for data export (CSV) and deletion.
  - Anonymize backups.
- [ ] Harden authentication:
  - Invalidate refresh tokens on logout/password change.
  - Test password hashing with `pwdlib`.
- [ ] Enable encryption:
  - Configure PostgreSQL for encryption at rest.
  - Use TLS for API requests.
- [ ] Test security with Pytest and manual penetration testing.
- **Estimated Duration**: 1.5 weeks

### 4.2 Testing
- [ ] Write Pytest tests for all endpoints:
  - Authentication (signup, login, refresh).
  - CRUD operations for all entities.
  - Role-based access control.
  - Tenant isolation.
- [ ] Achieve 80%+ test coverage (Coverage.py).
- [ ] Perform manual UI testing on multiple devices.
- [ ] Test performance of reporting endpoints with large datasets.
- **Estimated Duration**: 1.5 weeks

### 4.3 Deployment
- [ ] Deploy to cloud provider (e.g., Railway, Fly.io, AWS ECS).
  - Configure PostgreSQL (AWS RDS or similar).
  - Set up S3 for file storage.
- [ ] Configure monitoring (e.g., Sentry for errors, CloudWatch for logs).
- [ ] Set up daily backups with point-in-time recovery.
- [ ] Test deployment and rollback procedures.
- **Estimated Duration**: 1 week

## Phase 5: Feedback and Iteration (Ongoing)

### 5.1 User Testing
- [ ] Recruit 5-10 Brazilian freelancers for beta testing.
- [ ] Collect feedback on usability, features, and performance.
- [ ] Prioritize bug fixes and feature requests.
- **Estimated Duration**: 2 weeks

### 5.2 Iteration
- [ ] Implement high-priority feedback (e.g., UI tweaks, additional filters).
- [ ] Update MkDocs documentation with new features.
- [ ] Monitor adoption metrics (target: 500 tenants in 6 months).
- [ ] Plan additional features (e.g., email notifications, integrations) based on demand.
- **Estimated Duration**: Ongoing

## Total Estimated Duration
- **Core Development (Phases 1-4)**: 17-22 weeks (~4-5.5 months)
- **Initial Feedback (Phase 5)**: 2 weeks
- **Total Initial Build**: ~4.5-6 months

## Notes
- **Team Size**: Assumes 2-3 developers working full-time. Adjust timelines for larger/smaller teams.
- **Parallel Tasks**: Frontend and backend tasks can be developed concurrently to reduce timeline.
- **Testing**: Continuous testing during development reduces Phase 4 workload.
- **Cloud Costs**: Budget for PostgreSQL, S3, and hosting (~$50-100/month initially).
- **Documentation**: Update MkDocs with each feature for developer handoff.

## Next Immediate Steps
1. Create GitHub repository and initialize Poetry/Vite projects.
2. Set up Docker Compose for local PostgreSQL, FastAPI, and React.
3. Define Alembic migrations for initial schema.
4. Implement and test `/signup`, `/login`, and `/refresh` endpoints with `pwdlib` and `PyJWT`.