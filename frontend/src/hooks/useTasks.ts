
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { TaskAPI } from "@/lib/storage";
import { useTenant } from "@/contexts/TenantContext";

export const TASKS_QUERY_KEY = "tasks";

export function useTasks() {
  const { tenant } = useTenant();
  const queryClient = useQueryClient();

  const { data: tasks = [], isLoading } = useQuery({
    queryKey: [TASKS_QUERY_KEY],
    queryFn: () => tenant ? TaskAPI.getAll(tenant.id) : [],
    enabled: !!tenant,
  });

  const invalidateTasks = () => {
    queryClient.invalidateQueries({ queryKey: [TASKS_QUERY_KEY] });
  };

  return {
    tasks,
    isLoading,
    invalidateTasks,
  };
}
