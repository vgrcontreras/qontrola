
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ProjectAPI } from "@/lib/storage";
import { useTenant } from "@/contexts/TenantContext";

export const PROJECTS_QUERY_KEY = "projects";

export function useProjects() {
  const { tenant } = useTenant();
  const queryClient = useQueryClient();

  const { data: projects = [], isLoading } = useQuery({
    queryKey: [PROJECTS_QUERY_KEY],
    queryFn: () => tenant ? ProjectAPI.getAll(tenant.id) : [],
    enabled: !!tenant,
  });

  const invalidateProjects = () => {
    queryClient.invalidateQueries({ queryKey: [PROJECTS_QUERY_KEY] });
  };

  return {
    projects,
    isLoading,
    invalidateProjects,
  };
}
