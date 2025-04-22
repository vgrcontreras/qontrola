
import { Card } from "@/components/ui/card";
import { ChevronUp } from "lucide-react";

export function FinancialOverview() {
  return (
    <Card className="bg-white p-6 rounded-xl shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Visão Financeira</h2>
        <select className="border border-gray-300 rounded p-1 text-sm">
          <option>Este mês</option>
          <option>Mês anterior</option>
          <option>Últimos 3 meses</option>
        </select>
      </div>
      
      <div className="bg-green-50 p-4 rounded-lg mb-4">
        <h3 className="text-lg font-semibold text-green-800">Receitas</h3>
        <p className="text-2xl font-bold text-green-600">R$ 12.580,00</p>
        <div className="flex items-center text-sm text-green-600">
          <ChevronUp className="h-4 w-4 mr-1" />
          12% em relação ao mês anterior
        </div>
      </div>
      
      <div className="bg-red-50 p-4 rounded-lg mb-4">
        <h3 className="text-lg font-semibold text-red-800">Despesas</h3>
        <p className="text-2xl font-bold text-red-600">R$ 4.250,00</p>
        <div className="flex items-center text-sm text-red-600">
          <ChevronUp className="h-4 w-4 mr-1" />
          5% em relação ao mês anterior
        </div>
      </div>
      
      <div className="bg-primary-50 p-4 rounded-lg mb-4">
        <h3 className="text-lg font-semibold text-primary-800">Lucro</h3>
        <p className="text-2xl font-bold text-primary-600">R$ 8.330,00</p>
        <div className="flex items-center text-sm text-primary-600">
          <ChevronUp className="h-4 w-4 mr-1" />
          16% em relação ao mês anterior
        </div>
      </div>
      
      <a href="#" className="block text-center w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 transition-all mt-4">
        Ver relatório completo
      </a>
    </Card>
  );
}
