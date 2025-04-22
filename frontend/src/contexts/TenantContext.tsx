
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { Tenant } from "@/lib/types";
import { SessionAPI } from "@/lib/storage";
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
  const { user } = useAuth();

  useEffect(() => {
    // Carregar o tenant atual quando o usuário estiver autenticado
    if (user) {
      const currentTenant = SessionAPI.getCurrentTenant();
      setTenant(currentTenant);
    } else {
      setTenant(null);
    }
    
    setIsLoading(false);
  }, [user]);

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
