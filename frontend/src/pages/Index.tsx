import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Index = () => {
  const navigate = useNavigate();
  
  useEffect(() => {
    // Redirecionar para a página de login
    navigate('/login');
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-caju-500 mb-4">Studio Caju</h1>
        <p className="text-xl text-gray-600">Carregando...</p>
      </div>
    </div>
  );
};

export default Index;
