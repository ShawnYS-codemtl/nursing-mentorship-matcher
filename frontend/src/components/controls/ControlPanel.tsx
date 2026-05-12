import React, { useState } from "react";
import { uploadCsvFiles, runMatching, exportData } from "../../services/api";
// import type { ImportSource } from "../../types";

interface Props {
  onRefresh: () => void;
}

const ControlPanel: React.FC<Props> = ({onRefresh}) => {
  const [loading, setLoading] = useState<string | null>(null);
  // const [source, setSource] = useState<ImportSource>("csv");
  const [mentorFile, setMentorFile] = useState<File | null>(null);
  const [menteeFile, setMenteeFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

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

  const handleCsvUpload = async () => {
    if (!mentorFile || !menteeFile) {
      alert("Please select both CSV files");
      return;
    }

    try {
      setUploading(true);

      const formData = new FormData();

      formData.append("mentor_file", mentorFile);
      formData.append("mentee_file", menteeFile);

      await uploadCsvFiles(formData);

      onRefresh();

      alert("CSV import successful");
    } catch (err) {
      console.error(err);
      alert("Failed to import CSVs");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="control-panel flex gap-2">
      <div className="flex flex-col gap-2">
        <div>
          <label className="block font-semibold mb-1">
            Mentor CSV
          </label>

          <input
            type="file"
            accept=".csv"
            onChange={(e) =>
              setMentorFile(e.target.files?.[0] || null)
            }
          />
        </div>

        <div>
          <label className="block font-semibold mb-1">
            Mentee CSV
          </label>

          <input
            type="file"
            accept=".csv"
            onChange={(e) =>
              setMenteeFile(e.target.files?.[0] || null)
            }
          />
        </div>
      </div>

      <button
        onClick={handleCsvUpload}
        disabled={!mentorFile || !menteeFile || uploading}
        className={`
          px-4 py-2 rounded font-semibold transition-all duration-200
          ${
            !mentorFile || !menteeFile || uploading
              ? "bg-gray-300 text-gray-500 cursor-not-allowed opacity-70"
              : "bg-blue-600 text-white hover:bg-blue-700 hover:shadow-md cursor-pointer"
          }
        `}
      >
        {uploading ? "Uploading..." : "Import CSVs"}
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