# Task and Finance Management SaaS Application Specification

## Overview

This multi-tenant SaaS application enables freelancers in Brazil to manage projects, tasks, clients, and finances (in BRL) at project and company levels. All tenants share a single PostgreSQL database, with data isolation enforced via a `tenant_id` column. Role-based access control restricts financial data visibility for non-admin users. Passwords are hashed using `pwdlib`, and authentication uses JWT tokens (`PyJWT`) with a refresh token mechanism. The app emphasizes usability, financial transparency with custom categories, and scalability with tiered pricing.

## Key Objectives

- Streamline project and task management for freelancers.
- Provide financial tracking (income/expenses) in BRL with user-defined categories at the company level.
- Support client management with optional project-client associations.
- Deliver actionable reports (e.g., profit/loss, cash flow, hour value).
- Ensure a responsive, intuitive web app with robust security.

## Target Audience

- Freelancers and small freelance teams in Brazil managing multiple projects.
- Users needing flexible financial tracking without client invoicing or portal access.
- Businesses requiring tiered pricing based on projects, clients, and users.

## Tech Stack

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy (with asyncio support)
- Pydantic
- Alembic (database migrations)
- AsyncPG (PostgreSQL driver)
- PyJWT (JWT authentication)
- pwdlib (password hashing)
- Pytest (testing)
- Poetry (package management)
- Ruff (linter/formatter)
- Coverage.py (code coverage)

### Frontend

- React 18
- TypeScript
- React Router
- React Hook Form
- Axios (HTTP client)
- Framer Motion (animations)
- Lucide React (icons)
- Vite (build tool)
- Tailwind CSS
- DaisyUI (Tailwind component library)

### DevOps/Tools

- Pre-commit (Git hooks)
- MkDocs (documentation)
- Taskipy (task runner)
- Docker (containerization)
- GitHub Actions (CI/CD)

## Architecture

- **Multi-Tenant Design**: Shared-database tenancy, with a single PostgreSQL database. Data isolation is enforced by a `tenant_id` column in all tenant-specific tables, with queries filtering by `tenant_id`.
- **Database**: Single PostgreSQL database for all tenants.
- **Authentication**:
  - JWT-based (`PyJWT`) with role-based access (Admin vs. Team Member).
  - Access tokens (short-lived, e.g., 15 minutes) include `tenant_id`, `user_id`, and `role`.
  - Refresh tokens (long-lived, e.g., 7 days) allow token refresh if valid.
  - Passwords hashed using `pwdlib` with a secure algorithm (e.g., Argon2).
- **Hosting**: Cloud-based (e.g., AWS ECS, Railway, or Fly.io) with auto-scaling.
- **File Storage**: AWS S3 for receipts or exported reports.
- **API-First**: FastAPI provides RESTful endpoints, with `tenant_id` validation in middleware.

## Core Features

### 1. Tenant Management

- **Signup/Login**:
  - Freelancers create a tenant (company) with email/password or OAuth (e.g., Google).
  - Passwords are hashed using `pwdlib` (Argon2 algorithm) before storage.
  - The first user is assigned the Admin role.
  - Login returns an access token and refresh token.
- **Token Refresh**:
  - Users can refresh access tokens using a valid refresh token via a `/refresh` endpoint.
  - Refresh tokens are stored in a `refresh_tokens` table and validated before issuing new access tokens.
- **Profile Settings**: Manage company details (name, logo, address).
- **Subscription Plans**: Tiered pricing based on:
  - **Free**: 5 projects, 10 clients, 1 user.
  - **Basic**: 20 projects, 50 clients, 3 users.
  - **Pro**: Unlimited projects/clients, 10 users.
  - Pricing TBD (e.g., Free, R$50/month, R$150/month).
- **User Roles**:
  - **Admin**: Full access to projects, tasks, clients, and financial data.
  - **Team Member**: Access to assigned projects/tasks, no financial data visibility.

### 2. Client Management

- **Client Profiles**: Create/edit/delete clients (name, email, phone, address, notes).
- **Client Association**: Projects can be linked to a client or remain unassociated.
- **No Client Portal**: Clients cannot access the app or view project data.

