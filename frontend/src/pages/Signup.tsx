
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";

const Signup = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login, error } = useAuth(); // Assuming you register automatically on tenant "1"
  const navigate = useNavigate();

  // Simples: tenta registrar no tenant "1" (demonstração)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Mock: utiliza register da AuthService se disponível, senão apenas login direto (ajuste conforme sua regra)
    if (typeof (window as any).AuthService !== "undefined" && typeof (window as any).AuthService.register === "function") {
      const { register } = (window as any).AuthService;
      const result = register("1", { name, email, password });
      if (result.success && result.user) {
        await login(email, password);
        navigate("/dashboard");
      }
    } else {
      // fallback: apenas faz login com o cadastro novo
      await login(email, password);
      navigate("/dashboard");
    }

    setIsLoading(false);
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
            <CardTitle className="text-xl">Criar uma conta</CardTitle>
            <CardDescription>Preencha os campos abaixo para se cadastrar</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              <div className="space-y-2">
                <Label htmlFor="name">Nome</Label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Seu nome"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">E-mail</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Senha</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="********"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button
                type="submit"
                className="w-full mt-6 bg-caju-500 hover:bg-caju-600"
                disabled={isLoading}
              >
                {isLoading ? "Criando conta..." : "Criar conta"}
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
