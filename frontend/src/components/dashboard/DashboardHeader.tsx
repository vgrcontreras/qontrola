
import { NotificationsPopover } from "@/components/notifications/NotificationsPopover";

export function DashboardHeader() {
  return (
    <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-500">Bem-vindo, gerencie seus projetos e finanças</p>
      </div>
      <div className="flex gap-2">
        <NotificationsPopover />
      </div>
    </header>
  );
}
