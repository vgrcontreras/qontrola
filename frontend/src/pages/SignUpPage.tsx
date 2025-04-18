import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle2, AlertCircle } from 'lucide-react';
import QontrollaLogo from '../components/QontrollaLogo';
import FormInput from '../components/FormInput';
import tenantService, { TenantRegistration } from '../services/tenantService';

interface SignUpFormValues {
  companyName: string;
  domain: string;
  email: string;
  password: string;
  acceptTerms: boolean;
}

const SignUpPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors } 
  } = useForm<SignUpFormValues>({
    mode: 'onBlur' // Validates on blur to show red borders immediately
  });
  
  const onSubmit = async (data: SignUpFormValues) => {
    if (!data.acceptTerms) {
      return;
    }
    
    setIsLoading(true);
    setErrorMessage('');
    setSuccessMessage('');
    
    try {
      // Transform form data to match the API expected format
      const tenantData: TenantRegistration = {
        name: data.companyName,
        domain: data.domain,
        admin_user: {
          email: data.email,
          password: data.password
        }
      };
      
      const result = await tenantService.registerTenant(tenantData);
      setSuccessMessage(`Sua conta foi criada com sucesso!`);
    } catch (error: any) {
      setErrorMessage('Falha ao criar conta. Por favor, tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen bg-royal-blue-light flex flex-col items-center justify-center p-4 md:p-6">
      <div className="w-full max-w-md md:max-w-lg">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-6 flex justify-center"
        >
          <QontrollaLogo />
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="bg-white rounded-xl shadow-large p-6 md:p-8"
        >
          <h3 className="text-3xl font-semibold text-neutral-darker text-center mb-2">Criar Conta</h3>
          <p className="text-neutral-dark text-center mb-6">Junte-se a milhares de profissionais criativos</p>
          
          {successMessage && (
            <div className="mb-6 p-3 bg-success/10 text-success rounded-lg flex items-start gap-2">
              <CheckCircle2 className="mt-0.5" size={18} />
              <span>{successMessage}</span>
            </div>
          )}
          
          {errorMessage && (
            <div className="mb-6 p-3 bg-error/10 text-error rounded-lg flex items-start gap-2">
              <AlertCircle className="mt-0.5" size={18} />
              <span>{errorMessage}</span>
            </div>
          )}
          
          <form onSubmit={handleSubmit(onSubmit)}>
            <FormInput
              label="Empresa"
              placeholder="Nome da sua empresa"
              animationDelay={1}
              {...register('companyName', { 
                required: true,
                minLength: 2
              })}
              error={errors.companyName ? "" : ""}
              className={errors.companyName ? "border-error focus:ring-error/50" : ""}
            />
            
            <div className="mb-4 animate-fade-in-up animate-delay-2">
              <label className="form-label">Domínio</label>
              <div className="flex">
                <div className="relative flex-1">
                  <input
                    type="text"
                    placeholder="sua-empresa"
                    className={`form-input rounded-r-none ${errors.domain ? 'border-error focus:ring-error/50' : ''}`}
                    {...register('domain', { 
                      required: true,
                      pattern: /^[a-z0-9-]+$/
                    })}
                  />
                </div>
                <div className="bg-neutral-lighter border border-l-0 border-input-border rounded-r-md flex items-center px-3 text-neutral-dark">
                  <span>.qontrolla.com</span>
                </div>
              </div>
            </div>
            
            <FormInput
              label="Email"
              type="email"
              placeholder="voce@exemplo.com"
              animationDelay={3}
              {...register('email', { 
                required: true,
                pattern: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i
              })}
              error={errors.email ? "" : ""}
              className={errors.email ? "border-error focus:ring-error/50" : ""}
            />
            
            <FormInput
              label="Senha"
              type="password"
              placeholder="Escolha uma senha segura"
              animationDelay={4}
              {...register('password', { 
                required: true,
                minLength: 6
              })}
              error={errors.password ? "" : ""}
              className={errors.password ? "border-error focus:ring-error/50" : ""}
            />
            
            <div className="mb-6 animate-fade-in-up animate-delay-4">
              <div className="flex items-start gap-2">
                <input
                  type="checkbox"
                  id="acceptTerms"
                  className={`mt-1 ${errors.acceptTerms ? 'outline-error' : ''}`}
                  {...register('acceptTerms', { 
                    required: true
                  })}
                />
                <label htmlFor="acceptTerms" className="text-sm text-neutral-dark">
                  Eu aceito os <a href="#" className="text-royal-blue hover:underline">Termos de Serviço</a> e a <a href="#" className="text-royal-blue hover:underline">Política de Privacidade</a>
                </label>
              </div>
            </div>
            
            <button
              type="submit"
              disabled={isLoading}
              className="gradient-btn w-full flex items-center justify-center gap-2 animate-fade-in-up animate-delay-4"
            >
              {isLoading ? 'Criando Conta...' : 'Criar Conta Agora'}
              {!isLoading && <ArrowRight size={18} />}
            </button>
          </form>
          
          <div className="mt-6 text-center text-neutral-dark animate-fade-in-up animate-delay-4">
            Já tem uma conta? <Link to="/login" className="text-royal-blue font-medium hover:underline">Entrar</Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default SignUpPage; 