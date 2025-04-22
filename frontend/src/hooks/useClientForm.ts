
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { ClientType } from "@/lib/types";
import { ClientAPI } from "@/lib/storage";
import { useTenant } from "@/contexts/TenantContext";
import { useToast } from "@/hooks/use-toast";
import { useClients } from "@/hooks/useClients";

const formSchema = z.object({
  name: z.string().min(2, "Nome deve ter pelo menos 2 caracteres"),
  type: z.enum([ClientType.PF, ClientType.PJ]),
  document: z.string().min(11, "Documento deve ter pelo menos 11 caracteres"),
  email: z.string().email("Email inválido"),
  phone: z.string().min(10, "Telefone deve ter pelo menos 10 caracteres"),
  address: z.string().optional(),
  city: z.string().optional(),
  state: z.string().optional(),
});

export type ClientFormValues = z.infer<typeof formSchema>;

export function useClientForm() {
  const { tenant } = useTenant();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { invalidateClients } = useClients();
  
  const form = useForm<ClientFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      type: ClientType.PF,
      document: "",
      email: "",
      phone: "",
      address: "",
      city: "",
      state: "",
    },
  });

  const onSubmit = async (values: ClientFormValues) => {
    if (!tenant) return;
    
    setIsSubmitting(true);
    try {
      const client = ClientAPI.add({
        tenantId: tenant.id,
        name: values.name,
        type: values.type,
        document: values.document,
        email: values.email,
        phone: values.phone,
        address: values.address || "",
        city: values.city || "",
        state: values.state || "",
      });
      
      toast({
        title: "Cliente cadastrado",
        description: `${client.name} foi cadastrado com sucesso.`,
      });

      form.reset();
      invalidateClients();
      
      setTimeout(() => {
        const closeButton = document.querySelector('[data-radix-collection-item]') as HTMLElement;
        if (closeButton) closeButton.click();
      }, 100);
      
    } catch (error) {
      console.error("Erro ao cadastrar cliente:", error);
      toast({
        title: "Erro",
        description: "Ocorreu um erro ao cadastrar o cliente.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    form,
    isSubmitting,
    onSubmit: form.handleSubmit(onSubmit),
  };
}
