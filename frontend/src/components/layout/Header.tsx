import React from "react";
import { getSessionCode, clearSessionCode } from "../../services/api";

const Header: React.FC = () => {
  const sessionCode = getSessionCode();

  function handleSwitch() {
    clearSessionCode();
    window.location.reload();
  }

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm px-6 py-4 flex items-center justify-between">
      <div className="border-l-4 border-blue-600 pl-4">
        <h1 className="text-xl font-bold text-gray-900 leading-tight">Mentorship Dashboard</h1>
        <p className="text-xs text-gray-500 mt-0.5">McGill Nursing — Mentorship Matching</p>
      </div>

      {sessionCode && (
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-blue-50 border border-blue-200 rounded-lg px-3 py-1.5">
            <span className="text-xs text-blue-500 font-medium">Workspace</span>
            <span className="text-sm font-mono font-semibold text-blue-800">{sessionCode}</span>
          </div>
          <button
            onClick={handleSwitch}
            className="text-xs text-gray-500 hover:text-gray-700 border border-gray-300 rounded-md px-2.5 py-1.5 hover:bg-gray-50 transition-colors"
          >
            Switch
          </button>
        </div>
      )}
    </header>
  );
};

export default Header;
