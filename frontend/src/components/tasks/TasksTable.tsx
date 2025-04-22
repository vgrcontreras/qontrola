
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
import { TaskStatus, TaskPriority } from "@/lib/types";
import { useTasks } from "@/hooks/useTasks";
import { useProjects } from "@/hooks/useProjects";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/hooks/use-toast";

export function TasksTable() {
  const { tasks, isLoading } = useTasks();
  const { projects } = useProjects();
  const { toast } = useToast();

  const handleView = (taskId: string) => {
    toast({
      title: "Visualizar tarefa",
      description: `Visualizando tarefa com ID: ${taskId}`,
    });
  };

  const handleEdit = (taskId: string) => {
    toast({
      title: "Editar tarefa",
      description: `Editando tarefa com ID: ${taskId}`,
    });
  };

  const handleDelete = (taskId: string) => {
    toast({
      title: "Excluir tarefa",
      description: `Excluindo tarefa com ID: ${taskId}`,
      variant: "destructive",
    });
  };

  const getPriorityColor = (priority: TaskPriority) => {
    switch (priority) {
      case TaskPriority.BAIXA:
        return "bg-blue-100 text-blue-800";
      case TaskPriority.MEDIA:
        return "bg-yellow-100 text-yellow-800";
      case TaskPriority.ALTA:
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getProjectName = (projectId?: string) => {
    if (!projectId) return "Sem projeto";
    if (projectId === "none") return "Sem projeto";
    const project = projects.find(project => project.id === projectId);
    return project ? project.name : "Projeto não encontrado";
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg border p-8 flex items-center justify-center">
        <div className="text-muted-foreground">Carregando tarefas...</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Título</TableHead>
            <TableHead>Projeto</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Prioridade</TableHead>
            <TableHead>Data Limite</TableHead>
            <TableHead>Responsável</TableHead>
            <TableHead className="w-[72px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tasks.map((task) => (
            <TableRow key={task.id}>
              <TableCell className="font-medium">{task.title}</TableCell>
              <TableCell>{getProjectName(task.projectId)}</TableCell>
              <TableCell>{task.status}</TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-xs ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
              </TableCell>
              <TableCell>{task.dueDate}</TableCell>
              <TableCell>{task.assigneeId}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <EllipsisVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => handleView(task.id)}>
                      <Eye className="h-4 w-4 mr-2" /> Visualizar
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleEdit(task.id)}>
                      <Pencil className="h-4 w-4 mr-2" /> Editar
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleDelete(task.id)} className="text-red-600">
                      <Trash2 className="h-4 w-4 mr-2" /> Excluir
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
          {tasks.length === 0 && (
            <TableRow>
              <TableCell colSpan={7} className="text-center py-4 text-gray-500">
                Nenhuma tarefa cadastrada
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
