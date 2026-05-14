import React, { useState } from "react";
import { uploadCsvFiles, runMatching, exportData, confirmImport } from "../../services/api";
import type { ImportPreviewResponse } from "../../types";
import ImportMappingTable from "./ImportMappingTable";
import { MENTEE_FIELDS, MENTOR_FIELDS } from "../../constants/importFields";

interface Props {
  onRefresh: () => void;
}

const ControlPanel: React.FC<Props> = ({onRefresh}) => {
  
  const [mentorFile, setMentorFile] = useState<File | null>(null);
  const [menteeFile, setMenteeFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<ImportPreviewResponse | null>(null);

  const [loading, setLoading] = useState<string | null>(null);
  const [importing, setImporting] = useState(false);
  const [loadingPreview, setLoadingPreview] = useState(false);

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

  const handlePreviewUpload = async () => {
    if (!mentorFile || !menteeFile) return;

    try {
      setLoadingPreview(true);

      const formData = new FormData();

      formData.append("mentor_file", mentorFile);
      formData.append("mentee_file", menteeFile);

      const data = await uploadCsvFiles(formData);

      setPreview(data);

    } catch (err) {
      console.error(err);
      alert("Failed to preview CSVs");
    } finally {
      setLoadingPreview(false);
    }
  };

  const handleConfirmImport = async () => {
    if (
      !mentorFile ||
      !menteeFile ||
      !preview
    ) {
      return;
    }

    try {
      setImporting(true);

      const formData = new FormData();

      formData.append(
        "mentor_file",
        mentorFile
      );

      formData.append(
        "mentee_file",
        menteeFile
      );

      formData.append(
        "mentor_mapping",
        JSON.stringify(
          preview.mentor.mapping
        )
      );

      formData.append(
        "mentee_mapping",
        JSON.stringify(
          preview.mentee.mapping
        )
      );

      await confirmImport(formData);
      
      onRefresh();

      alert("Import successful");

      setPreview(null);

    } catch (err) {
      console.error(err);
      alert("Import failed");
    } finally {
      setImporting(false);
    }
  };

  return (
    <div className="control-panel flex flex-col gap-2">
      <div className="border rounded p-4 bg-gray-50">
        <h3 className="font-bold mb-3">Import CSV Files</h3>

        {/* file inputs */}
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

        {/* import button */}
        <button
          onClick={handlePreviewUpload}
          disabled={!mentorFile || !menteeFile || loadingPreview}
          className={`
            px-4 py-2 rounded font-semibold transition-all duration-200 mt-4
            ${
              !mentorFile || !menteeFile || loadingPreview
                ? "bg-gray-300 text-gray-500 cursor-not-allowed opacity-70"
                : "bg-blue-600 text-white hover:bg-blue-700 hover:shadow-md cursor-pointer"
            }
          `}
        >
          {loadingPreview ? "Analyzing..." : "Preview Import"}
        </button>

        {preview && (
          <div className="grid grid-cols-2 gap-4 mt-6">
            <ImportMappingTable
              title="Mentor Mapping"
              headers={preview.mentor.headers}
              mapping={preview.mentor.mapping}
              fields={MENTOR_FIELDS}
              onChange={(column, value) => {
                setPreview((prev) => {
                  if (!prev) return prev;

                  return {
                    ...prev,

                    mentor: {
                      ...prev.mentor,

                      mapping: {
                        ...prev.mentor.mapping,
                        [column]: value,
                      },
                    },
                  };
                });
              }}
            />

            <ImportMappingTable
              title="Mentee Mapping"
              headers={preview.mentee.headers}
              mapping={preview.mentee.mapping}
              fields={MENTEE_FIELDS}
              onChange={(column, value) => {
                setPreview((prev) => {
                  if (!prev) return prev;

                  return {
                    ...prev,

                    mentee: {
                      ...prev.mentee,

                      mapping: {
                        ...prev.mentee.mapping,
                        [column]: value,
                      },
                    },
                  };
                });
              }}
            />
          </div>
        )}
        {preview && (
          <div className="mt-4">
            <button
              onClick={handleConfirmImport}
              disabled={importing}
              className={`
                px-4 py-2 rounded font-semibold
                ${
                  importing
                    ? "bg-gray-300 text-gray-500"
                    : "bg-green-600 text-white hover:bg-green-700"
                }
              `}
            >
              {importing
                ? "Importing..."
                : "Confirm Import"}
            </button>
          </div>
        )}
      </div>

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