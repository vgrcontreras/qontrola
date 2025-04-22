
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
import { TransactionType } from "@/lib/types";
import { useFinances } from "@/hooks/useFinances";
import { useProjects } from "@/hooks/useProjects";
import { CategoryAPI } from "@/lib/storage";
import { useTenant } from "@/contexts/TenantContext";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/hooks/use-toast";

export function FinancesTable() {
  const { transactions, isLoading } = useFinances();
  const { projects } = useProjects();
  const { tenant } = useTenant();
  const categories = tenant ? CategoryAPI.getAll(tenant.id) : [];
  const { toast } = useToast();

  const handleView = (transactionId: string) => {
    toast({
      title: "Visualizar transação",
      description: `Visualizando transação com ID: ${transactionId}`,
    });
  };

  const handleEdit = (transactionId: string) => {
    toast({
      title: "Editar transação",
      description: `Editando transação com ID: ${transactionId}`,
    });
  };

  const handleDelete = (transactionId: string) => {
    toast({
      title: "Excluir transação",
      description: `Excluindo transação com ID: ${transactionId}`,
      variant: "destructive",
    });
  };

  const getProjectName = (projectId?: string) => {
    if (!projectId) return "Geral";
    if (projectId === "none") return "Geral";
    const project = projects.find(project => project.id === projectId);
    return project ? project.name : "Projeto não encontrado";
  };

  const getCategoryName = (categoryId?: string) => {
    if (!categoryId) return "Sem categoria";
    if (categoryId === "none") return "Sem categoria";
    const category = categories.find(category => category.id === categoryId);
    return category ? category.name : "Categoria não encontrada";
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg border p-8 flex items-center justify-center">
        <div className="text-muted-foreground">Carregando transações...</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Descrição</TableHead>
            <TableHead>Tipo</TableHead>
            <TableHead>Categoria</TableHead>
            <TableHead>Projeto</TableHead>
            <TableHead>Data</TableHead>
            <TableHead className="text-right">Valor</TableHead>
            <TableHead className="w-[72px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {transactions.map((transaction) => (
            <TableRow key={transaction.id}>
              <TableCell className="font-medium">{transaction.description}</TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  transaction.type === TransactionType.RECEITA 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {transaction.type}
                </span>
              </TableCell>
              <TableCell>{getCategoryName(transaction.categoryId)}</TableCell>
              <TableCell>{getProjectName(transaction.projectId)}</TableCell>
              <TableCell>{transaction.date}</TableCell>
              <TableCell className="text-right">
                {new Intl.NumberFormat('pt-BR', { 
                  style: 'currency', 
                  currency: 'BRL' 
                }).format(transaction.amount / 100)}
              </TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <EllipsisVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => handleView(transaction.id)}>
                      <Eye className="h-4 w-4 mr-2" /> Visualizar
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleEdit(transaction.id)}>
                      <Pencil className="h-4 w-4 mr-2" /> Editar
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleDelete(transaction.id)} className="text-red-600">
                      <Trash2 className="h-4 w-4 mr-2" /> Excluir
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
          {transactions.length === 0 && (
            <TableRow>
              <TableCell colSpan={7} className="text-center py-4 text-gray-500">
                Nenhuma transação cadastrada
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
