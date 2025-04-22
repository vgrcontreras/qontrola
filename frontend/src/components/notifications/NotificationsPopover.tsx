
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Bell } from "lucide-react";

const notifications = [
  {
    id: 1,
    title: "Nova tarefa atribuída",
    description: "Você foi designado para revisar o layout do projeto XYZ",
    time: "há 5 minutos"
  },
  {
    id: 2,
    title: "Prazo próximo",
    description: "O projeto ABC precisa ser entregue em 2 dias",
    time: "há 1 hora"
  },
  {
    id: 3,
    title: "Comentário novo",
    description: "Maria comentou na tarefa de desenvolvimento",
    time: "há 2 horas"
  }
];

export function NotificationsPopover() {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" size="icon" className="relative">
          <Bell className="h-4 w-4" />
          <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
            {notifications.length}
          </span>
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0">
        <div className="p-4 border-b">
          <h4 className="font-semibold">Notificações</h4>
        </div>
        <div className="divide-y max-h-[300px] overflow-auto">
          {notifications.map((notification) => (
            <div key={notification.id} className="p-4 hover:bg-gray-50">
              <h5 className="font-medium text-sm">{notification.title}</h5>
              <p className="text-sm text-gray-500 mt-1">{notification.description}</p>
              <span className="text-xs text-gray-400 mt-2 block">{notification.time}</span>
            </div>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  );
}