### 3. Project Management

- **Project Creation**: Details include name, description, client (optional), start/end dates, budget (BRL).
- **Project Status**: Not Started, In Progress, Completed, On Hold.
- **Task Management**:
  - Create tasks (title, description, due date, priority, assignee for team members).
  - Statuses: To Do, In Progress, Done.
  - Views: Kanban board (drag-and-drop) or list view.
- **Time Tracking**: Manual input for hours spent on tasks or total project.
- **Calendar View**: Embedded calendar displaying task due dates and project deadlines.

### 4. Finance Management

- **Currency**: All transactions in BRL.
- **Custom Categories**:
  - Users create custom categories for income and expenses at the company (tenant) level (e.g., "Design Software," "Travel Costs").
  - No default categories; all categories are user-defined.
  - Categories are scoped to each tenant via `tenant_id`, but different tenants can have identical category names (e.g., "Marketing").
- **Project-Level Finances**:
  - **Income**: Log payments or fees (amount, date, description, category).
  - **Expenses**: Log costs (amount, date, category, description, receipt upload).
  - **Profitability**: Calculate profit (income - expenses).
- **Company-Level Finances**:
  - Aggregate income/expenses across projects.
  - Cash flow tracking (monthly/quarterly/yearly).
- **No Invoicing**: Invoicing functionality is excluded.

### 5. Reporting and Analytics

- **Reports**:
  - **Profit/Loss per Project**: Income - expenses.
  - **Cash Flow**: Net cash (income - expenses) over time.
  - **Expenses/Income by Category**: Breakdown by user-defined categories.
  - **Hour Value**: Net profit (income - expenses) ÷ total hours worked per project.
- **Export Options**: CSV or PDF for all reports.
- **Dashboard**: Visual charts (e.g., bar for income/expenses by category, line for cash flow) using Chart.js.

### 6. Usability Features

- **Responsive Design**: Optimized for desktop, tablet, and mobile using Tailwind CSS and DaisyUI.
- **Drag-and-Drop**: Reorder tasks or move between Kanban columns (Framer Motion).
- **Notifications**: In-app alerts for due dates (email notifications optional).
- **Search and Filters**: Search projects, tasks, or clients; filter by status, client, or date.
- **Data Export**: Export clients, projects, or financial data as CSV.

### 7. Security and Compliance

- **Data Isolation**: Enforced via `tenant_id` in all tenant-specific tables. FastAPI middleware validates `tenant_id` on every request.
- **Password Hashing**: User passwords hashed with `pwdlib` (Argon2 algorithm) for secure storage.
- **Authentication**:
  - Access tokens (JWT, 15-minute expiry) include `tenant_id`, `user_id`, and `role`.
  - Refresh tokens (JWT, 7-day expiry) stored in `refresh_tokens` table, invalidated on logout or password change.
  - Token refresh endpoint (`/refresh`) issues new access tokens if refresh token is valid.
- **Encryption**: Data encrypted at rest (PostgreSQL) and in transit (TLS).
- **Compliance**: Adhere to LGPD (Brazil’s data protection law) for data deletion/export.
- **Backups**: Daily backups with point-in-time recovery (AWS RDS or similar).
- **Query Safety**: Use SQLAlchemy’s parameterized queries to prevent tenant data leakage.

## Database Schema (Single Database)

