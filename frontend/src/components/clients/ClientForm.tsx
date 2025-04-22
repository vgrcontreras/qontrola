
import { Form } from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { DialogClose } from "@/components/ui/dialog";
import { useClientForm } from "@/hooks/useClientForm";
import { ClientBasicFields } from "./form/ClientBasicFields";
import { ClientContactFields } from "./form/ClientContactFields";
import { ClientAddressFields } from "./form/ClientAddressFields";

export function ClientForm() {
  const { form, isSubmitting, onSubmit } = useClientForm();

  return (
    <Form {...form}>
      <form onSubmit={onSubmit} className="space-y-4">
        <ClientBasicFields form={form} />
        <ClientContactFields form={form} />
        <ClientAddressFields form={form} />
        
        <div className="flex justify-end space-x-2 pt-4">
          <DialogClose asChild>
            <Button variant="outline" type="button">Cancelar</Button>
          </DialogClose>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Cadastrando..." : "Cadastrar cliente"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
