
import { Button } from "@/components/ui/button";
import { MoreVertical } from "lucide-react";

export function ClientsList() {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Clientes Recentes</h2>
        <Button variant="link" className="text-caju-500 hover:text-caju-600">
          Ver todos
        </Button>
      </div>
      <div className="space-y-4">
        <div className="flex items-center p-3 rounded-lg hover:bg-gray-50 transition-all">
          <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold mr-3">
            EC
          </div>
          <div className="flex-grow">
            <h3 className="font-medium">Empresa Comércio Ltda</h3>
            <p className="text-sm text-gray-500">CNPJ: 12.345.678/0001-90</p>
          </div>
          <Button variant="ghost" size="icon">
            <MoreVertical className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
