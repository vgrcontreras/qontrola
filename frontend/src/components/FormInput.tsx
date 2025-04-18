import React, { useState, InputHTMLAttributes, forwardRef } from 'react';
import { Eye, EyeOff } from 'lucide-react';

interface FormInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  animationDelay?: number;
}

const FormInput = forwardRef<HTMLInputElement, FormInputProps>(
  ({ label, error, type = 'text', className = '', animationDelay = 0, ...props }, ref) => {
    const [showPassword, setShowPassword] = useState(false);
    const inputType = type === 'password' && showPassword ? 'text' : type;
    const delayClass = animationDelay ? `animate-delay-${animationDelay}` : '';
    
    return (
      <div className={`mb-4 animate-fade-in-up ${delayClass}`}>
        {label && (
          <label className="form-label">{label}</label>
        )}
        
        <div className="relative">
          <input
            ref={ref}
            type={inputType}
            className={`form-input ${className}`}
            {...props}
          />
          
          {type === 'password' && (
            <button
              type="button"
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-neutral-dark hover:text-neutral-darker transition-colors"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? 'Esconder senha' : 'Mostrar senha'}
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          )}
        </div>
      </div>
    );
  }
);

FormInput.displayName = 'FormInput';

export default FormInput; 