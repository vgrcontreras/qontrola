
import { Button } from "@/components/ui/button";
import { DollarSign } from "lucide-react";

export function FinancesHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Finanças</h1>
        <p className="text-sm text-gray-500">Gerencie suas finanças</p>
      </div>
      <Button>
        <DollarSign className="mr-2" />
        Nova Transação
      </Button>
    </div>
  );
}
