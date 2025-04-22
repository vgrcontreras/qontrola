
import { DashboardLayout } from "@/components/layouts/DashboardLayout";
import { ReportsHeader } from "@/components/reports/ReportsHeader";

const Reports = () => {
  return (
    <DashboardLayout>
      <div className="flex-grow p-6 space-y-6">
        <ReportsHeader />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg border">
            <h3 className="text-lg font-medium mb-4">Receitas vs Despesas</h3>
            <div className="h-80 flex items-center justify-center text-gray-500">
              Gráfico de Receitas vs Despesas
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg border">
            <h3 className="text-lg font-medium mb-4">Projetos por Status</h3>
            <div className="h-80 flex items-center justify-center text-gray-500">
              Gráfico de Projetos por Status
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg border">
            <h3 className="text-lg font-medium mb-4">Tarefas por Responsável</h3>
            <div className="h-80 flex items-center justify-center text-gray-500">
              Gráfico de Tarefas por Responsável
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg border">
            <h3 className="text-lg font-medium mb-4">Faturamento Mensal</h3>
            <div className="h-80 flex items-center justify-center text-gray-500">
              Gráfico de Faturamento Mensal
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Reports;
