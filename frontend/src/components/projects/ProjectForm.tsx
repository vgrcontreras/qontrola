
import { useState } from "react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DialogClose } from "@/components/ui/dialog";
import { ProjectStatus } from "@/lib/types";
import { ProjectAPI } from "@/lib/storage";
import { useTenant } from "@/contexts/TenantContext";
import { useToast } from "@/hooks/use-toast";
import { useProjects } from "@/hooks/useProjects";
import { useClients } from "@/hooks/useClients";

const projectFormSchema = z.object({
  name: z.string().min(2, "Nome deve ter pelo menos 2 caracteres"),
  description: z.string().optional(),
  clientId: z.string().optional(),
  status: z.nativeEnum(ProjectStatus),
  startDate: z.string().optional(),
  targetDate: z.string().optional(),
  value: z.coerce.number().min(0, "Valor deve ser positivo")
});

type ProjectFormValues = z.infer<typeof projectFormSchema>;

interface ProjectFormProps {
  onSuccess?: () => void;
}

export function ProjectForm({ onSuccess }: ProjectFormProps = {}) {
  const { tenant } = useTenant();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { invalidateProjects } = useProjects();
  const { clients } = useClients();
  
  const form = useForm<ProjectFormValues>({
    resolver: zodResolver(projectFormSchema),
    defaultValues: {
      name: "",
      description: "",
      clientId: "",
      status: ProjectStatus.NAO_INICIADO,
      startDate: "",
      targetDate: "",
      value: 0,
    },
  });

  const onSubmit = async (values: ProjectFormValues) => {
    if (!tenant) return;
    
    setIsSubmitting(true);
    try {
      const valueInCents = Math.round(values.value * 100);
      
      const project = ProjectAPI.add({
        tenantId: tenant.id,
        name: values.name,
        description: values.description || "",
        clientId: values.clientId || undefined,
        status: values.status,
        startDate: values.startDate || undefined,
        targetDate: values.targetDate || undefined,
        value: valueInCents
      });
      
      toast({
        title: "Projeto criado com sucesso",
        description: `${project.name} foi adicionado à sua lista de projetos.`,
      });

      form.reset();
      invalidateProjects();
      
      // Chama o callback de sucesso, se fornecido
      if (onSuccess) {
        onSuccess();
      } else {
        // Fechar dialog após o salvamento apenas se não houver callback
        setTimeout(() => {
          const closeButton = document.querySelector('[data-radix-collection-item]') as HTMLElement;
          if (closeButton) closeButton.click();
        }, 100);
      }
    } catch (error) {
      console.error("Erro ao criar projeto:", error);
      toast({
        title: "Erro ao criar projeto",
        description: "Ocorreu um erro ao criar o projeto. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nome do Projeto</FormLabel>
              <FormControl>
                <Input placeholder="Digite o nome do projeto" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Descrição</FormLabel>
              <FormControl>
                <Textarea placeholder="Descreva o projeto" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="clientId"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Cliente</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um cliente" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="none">Sem cliente</SelectItem>
                  {clients.map((client) => (
                    <SelectItem key={client.id} value={client.id}>
                      {client.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="status"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Status</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o status" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value={ProjectStatus.NAO_INICIADO}>Não iniciado</SelectItem>
                  <SelectItem value={ProjectStatus.EM_ANDAMENTO}>Em andamento</SelectItem>
                  <SelectItem value={ProjectStatus.CONCLUIDO}>Concluído</SelectItem>
                  <SelectItem value={ProjectStatus.CANCELADO}>Cancelado</SelectItem>
                  <SelectItem value={ProjectStatus.EM_PAUSA}>Em pausa</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="startDate"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Data de Início</FormLabel>
                <FormControl>
                  <Input type="date" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="targetDate"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Data de Término</FormLabel>
                <FormControl>
                  <Input type="date" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="value"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Valor (R$)</FormLabel>
              <FormControl>
                <Input 
                  type="number" 
                  step="0.01" 
                  placeholder="0,00"
                  {...field} 
                  onChange={(e) => {
                    const value = e.target.value === '' ? '0' : e.target.value;
                    field.onChange(parseFloat(value));
                  }}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end space-x-2 pt-4">
          <DialogClose asChild>
            <Button variant="outline" type="button">Cancelar</Button>
          </DialogClose>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Salvando..." : "Salvar Projeto"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
