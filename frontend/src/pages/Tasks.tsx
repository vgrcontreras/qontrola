
import { DashboardLayout } from "@/components/layouts/DashboardLayout";
import { TasksTable } from "@/components/tasks/TasksTable";
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { CheckSquare } from "lucide-react";
import { useTenant } from "@/contexts/TenantContext";
import { TaskAPI } from "@/lib/storage";
import { TaskStatus, TaskPriority } from "@/lib/types";
import { useToast } from "@/hooks/use-toast";
import { useProjects } from "@/hooks/useProjects";
import { useTasks } from "@/hooks/useTasks";

const Tasks = () => {
  const [open, setOpen] = useState(false);
  const { tenant } = useTenant();
  const { toast } = useToast();
  const { projects } = useProjects();
  const { invalidateTasks } = useTasks();
  
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    projectId: "",
    status: TaskStatus.A_FAZER,
    priority: TaskPriority.MEDIA,
    dueDate: ""
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleSelectChange = (id: string, value: string) => {
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!tenant) return;
    
    try {
      TaskAPI.add({
        tenantId: tenant.id,
        title: formData.title,
        description: formData.description,
        projectId: formData.projectId || undefined,
        status: formData.status as TaskStatus,
        priority: formData.priority as TaskPriority,
        dueDate: formData.dueDate || undefined,
        assigneeId: undefined
      });

      toast({
        title: "Tarefa criada",
        description: "A tarefa foi criada com sucesso!"
      });
      
      // Resetar formulário
      setFormData({
        title: "",
        description: "",
        projectId: "",
        status: TaskStatus.A_FAZER,
        priority: TaskPriority.MEDIA,
        dueDate: ""
      });
      
      // Atualizar a tabela
      invalidateTasks();
      
      // Fechar o modal
      setOpen(false);
    } catch (error) {
      console.error("Erro ao criar tarefa:", error);
      toast({
        title: "Erro",
        description: "Ocorreu um erro ao criar a tarefa.",
        variant: "destructive"
      });
    }
  };

  return (
    <DashboardLayout>
      <div className="flex-grow p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Tarefas</h1>
            <p className="text-sm text-gray-500">Gerencie suas tarefas</p>
          </div>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button>
                <CheckSquare className="mr-2" />
                Nova Tarefa
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Nova Tarefa</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4 pt-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Título</Label>
                  <Input 
                    id="title" 
                    placeholder="Título da tarefa"
                    value={formData.title}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Descrição</Label>
                  <Textarea 
                    id="description" 
                    placeholder="Descrição da tarefa"
                    value={formData.description}
                    onChange={handleChange}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="projectId">Projeto</Label>
                  <Select 
                    value={formData.projectId} 
                    onValueChange={(value) => handleSelectChange("projectId", value)}
                  >
                    <SelectTrigger id="projectId">
                      <SelectValue placeholder="Selecione um projeto" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">Sem projeto</SelectItem>
                      {projects.map((project) => (
                        <SelectItem key={project.id} value={project.id}>
                          {project.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="status">Status</Label>
                  <Select 
                    value={formData.status} 
                    onValueChange={(value) => handleSelectChange("status", value)}
                  >
                    <SelectTrigger id="status">
                      <SelectValue placeholder="Selecione um status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value={TaskStatus.A_FAZER}>Pendente</SelectItem>
                      <SelectItem value={TaskStatus.EM_ANDAMENTO}>Em andamento</SelectItem>
                      <SelectItem value={TaskStatus.CONCLUIDO}>Concluída</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="priority">Prioridade</Label>
                  <Select 
                    value={formData.priority} 
                    onValueChange={(value) => handleSelectChange("priority", value)}
                  >
                    <SelectTrigger id="priority">
                      <SelectValue placeholder="Selecione uma prioridade" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value={TaskPriority.BAIXA}>Baixa</SelectItem>
                      <SelectItem value={TaskPriority.MEDIA}>Média</SelectItem>
                      <SelectItem value={TaskPriority.ALTA}>Alta</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="dueDate">Data limite</Label>
                  <Input 
                    id="dueDate" 
                    type="date"
                    value={formData.dueDate}
                    onChange={handleChange}
                  />
                </div>
                <div className="pt-4 flex justify-end space-x-2">
                  <Button type="button" variant="outline" onClick={() => setOpen(false)}>
                    Cancelar
                  </Button>
                  <Button type="submit">Criar Tarefa</Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
        <TasksTable />
      </div>
    </DashboardLayout>
  );
};

export default Tasks;
