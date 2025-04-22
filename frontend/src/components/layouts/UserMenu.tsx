import { ChevronDown } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useSidebar } from "@/components/ui/sidebar";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function UserMenu() {
  const { user, logout } = useAuth();
  const { state } = useSidebar();
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const isCollapsed = state === "collapsed";
  const navigate = useNavigate();

  const toggleUserMenu = () => setUserMenuOpen(!userMenuOpen);

  return (
    <div className="p-4 border-t border-caju-800">
      <div className="relative">
        <button 
          onClick={toggleUserMenu}
          className="w-full flex items-center p-3 rounded-lg hover:bg-caju-800 transition-colors group text-white"
        >
          <div className="h-8 w-8 rounded-full bg-caju-300 flex items-center justify-center text-caju-900 font-bold">
            {user?.name?.charAt(0)}
          </div>
          {!isCollapsed && (
            <>
              <div className="ml-3 flex-1 text-left">
                <p className="font-medium truncate">{user?.name}</p>
                <p className="text-xs text-caju-300">Admin</p>
              </div>
              <ChevronDown className={`h-5 w-5 transition-transform ${userMenuOpen ? 'rotate-180' : ''}`} />
            </>
          )}
        </button>

        {userMenuOpen && !isCollapsed && (
          <div className="absolute bottom-full left-0 right-0 mb-2 bg-caju-800 rounded-lg py-2">
            <button 
              onClick={() => navigate("/perfil")}
              className="block w-full text-left px-4 py-2 text-sm hover:bg-caju-700 transition-colors text-white"
            >
              Meu Perfil
            </button>
            <button 
              onClick={() => navigate("/configuracoes")}
              className="block w-full text-left px-4 py-2 text-sm hover:bg-caju-700 transition-colors text-white"
            >
              Configurações
            </button>
            <button 
              onClick={() => logout()} 
              className="w-full text-left px-4 py-2 text-sm hover:bg-caju-700 transition-colors text-red-300"
            >
              Sair
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
