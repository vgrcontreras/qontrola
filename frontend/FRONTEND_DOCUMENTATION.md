# Studio Caju Frontend Documentation

## Overview

Studio Caju frontend is a modern React application built with TypeScript, Vite, and TailwindCSS. The application provides a user interface for tenant registration and management.

## Tech Stack

- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS with DaisyUI
- **Routing**: React Router v6
- **Form Handling**: React Hook Form
- **HTTP Client**: Axios
- **Animation**: Framer Motion
- **Icons**: Lucide React

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── assets/          # Images, fonts, and other assets
│   ├── components/      # Reusable UI components
│   ├── pages/           # Application pages
│   ├── services/        # API services and data fetching
│   ├── styles/          # CSS and style-related files
│   ├── utils/           # Utility functions and helpers
│   ├── App.tsx          # Main application component
│   └── main.tsx         # Application entry point
├── .dockerignore        # Files excluded from Docker builds
├── .gitignore           # Files excluded from Git
├── Dockerfile           # Docker configuration
├── package.json         # Project dependencies and scripts
├── postcss.config.js    # PostCSS configuration
├── tailwind.config.js   # TailwindCSS configuration
├── tsconfig.json        # TypeScript configuration
└── vite.config.ts       # Vite configuration
```

## Components

### Core Components

- **FormInput.tsx**: Reusable form input component with validation support
- **QontrollaLogo.tsx**: Logo component for branding

## Pages

- **SignUpPage.tsx**: Page for tenant registration and admin user creation

## Services

### Tenant Service

The `tenantService.ts` file contains functions for tenant-related API calls:

- `registerTenant`: Registers a new tenant with admin user information

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- npm or yarn package manager

### Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install dependencies:

```bash
npm install
# or
yarn install
```

### Development

To start the development server:

```bash
npm run dev
# or
yarn dev
```

This will start the Vite development server, typically at http://localhost:5173.

### Building for Production

To build the application for production:

```bash
npm run build
# or
yarn build
```

The build artifacts will be stored in the `dist/` directory.

### Preview Production Build

To preview the production build locally:

```bash
npm run preview
# or
yarn preview
```

## Docker

The application includes Docker configuration for containerized deployment:

- **Dockerfile**: Contains instructions for building the container image
- **.dockerignore**: Specifies files to exclude from the Docker build

## Styling

The application uses TailwindCSS with DaisyUI components for styling. The main stylesheet is in `src/styles/index.css`.

## API Integration

The application uses Axios for API requests. API services are organized in the `services` directory, with each service file responsible for a specific domain of API calls.

## Routing

React Router v6 is used for client-side routing. The main routes are defined in `App.tsx`.

## Future Development

Areas for potential expansion:

- User authentication and authorization
- Dashboard for tenant management
- User profile management
- Additional tenant configuration options 