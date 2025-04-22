import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { Tenant } from "@/lib/types";
import { TenantAPI } from "@/lib/api";
import { useAuth } from "./AuthContext";

interface TenantContextType {
  tenant: Tenant | null;
  isLoading: boolean;
}

const TenantContext = createContext<TenantContextType>({} as TenantContextType);

export const useTenant = () => useContext(TenantContext);

export function TenantProvider({ children }: { children: ReactNode }) {
  const [tenant, setTenant] = useState<Tenant | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const loadTenant = async () => {
      if (isAuthenticated) {
        try {
          const tenantDomain = localStorage.getItem('tenantDomain');
          if (tenantDomain) {
            const tenantData = await TenantAPI.getCurrent(tenantDomain);
            setTenant(tenantData);
          }
        } catch (err) {
          console.error('Erro ao carregar tenant:', err);
        } finally {
          setIsLoading(false);
        }
      } else {
        setTenant(null);
        setIsLoading(false);
      }
    };
    
    loadTenant();
  }, [isAuthenticated]);

  return (
    <TenantContext.Provider
      value={{
        tenant,
        isLoading
      }}
    >
      {children}
    </TenantContext.Provider>
  );
}
