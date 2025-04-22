
import { Button } from "@/components/ui/button";
import { BarChart } from "lucide-react";

export function ReportsHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Relatórios</h1>
        <p className="text-sm text-gray-500">Visualize seus relatórios</p>
      </div>
      <Button>
        <BarChart className="mr-2" />
        Exportar
      </Button>
    </div>
  );
}
