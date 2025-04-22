
import { AlertCircle, Briefcase, CheckSquare, DollarSign, ChevronUp, ChevronDown } from "lucide-react";

export function StatsCards() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard 
        title="Projetos"
        subtitle="Total de projetos ativos"
        value="12"
        change="+8%"
        increasing={true}
        icon={<Briefcase className="h-6 w-6 text-blue-600" />}
        iconBg="bg-blue-100"
      />
      <StatCard 
        title="Tarefas"
        subtitle="Tarefas pendentes"
        value="28"
        change="-3%"
        increasing={false}
        icon={<CheckSquare className="h-6 w-6 text-purple-600" />}
        iconBg="bg-purple-100"
      />
      <StatCard 
        title="Receitas"
        subtitle="Este mês"
        value="R$ 12.580"
        change="+12%"
        increasing={true}
        icon={<DollarSign className="h-6 w-6 text-green-600" />}
        iconBg="bg-green-100"
      />
      <StatCard 
        title="Despesas"
        subtitle="Este mês"
        value="R$ 4.250"
        change="+5%"
        increasing={true}
        icon={<AlertCircle className="h-6 w-6 text-red-600" />}
        iconBg="bg-red-100"
      />
    </div>
  );
}

interface StatCardProps {
  title: string;
  subtitle: string;
  value: string;
  change: string;
  increasing: boolean;
  icon: React.ReactNode;
  iconBg: string;
}

function StatCard({ title, subtitle, value, change, increasing, icon, iconBg }: StatCardProps) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-all">
      <div className="flex items-center mb-4">
        <div className={`h-12 w-12 rounded-full ${iconBg} flex items-center justify-center mr-4`}>
          {icon}
        </div>
        <div>
          <h3 className="text-xl font-semibold">{title}</h3>
          <p className="text-gray-500 text-sm">{subtitle}</p>
        </div>
      </div>
      <div className="flex items-end justify-between">
        <span className="text-3xl font-bold">{value}</span>
        <span className={`${increasing ? 'text-green-500' : 'text-red-500'} flex items-center`}>
          {increasing ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          {change}
        </span>
      </div>
    </div>
  );
}
