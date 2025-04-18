# Qontrolla Sign Up Page

A modern, responsive sign-up page for Qontrolla, designed for creative professionals who want more control over their projects and finances.

## Features

- Clean, modern design following Qontrolla's style guide
- Responsive layout that adapts to different screen sizes
- Smooth animations and transitions
- Form validation with inline error messages
- Password visibility toggle
- Connection to the backend API for tenant registration

## Technology Stack

- React with TypeScript
- Tailwind CSS for styling
- DaisyUI component library
- Framer Motion for animations
- React Hook Form for form validation
- Lucide React for icons

## Getting Started

### Prerequisites

- Node.js 14.x or higher
- npm or yarn

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

The application will be available at http://localhost:3000

### Building for Production

To build the application:

```bash
npm run build
# or
yarn build
```

## Project Structure

- `/src` - Source code
  - `/components` - Reusable React components
  - `/pages` - Page components
  - `/services` - API service functions
  - `/styles` - CSS styles and Tailwind configuration

## Backend Integration

The sign-up page connects to the backend API for tenant registration. The configuration uses a Vite proxy to handle API requests and avoid CORS issues during development.

## Design System

The application follows Qontrolla's design system with:
- Poppins font for typography
- Royal Blue light background
- Gradient buttons using Royal Blue and Ice Cold colors
- Consistent spacing and rounded corners
- Smooth animations and transitions 