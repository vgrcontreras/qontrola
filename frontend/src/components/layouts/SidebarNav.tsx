import { 
  LayoutDashboard, 
  Users, 
  Briefcase, 
  CheckSquare, 
  DollarSign,
  BarChart,
  Settings
} from "lucide-react";

import { useSidebar } from "@/components/ui/sidebar";
import { useLocation, useNavigate } from "react-router-dom";

export function SidebarNav() {
  const { state } = useSidebar();
  const isCollapsed = state === "collapsed";
  const location = useLocation();
  const navigate = useNavigate();
  const currentPath = location.pathname;

  const navItems = [
    { path: "/dashboard", icon: LayoutDashboard, text: "Dashboard" },
    { path: "/clientes", icon: Users, text: "Clientes" },
    { path: "/projetos", icon: Briefcase, text: "Projetos" },
    { path: "/tarefas", icon: CheckSquare, text: "Tarefas" },
    { path: "/financas", icon: DollarSign, text: "Finanças" },
    { path: "/relatorios", icon: BarChart, text: "Relatórios" },
    { path: "/configuracoes", icon: Settings, text: "Configurações" }
  ];

  return (
    <nav className="flex-1 p-4 space-y-1">
      {navItems.map((item) => (
        <button 
          key={item.text}
          onClick={() => navigate(item.path)}
          className={`flex items-center p-3 rounded-lg w-full text-left ${
            item.path === currentPath 
              ? "bg-caju-800 text-white"
              : "text-caju-500 hover:bg-caju-100 hover:text-caju-800"
          } transition-colors`}
        >
          <item.icon className="h-5 w-5" />
          {!isCollapsed && <span className="ml-3">{item.text}</span>}
        </button>
      ))}
    </nav>
  );
}
