import React, { useState } from "react";
import { importData, runMatching, exportData } from "../../services/api";
import type { ImportSource } from "../../types";

interface Props {
  onRefresh: () => void;
}

const ControlPanel: React.FC<Props> = ({onRefresh}) => {
  const [loading, setLoading] = useState<string | null>(null);
  const [source, setSource] = useState<ImportSource>("csv");

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
    <div className="control-panel flex gap-2">
      <select
        value={source}
        onChange={(e) => setSource(e.target.value as ImportSource)}
        className="border px-2 py-1"
      >
        <option value="csv">CSV</option>
        <option value="google_sheets">Google Sheets</option>
      </select>
      <button
        onClick={() => handleAction(
          () => importData({source}), "Import")}
        disabled={loading !== null}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {loading === "Import" ? "Importing..." : "Import"}
      </button>

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