```sql
CREATE TABLE tenants (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP,
    subscription_plan VARCHAR(50)
);

CREATE TABLE users (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255), -- Hashed with pwdlib (Argon2)
    role ENUM('admin', 'member'),
    created_at TIMESTAMP
);

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    token VARCHAR(512), -- JWT refresh token
    expires_at TIMESTAMP,
    created_at TIMESTAMP
);

CREATE TABLE clients (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    notes TEXT
);

CREATE TABLE categories (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255),
    type ENUM('income', 'expense'),
    created_at TIMESTAMP,
    CONSTRAINT unique_category_name_per_tenant UNIQUE (tenant_id, name)
);

CREATE TABLE projects (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    client_id UUID REFERENCES clients(id) NULL,
    name VARCHAR(255),
    description TEXT,
    status ENUM('not_started', 'in_progress', 'completed', 'on_hold'),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15,2)
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    project_id UUID REFERENCES projects(id),
    title VARCHAR(255),
    description TEXT,
    status ENUM('todo', 'in_progress', 'done'),
    priority ENUM('low', 'medium', 'high'),
    due_date DATE,
    assignee_id UUID REFERENCES users(id) NULL,
    hours_spent DECIMAL(10,2)
);

CREATE TABLE income (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    project_id UUID REFERENCES projects(id) NULL,
    category_id UUID REFERENCES categories(id),
    amount DECIMAL(15,2),
    date DATE,
    description TEXT
);

CREATE TABLE expenses (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    project_id UUID REFERENCES projects(id) NULL,
    category_id UUID REFERENCES categories(id),
    amount DECIMAL(15,2),
    date DATE,
    description TEXT,
    receipt_url VARCHAR(255)
);
```

## User Flow Example

 1. **Signup**: Freelancer signs up, creates a tenant, and becomes Admin. Password is hashed with `pwdlib`.
 2. **Login**: Enters credentials, receives access token (15-min expiry) and refresh token (7-day expiry).
 3. **Token Refresh**: If access token expires, uses `/refresh` endpoint with refresh token to get a new access token.
 4. **Team Setup**: Admin invites a team member (e.g., developer) with Member role.
 5. **Category Setup**: Admin creates custom categories (e.g., "Design Tools," "Client Meetings").
 6. **Client Setup**: Adds client (e.g., "Acme Corp").
 7. **Project Creation**: Creates "Website Redesign" project linked to Acme Corp.
 8. **Task Management**: Adds tasks (e.g., "Design Homepage"), assigns to team member, logs 5 hours.
 9. **Financial Tracking**: Admin logs R$1,000 income (category: "Client Savoy") and R$200 expense (category: "Design Tools").
10. **Reporting**: Admin views profit (R$800), hour value (R$800 ÷ 5 = R$160/hour), and category breakdown.

## Development Phases

- **Phase 1: Core Features** (3-4 months)
  - Tenant setup, user roles, client/project/task management, custom category management.
  - Authentication with `pwdlib` for password hashing and `PyJWT` for access/refresh tokens.
  - Responsive UI with Tailwind/DaisyUI, FastAPI backend, single PostgreSQL database with AsyncPG.
- **Phase 2: Financial Features** (2 months)
  - Income/expense tracking with custom categories, reporting (profit/loss, cash flow, hour value).
  - Calendar view and data export (CSV/PDF).
- **Phase 3: Polish and Scale** (1-2 months)
  - Notifications, search/filters, performance optimization.
  - CI/CD with GitHub Actions, documentation with MkDocs.
- **Phase 4: Feedback and Iteration** (ongoing)
  - User testing with Brazilian freelancers, feature enhancements.

## Success Metrics

- **Adoption**: 500 active tenants in Brazil within 6 months.
- **Engagement**: Average 3 projects per tenant within 3 months.
- **Retention**: 85% tenant retention after 6 months.
- **Report Usage**: 70% of tenants export at least one report monthly.

## Risks and Mitigations

- **Risk**: Tenant data leakage in shared database.
  - **Mitigation**: Enforce `tenant_id` filtering in all SQLAlchemy queries; use FastAPI middleware to validate `tenant_id`.
- **Risk**: Weak password hashing.
  - **Mitigation**: Use `pwdlib` with Argon2 for secure, future-proof hashing.
- **Risk**: Refresh token misuse.
  - **Mitigation**: Store refresh tokens in database, invalidate on logout/password change, and enforce expiry.
- **Risk**: LGPD compliance issues.
  - **Mitigation**: Implement data export/deletion endpoints, anonymize backups.

## Next Steps

- Develop wireframes for key screens (dashboard, project view, category management, reports).
- Set up FastAPI project with Poetry, SQLAlchemy, AsyncPG, `pwdlib`, and `PyJWT`.
- Implement authentication with password hashing and token refresh.
- Create a prototype for tenant signup, project/task management, and custom category management.
- Validate with Brazilian freelancers for feedback.