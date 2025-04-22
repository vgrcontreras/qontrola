
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { EllipsisVertical, Eye, Pencil, Trash2 } from "lucide-react";
import { ProjectStatus } from "@/lib/types";
import { useProjects } from "@/hooks/useProjects";
import { useClients } from "@/hooks/useClients";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/hooks/use-toast";

export function ProjectsTable() {
  const { projects, isLoading } = useProjects();
  const { clients } = useClients();
  const { toast } = useToast();

  const handleView = (projectId: string) => {
    toast({
      title: "Visualizar projeto",
      description: `Visualizando projeto com ID: ${projectId}`,
    });
  };

  const handleEdit = (projectId: string) => {
    toast({
      title: "Editar projeto",
      description: `Editando projeto com ID: ${projectId}`,
    });
  };

  const handleDelete = (projectId: string) => {
    toast({
      title: "Excluir projeto",
      description: `Excluindo projeto com ID: ${projectId}`,
      variant: "destructive",
    });
  };

  const getStatusColor = (status: ProjectStatus) => {
    switch (status) {
      case ProjectStatus.NAO_INICIADO:
        return "bg-gray-100 text-gray-800";
      case ProjectStatus.EM_ANDAMENTO:
        return "bg-blue-100 text-blue-800";
      case ProjectStatus.CONCLUIDO:
        return "bg-green-100 text-green-800";
      case ProjectStatus.CANCELADO:
        return "bg-red-100 text-red-800";
      case ProjectStatus.EM_PAUSA:
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getClientName = (clientId?: string) => {
    if (!clientId) return "Sem cliente";
    const client = clients.find(client => client.id === clientId);
    return client ? client.name : "Cliente não encontrado";
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg border p-8 flex items-center justify-center">
        <div className="text-muted-foreground">Carregando projetos...</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Nome</TableHead>
            <TableHead>Cliente</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Data Início</TableHead>
            <TableHead>Data Fim</TableHead>
            <TableHead className="text-right">Valor</TableHead>
            <TableHead className="w-[72px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {projects.map((project) => (
            <TableRow key={project.id}>
              <TableCell className="font-medium">{project.name}</TableCell>
              <TableCell>{getClientName(project.clientId)}</TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(project.status)}`}>
                  {project.status}
                </span>
              </TableCell>
              <TableCell>{project.startDate}</TableCell>
              <TableCell>{project.targetDate}</TableCell>
              <TableCell className="text-right">
                {new Intl.NumberFormat('pt-BR', { 
                  style: 'currency', 
                  currency: 'BRL' 
                }).format(project.value / 100)}
              </TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <EllipsisVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => handleView(project.id)}>
                      <Eye className="h-4 w-4 mr-2" /> Visualizar
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleEdit(project.id)}>
                      <Pencil className="h-4 w-4 mr-2" /> Editar
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleDelete(project.id)} className="text-red-600">
                      <Trash2 className="h-4 w-4 mr-2" /> Excluir
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
          {projects.length === 0 && (
            <TableRow>
              <TableCell colSpan={7} className="text-center py-4 text-gray-500">
                Nenhum projeto cadastrado
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
