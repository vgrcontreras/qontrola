import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { User } from "@/lib/types";
import { AuthAPI, UserAPI } from "@/lib/api";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadUser = async () => {
      try {
        // Verificar se há um token salvo
        const token = localStorage.getItem('token');
        const tenantDomain = localStorage.getItem('tenantDomain');
        
        if (token && tenantDomain) {
          // Tenta obter os dados do usuário
          const userData = await UserAPI.getCurrentUser(tenantDomain);
          setUser(userData);
        }
      } catch (err) {
        console.error('Erro ao carregar usuário:', err);
        // Limpar o token se ocorrer um erro
        localStorage.removeItem('token');
      } finally {
        setIsLoading(false);
      }
    };
    
    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    setError(null);
    
    try {
      // Obter o domínio do tenant
      const tenantDomain = localStorage.getItem('tenantDomain');
      
      if (!tenantDomain) {
        throw new Error('Domínio do tenant não encontrado');
      }
      
      // Fazer login
      const userData = await AuthAPI.login(tenantDomain, email, password);
      setUser(userData);
      return true;
    } catch (err: any) {
      setError(err.message || "Ocorreu um erro durante o login");
      return false;
    }
  };

  const logout = () => {
    AuthAPI.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        error
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
