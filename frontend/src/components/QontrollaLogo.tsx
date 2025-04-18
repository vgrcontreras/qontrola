import React from 'react';

interface LogoProps {
  className?: string;
  darkMode?: boolean;
}

const QontrollaLogo: React.FC<LogoProps> = ({ className = '', darkMode = false }) => {
  const textColor = darkMode ? 'text-white' : 'text-neutral-darker';
  
  return (
    <div className={`flex items-center ${className}`}>
      <span className={`text-2xl font-bold ${textColor}`}>
        <span className="text-royal-blue">q</span>ontrolla<span className="text-royal-blue">.</span>
      </span>
    </div>
  );
};

export default QontrollaLogo; 