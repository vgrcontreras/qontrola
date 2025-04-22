
import { DashboardLayout } from "@/components/layouts/DashboardLayout";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { StatsCards } from "@/components/dashboard/StatsCards";
import { TasksTable } from "@/components/dashboard/TasksTable";
import { ClientsList } from "@/components/dashboard/ClientsList";
import { ProjectsList } from "@/components/dashboard/ProjectsList";
import { FinancialOverview } from "@/components/dashboard/FinancialOverview";

const Dashboard = () => {
  return (
    <DashboardLayout>
      <div className="flex-grow p-6">
        <DashboardHeader />
        <StatsCards />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <TasksTable />
          <ClientsList />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ProjectsList />
          <FinancialOverview />
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;
