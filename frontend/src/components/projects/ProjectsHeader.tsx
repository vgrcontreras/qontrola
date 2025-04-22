
import { Button } from "@/components/ui/button";
import { Briefcase } from "lucide-react";

export function ProjectsHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Projetos</h1>
        <p className="text-sm text-gray-500">Gerencie seus projetos</p>
      </div>
      <Button>
        <Briefcase className="mr-2" />
        Novo Projeto
      </Button>
    </div>
  );
}
