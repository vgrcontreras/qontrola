import React from 'react';
import { Routes, Route } from 'react-router-dom';
import SignUpPage from './pages/SignUpPage';

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<SignUpPage />} />
    </Routes>
  );
};

export default App; 