import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AuthAPI } from "@/lib/api";

const Signup = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { toast } = useToast();

  // Formulário para cadastro de tenant e admin
  const [formData, setFormData] = useState({
    // Tenant
    tenantName: "",
    tenantDomain: "",
    // Admin
    adminEmail: "",
    adminPassword: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setFormData({
      ...formData,
      [id]: value
    });

    // Se estiver digitando o nome do tenant, sugerir um domínio automaticamente
    if (id === "tenantName") {
      const suggestedDomain = value.toLowerCase().replace(/\s+/g, '-');
      setFormData(prev => ({
        ...prev,
        tenantDomain: suggestedDomain
      }));
    }
  };

  const validateForm = () => {
    if (!formData.tenantName || !formData.tenantDomain) {
      setError("Nome e domínio da organização são obrigatórios");
      return false;
    }

    if (!formData.adminEmail || !formData.adminPassword) {
      setError("Email e senha do administrador são obrigatórios");
      return false;
    }

    // Validações adicionais podem ser adicionadas aqui

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Preparar dados para API
      const registrationData = {
        name: formData.tenantName,
        domain: formData.tenantDomain,
        admin_user: {
          email: formData.adminEmail,
          password: formData.adminPassword
        }
      };

      // Registrar tenant e administrador
      await AuthAPI.registerTenant(registrationData);

      // Fazer login automaticamente - atualizando para a nova assinatura do método
      await AuthAPI.login(formData.adminEmail, formData.adminPassword);

      toast({
        title: "Cadastro realizado com sucesso!",
        description: "Sua organização foi criada e você já está logado."
      });

      // Redirecionar para dashboard
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Ocorreu um erro ao criar sua conta");
      console.error("Erro ao criar conta:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-caju-500">Studio Caju</h1>
          <p className="text-gray-600 mt-2">Gestão de Tarefas e Finanças</p>
        </div>
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Registrar Nova Organização</CardTitle>
            <CardDescription>Crie sua organização e conta de administrador</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-2">
                <Label htmlFor="tenantName">Nome da Organização</Label>
                <Input
                  id="tenantName"
                  type="text"
                  placeholder="Studio Caju"
                  value={formData.tenantName}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="tenantDomain">Domínio</Label>
                <Input
                  id="tenantDomain"
                  type="text"
                  placeholder="studio-caju"
                  value={formData.tenantDomain}
                  onChange={handleChange}
                  required
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Este será o identificador único da sua organização. 
                  Apenas letras minúsculas, números e hífens.
                </p>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="adminEmail">E-mail do Administrador</Label>
                <Input
                  id="adminEmail"
                  type="email"
                  placeholder="admin@exemplo.com"
                  value={formData.adminEmail}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="adminPassword">Senha</Label>
                <Input
                  id="adminPassword"
                  type="password"
                  placeholder="********"
                  value={formData.adminPassword}
                  onChange={handleChange}
                  required
                />
              </div>

              <Button
                type="submit"
                className="w-full mt-6 bg-caju-500 hover:bg-caju-600"
                disabled={isLoading}
              >
                {isLoading ? "Criando organização..." : "Criar Organização e Conta"}
              </Button>
            </form>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4 border-t pt-4">
            <div className="text-sm text-center text-gray-500">
              Já tem uma conta?{" "}
              <a href="/login" className="text-caju-600 hover:underline">
                Entrar
              </a>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default Signup;
