# Studio Caju Frontend Components

This document provides detailed information about the components used in the Studio Caju frontend application.

## UI Components

### FormInput

**File:** `src/components/FormInput.tsx`

A reusable form input component that integrates with React Hook Form for validation and state management.

**Props:**
- `label`: Input field label text
- `name`: Input field name (used for form registration)
- `type`: Input type (text, password, email, etc.)
- `placeholder`: Placeholder text
- `register`: React Hook Form register function
- `errors`: Form validation errors object
- `required`: Whether the field is required
- `pattern`: Regex pattern for validation
- `validationMessage`: Custom validation error message

**Usage Example:**
```tsx
<FormInput
  label="Email"
  name="email"
  type="email"
  placeholder="youremail@example.com"
  register={register}
  errors={errors}
  required="Email is required"
  pattern={{
    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
    message: "Invalid email address"
  }}
/>
```

### QontrollaLogo

**File:** `src/components/QontrollaLogo.tsx`

Component that renders the application logo.

**Props:**
- `className`: Optional CSS classes to apply to the logo

**Usage Example:**
```tsx
<QontrollaLogo className="w-40 h-40" />
```

## Pages

### SignUpPage

**File:** `src/pages/SignUpPage.tsx`

The tenant registration page allows users to create a new tenant account with an admin user.

**Features:**
- Form for tenant information (name, domain)
- Form for admin user credentials (email, password)
- Form validation using React Hook Form
- API integration with tenant registration service
- Error handling for API responses
- Loading state management
- Success feedback

**State Management:**
- Form data validation
- Form submission state
- API error handling

**Dependencies:**
- React Hook Form for form management
- Axios for API requests
- Framer Motion for animations
- TailwindCSS and DaisyUI for styling

## Service Integration

Components interact with backend services through the service layer:

### Tenant Service Integration

The SignUpPage component uses the `registerTenant` function from `tenantService.ts` to submit tenant registration data to the API.

## Styling Pattern

Components in the application follow these styling patterns:

1. **TailwindCSS Utility Classes**: Primary styling method
2. **DaisyUI Components**: Used for pre-styled UI elements
3. **Custom CSS**: Limited use for specific styling not covered by Tailwind

## Best Practices

When creating new components:

1. Keep components focused on a single responsibility
2. Use TypeScript interfaces to define props
3. Follow existing naming conventions
4. Implement proper error handling
5. Follow the existing styling patterns
6. Add comprehensive prop validation
7. Document component usage 