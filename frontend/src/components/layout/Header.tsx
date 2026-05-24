import React from "react";

const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm px-6 py-4 flex items-center">
      <div className="border-l-4 border-blue-600 pl-4">
        <h1 className="text-xl font-bold text-gray-900 leading-tight">Mentorship Dashboard</h1>
        <p className="text-xs text-gray-500 mt-0.5">McGill Nursing — Mentorship Matching</p>
      </div>
    </header>
  );
};

export default Header;
