import React, { useState } from "react";
import { runMatching, exportData, resetDatabase } from "../../services/api";
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

  const handleReset = async () => {
    if (!window.confirm("Reset the database? This will delete all mentors, mentees, and matches.")) return;
    try {
      setLoading("Reset");
      await resetDatabase();
      onRefresh();
    } catch (err) {
      console.error(err);
      alert("Reset failed");
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="control-panel flex flex-col gap-2">
      <ImportPanel onRefresh={onRefresh} />

      <div className="border-t border-gray-200 pt-4 mt-2 flex gap-2">
        <button
          onClick={() => handleAction(runMatching, "Run Matching")}
          disabled={loading !== null}
          className={`flex-1 py-2 rounded-lg text-sm font-semibold transition-colors ${
            loading !== null
              ? "bg-gray-200 text-gray-400 cursor-not-allowed"
              : "bg-emerald-600 text-white hover:bg-emerald-700"
          }`}
        >
          {loading === "Run Matching" ? "Running..." : "Run Matching"}
        </button>

        <button
          onClick={() => handleAction(exportData, "Export")}
          disabled={loading !== null}
          className={`flex-1 py-2 rounded-lg text-sm font-semibold border transition-colors ${
            loading !== null
              ? "border-gray-200 text-gray-400 cursor-not-allowed"
              : "border-gray-300 text-gray-700 hover:bg-gray-50"
          }`}
        >
          {loading === "Export" ? "Exporting..." : "Export CSV"}
        </button>

        <button
          onClick={handleReset}
          disabled={loading !== null}
          className={`flex-1 py-2 rounded-lg text-sm font-semibold border transition-colors ${
            loading !== null
              ? "border-gray-200 text-gray-400 cursor-not-allowed"
              : "border-red-300 text-red-600 hover:bg-red-50"
          }`}
        >
          {loading === "Reset" ? "Resetting..." : "Reset DB"}
        </button>
      </div>
    </div>
  );
};

export default ControlPanel;
