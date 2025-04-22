
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ClientAPI } from "@/lib/storage";
import { useTenant } from "@/contexts/TenantContext";

export const CLIENTS_QUERY_KEY = "clients";

export function useClients() {
  const { tenant } = useTenant();
  const queryClient = useQueryClient();

  const { data: clients = [], isLoading } = useQuery({
    queryKey: [CLIENTS_QUERY_KEY],
    queryFn: () => tenant ? ClientAPI.getAll(tenant.id) : [],
    enabled: !!tenant,
  });

  const invalidateClients = () => {
    queryClient.invalidateQueries({ queryKey: [CLIENTS_QUERY_KEY] });
  };

  return {
    clients,
    isLoading,
    invalidateClients,
  };
}
