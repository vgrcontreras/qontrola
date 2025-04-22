
import { DashboardLayout } from "@/components/layouts/DashboardLayout";
import { ProjectsHeader } from "@/components/projects/ProjectsHeader";
import { ProjectsTable } from "@/components/projects/ProjectsTable";
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Briefcase } from "lucide-react";
import { ProjectForm } from "@/components/projects/ProjectForm";

const Projects = () => {
  const [open, setOpen] = useState(false);

  return (
    <DashboardLayout>
      <div className="flex-grow p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Projetos</h1>
            <p className="text-sm text-gray-500">Gerencie seus projetos</p>
          </div>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button>
                <Briefcase className="mr-2" />
                Novo Projeto
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle>Novo Projeto</DialogTitle>
              </DialogHeader>
              <ProjectForm />
            </DialogContent>
          </Dialog>
        </div>
        <ProjectsTable />
      </div>
    </DashboardLayout>
  );
};

export default Projects;
