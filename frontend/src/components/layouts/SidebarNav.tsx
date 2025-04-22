
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
import { useLocation } from "react-router-dom";

export function SidebarNav() {
  const { state } = useSidebar();
  const isCollapsed = state === "collapsed";
  const location = useLocation();
  const currentPath = location.pathname;

  const navItems = [
    { href: "/dashboard", icon: LayoutDashboard, text: "Dashboard" },
    { href: "/clientes", icon: Users, text: "Clientes" },
    { href: "/projetos", icon: Briefcase, text: "Projetos" },
    { href: "/tarefas", icon: CheckSquare, text: "Tarefas" },
    { href: "/financas", icon: DollarSign, text: "Finanças" },
    { href: "/relatorios", icon: BarChart, text: "Relatórios" },
    { href: "/configuracoes", icon: Settings, text: "Configurações" }
  ];

  return (
    <nav className="flex-1 p-4 space-y-1">
      {navItems.map((item) => (
        <a 
          key={item.text}
          href={item.href} 
          className={`flex items-center p-3 rounded-lg ${
            item.href === currentPath 
              ? "bg-caju-800 text-white"
              : "hover:bg-caju-800"
          } transition-colors`}
        >
          <item.icon className="h-5 w-5" />
          {!isCollapsed && <span className="ml-3">{item.text}</span>}
        </a>
      ))}
    </nav>
  );
}
