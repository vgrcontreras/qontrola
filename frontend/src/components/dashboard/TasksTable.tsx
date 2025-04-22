
import { Button } from "@/components/ui/button";
import { MoreVertical, CheckSquare } from "lucide-react";

export function TasksTable() {
  return (
    <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Tarefas Recentes</h2>
        <Button variant="link" className="text-caju-500 hover:text-caju-600">
          Ver todas
        </Button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="py-3 text-left">Tarefa</th>
              <th className="py-3 text-left">Projeto</th>
              <th className="py-3 text-left">Status</th>
              <th className="py-3 text-left">Prazo</th>
              <th className="py-3 text-left">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-gray-100 hover:bg-gray-50 transition-all">
              <td className="py-3">
                <div className="flex items-center">
                  <CheckSquare className="h-4 w-4 text-purple-500 mr-2" />
                  <span>Desenvolver página inicial</span>
                </div>
              </td>
              <td className="py-3">Website Empresa X</td>
              <td className="py-3">
                <span className="px-2 py-1 rounded-full bg-yellow-100 text-yellow-800 text-xs">
                  Em progresso
                </span>
              </td>
              <td className="py-3">15/07/2023</td>
              <td className="py-3">
                <Button variant="ghost" size="icon">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
