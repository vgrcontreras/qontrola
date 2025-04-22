
import { Button } from "@/components/ui/button";
import { useProjects } from "@/hooks/useProjects";
import { ProjectStatus } from "@/lib/types";
import { Link } from "react-router-dom";
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { ProjectForm } from "@/components/projects/ProjectForm";

export function ProjectsList() {
  const { projects, isLoading } = useProjects();
  const [isOpen, setIsOpen] = useState(false);
  
  // Filtra apenas projetos em andamento para o dashboard
  const ongoingProjects = projects.filter(
    project => project.status === ProjectStatus.EM_ANDAMENTO
  ).slice(0, 3); // Limita a 3 projetos para o dashboard
  
  // Define as cores com base no status
  const getStatusInfo = (status: ProjectStatus) => {
    switch (status) {
      case ProjectStatus.EM_ANDAMENTO:
        return { label: "Em progresso", color: "yellow" };
      case ProjectStatus.CONCLUIDO:
        return { label: "Finalizado", color: "green" };
      case ProjectStatus.CANCELADO:
        return { label: "Cancelado", color: "red" };
      case ProjectStatus.EM_PAUSA:
        return { label: "Em pausa", color: "yellow" };
      default:
        return { label: "Não iniciado", color: "gray" };
    }
  };

  if (isLoading) {
    return (
      <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Projetos em Andamento</h2>
        </div>
        <div className="flex items-center justify-center h-48">
          <p>Carregando projetos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Projetos em Andamento</h2>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            className="text-caju-500 hover:text-caju-600"
            onClick={() => setIsOpen(true)}
          >
            Novo
          </Button>
          <Button 
            variant="link" 
            className="text-caju-500 hover:text-caju-600"
            asChild
          >
            <Link to="/projetos">Ver todos</Link>
          </Button>
        </div>
      </div>
      
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>Novo Projeto</DialogTitle>
          </DialogHeader>
          <ProjectForm onSuccess={() => setIsOpen(false)} />
        </DialogContent>
      </Dialog>
      
      <div className="space-y-4">
        {ongoingProjects.length > 0 ? (
          ongoingProjects.map(project => {
            const statusInfo = getStatusInfo(project.status);
            // Calcular progresso com base em dados fictícios para demonstração
            // Em uma aplicação real, isso viria de dados reais de tarefas
            const progress = Math.floor(Math.random() * 100);
            
            return (
              <ProjectCard 
                key={project.id}
                title={project.name}
                status={statusInfo.label}
                statusColor={statusInfo.color as any}
                description={project.description || "Sem descrição"}
                team={["JS", "MR"]}
                teamColors={["blue", "green"]}
                tasksCount={Math.floor(Math.random() * 10) + 1}
                progress={progress}
                deadline={project.targetDate || "Sem prazo"}
                value={new Intl.NumberFormat('pt-BR', { 
                  minimumFractionDigits: 2 
                }).format(project.value / 100)}
              />
            );
          })
        ) : (
          <div className="text-center py-8 text-gray-500">
            Nenhum projeto em andamento no momento
          </div>
        )}
      </div>
    </div>
  );
}

interface ProjectCardProps {
  title: string;
  status: string;
  statusColor: "yellow" | "red" | "green" | "gray";
  description: string;
  team: string[];
  teamColors: string[];
  tasksCount: number;
  progress: number;
  deadline: string;
  value: string;
}

function ProjectCard({
  title,
  status,
  statusColor,
  description,
  team,
  teamColors,
  tasksCount,
  progress,
  deadline,
  value
}: ProjectCardProps) {
  const statusClasses = {
    yellow: "bg-yellow-100 text-yellow-800",
    red: "bg-red-100 text-red-800",
    green: "bg-green-100 text-green-800"
  };

  const progressBarColor = {
    yellow: "bg-yellow-500",
    red: "bg-red-500",
    green: "bg-green-500"
  };

  return (
    <div className="border border-gray-100 rounded-lg p-4 hover:shadow-md transition-all">
      <div className="flex justify-between mb-2">
        <h3 className="font-semibold">{title}</h3>
        <span className={`px-2 py-1 rounded-full text-xs ${statusClasses[statusColor]}`}>
          {status}
        </span>
      </div>
      <p className="text-sm text-gray-500 mb-3">{description}</p>
      <div className="flex justify-between items-center mb-2">
        <div className="flex -space-x-2">
          {team.map((member, index) => (
            <div 
              key={index}
              className={`h-8 w-8 rounded-full bg-${teamColors[index]}-500 flex items-center justify-center text-white text-xs border-2 border-white`}
            >
              {member}
            </div>
          ))}
        </div>
        <span className="text-sm text-gray-500">{tasksCount} tarefas</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className={`${progressBarColor[statusColor]} h-2 rounded-full`} 
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="flex justify-between mt-2 text-xs text-gray-500">
        <span>Prazo: {deadline}</span>
        <span>R$ {value}</span>
      </div>
    </div>
  );
}
