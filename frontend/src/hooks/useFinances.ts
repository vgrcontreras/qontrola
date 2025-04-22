
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { TransactionAPI } from "@/lib/storage";
import { useTenant } from "@/contexts/TenantContext";

export const FINANCES_QUERY_KEY = "finances";

export function useFinances() {
  const { tenant } = useTenant();
  const queryClient = useQueryClient();

  const { data: transactions = [], isLoading } = useQuery({
    queryKey: [FINANCES_QUERY_KEY],
    queryFn: () => tenant ? TransactionAPI.getAll(tenant.id) : [],
    enabled: !!tenant,
  });

  const invalidateFinances = () => {
    queryClient.invalidateQueries({ queryKey: [FINANCES_QUERY_KEY] });
  };

  return {
    transactions,
    isLoading,
    invalidateFinances,
  };
}
