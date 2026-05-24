import React, { useState } from "react";
import { runMatching, exportData } from "../../services/api";
import ImportPanel from "./ImportPanel";

interface Props {
  onRefresh: () => void;
}

const ControlPanel: React.FC<Props> = ({ onRefresh }) => {
  const [loading, setLoading] = useState<string | null>(null);

  const handleAction = async (action: () => Promise<void>, label: string) => {
    try {
      setLoading(label);
      await action();
      if (label !== "Export") {
        onRefresh();
      }
    } catch (err) {
      console.error(err);
      alert(`${label} failed`);
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="control-panel flex flex-col gap-2">
      <ImportPanel onRefresh={onRefresh} />

      <button
        onClick={() => handleAction(runMatching, "Run Matching")}
        disabled={loading !== null}
        className="bg-green-500 text-white px-4 py-2 rounded"
      >
        {loading === "Run Matching" ? "Running..." : "Run Matching"}
      </button>

      <button
        onClick={() => handleAction(exportData, "Export")}
        disabled={loading !== null}
        className="bg-gray-500 text-white px-4 py-2 rounded"
      >
        {loading === "Export" ? "Exporting..." : "Export"}
      </button>
    </div>
  );
};

export default ControlPanel;
