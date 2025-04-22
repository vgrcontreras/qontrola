
import { DashboardLayout } from "@/components/layouts/DashboardLayout";
import { FinancesHeader } from "@/components/finances/FinancesHeader";
import { FinancesTable } from "@/components/finances/FinancesTable";
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DollarSign } from "lucide-react";
import { useTenant } from "@/contexts/TenantContext";
import { TransactionAPI, CategoryAPI } from "@/lib/storage";
import { TransactionType } from "@/lib/types";
import { useToast } from "@/hooks/use-toast";
import { useProjects } from "@/hooks/useProjects";
import { useFinances } from "@/hooks/useFinances";

const Finances = () => {
  const [open, setOpen] = useState(false);
  const { tenant } = useTenant();
  const { toast } = useToast();
  const { projects } = useProjects();
  const { invalidateFinances } = useFinances();

  const categories = tenant ? CategoryAPI.getAll(tenant.id) : [];

  const [formData, setFormData] = useState({
    description: "",
    amount: "",
    type: TransactionType.RECEITA,
    categoryId: "",
    projectId: "",
    date: new Date().toISOString().split('T')[0]
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
      const amountInCents = Math.round(parseFloat(formData.amount) * 100);
      
      TransactionAPI.add({
        tenantId: tenant.id,
        description: formData.description,
        amount: amountInCents,
        type: formData.type as TransactionType,
        categoryId: formData.categoryId || undefined,
        projectId: formData.projectId || undefined,
        date: formData.date
      });

      toast({
        title: "Transação registrada",
        description: "A transação foi registrada com sucesso!"
      });
      
      // Resetar formulário
      setFormData({
        description: "",
        amount: "",
        type: TransactionType.RECEITA,
        categoryId: "",
        projectId: "",
        date: new Date().toISOString().split('T')[0]
      });
      
      // Atualizar a tabela
      invalidateFinances();
      
      // Fechar o modal
      setOpen(false);
    } catch (error) {
      console.error("Erro ao registrar transação:", error);
      toast({
        title: "Erro",
        description: "Ocorreu um erro ao registrar a transação.",
        variant: "destructive"
      });
    }
  };

  return (
    <DashboardLayout>
      <div className="flex-grow p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Finanças</h1>
            <p className="text-sm text-gray-500">Gerencie suas finanças</p>
          </div>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button>
                <DollarSign className="mr-2" />
                Nova Transação
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Nova Transação</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4 pt-4">
                <div className="space-y-2">
                  <Label htmlFor="description">Descrição</Label>
                  <Input 
                    id="description" 
                    placeholder="Descrição da transação"
                    value={formData.description}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="amount">Valor</Label>
                  <Input 
                    id="amount" 
                    type="number" 
                    step="0.01" 
                    placeholder="0,00"
                    value={formData.amount}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="type">Tipo</Label>
                  <Select 
                    value={formData.type}
                    onValueChange={(value) => handleSelectChange("type", value)}
                  >
                    <SelectTrigger id="type">
                      <SelectValue placeholder="Selecione um tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value={TransactionType.RECEITA}>Receita</SelectItem>
                      <SelectItem value={TransactionType.DESPESA}>Despesa</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="categoryId">Categoria</Label>
                  <Select 
                    value={formData.categoryId}
                    onValueChange={(value) => handleSelectChange("categoryId", value)}
                  >
                    <SelectTrigger id="categoryId">
                      <SelectValue placeholder="Selecione uma categoria" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">Sem categoria</SelectItem>
                      {categories.map((category) => (
                        <SelectItem key={category.id} value={category.id}>
                          {category.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
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
                      <SelectItem value="none">Geral</SelectItem>
                      {projects.map((project) => (
                        <SelectItem key={project.id} value={project.id}>
                          {project.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="date">Data</Label>
                  <Input 
                    id="date" 
                    type="date"
                    value={formData.date}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="pt-4 flex justify-end space-x-2">
                  <Button type="button" variant="outline" onClick={() => setOpen(false)}>
                    Cancelar
                  </Button>
                  <Button type="submit">Criar Transação</Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
        <FinancesTable />
      </div>
    </DashboardLayout>
  );
};

export default Finances;
