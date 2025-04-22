
import { DashboardLayout } from "@/components/layouts/DashboardLayout";
import { ClientsHeader } from "@/components/clients/ClientsHeader";
import { ClientsTable } from "@/components/clients/ClientsTable";

const Clients = () => {
  return (
    <DashboardLayout>
      <div className="flex-grow space-y-6">
        <ClientsHeader />
        <ClientsTable />
      </div>
    </DashboardLayout>
  );
};

export default Clients;
