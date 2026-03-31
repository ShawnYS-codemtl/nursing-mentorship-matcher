import React from "react";

const ControlPanel: React.FC = () => {
  return (
    <div className="control-panel flex gap-2">
      <button className="bg-blue-500 text-white px-4 py-2 rounded">
        Import
      </button>
      <button className="bg-green-500 text-white px-4 py-2 rounded">
        Run Matching
      </button>
      <button className="bg-gray-500 text-white px-4 py-2 rounded">
        Export
      </button>
    </div>
  );
};

export default ControlPanel;