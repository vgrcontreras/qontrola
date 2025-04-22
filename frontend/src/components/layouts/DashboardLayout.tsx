
import { Button } from "@/components/ui/button";
import { useLocation } from "react-router-dom";
import { useTenant } from "@/contexts/TenantContext";
import { SidebarNav } from "./SidebarNav";
import { UserMenu } from "./UserMenu";
import { 
  Sidebar,
  SidebarContent,
  SidebarProvider,
  SidebarTrigger 
} from "@/components/ui/sidebar";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const { tenant } = useTenant();
  const location = useLocation();
  
  const pageTitles: Record<string, string> = {
    "/dashboard": "Dashboard",
    "/clientes": "Clientes",
    "/projetos": "Projetos",
    "/tarefas": "Tarefas",
    "/financas": "Finanças",
    "/relatorios": "Relatórios",
    "/configuracoes": "Configurações",
  };

  const currentPageTitle = pageTitles[location.pathname] || "Dashboard";

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="min-h-screen w-full bg-gradient-to-br from-primary-50 to-neutral-100">
        <div className="w-full bg-white min-h-screen lg:rounded-xl lg:shadow-lg lg:m-0 overflow-hidden">
          <div className="flex flex-col lg:flex-row w-full">
            <Sidebar>
              <SidebarContent>
                <div className="p-4 border-b border-caju-800 flex items-center justify-between">
                  <h1 className="font-bold text-xl text-white">Studio Caju</h1>
                  <SidebarTrigger className="text-white md:hidden hover:bg-caju-800" />
                </div>
                <SidebarNav />
                <UserMenu />
              </SidebarContent>
            </Sidebar>

            <div className="flex-1 min-w-0 w-full">
              <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
                <div className="flex items-center justify-between px-4 py-4">
                  <div className="flex items-center gap-4">
                    <SidebarTrigger className="md:inline-flex" />
                    <h1 className="text-xl font-semibold text-gray-800">{currentPageTitle}</h1>
                  </div>
                  {tenant && (
                    <div className="text-sm font-medium text-gray-500">
                      {tenant.name}
                    </div>
                  )}
                </div>
              </header>
              <main className="p-4 md:p-6 w-full">
                {children}
              </main>
            </div>
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
}

