import React, { useState } from "react";
import { uploadCsvFiles, runMatching, exportData } from "../../services/api";
import type { ImportPreviewResponse } from "../../types";
import ImportMappingTable from "./ImportMappingTable";
import { MENTEE_FIELDS, MENTOR_FIELDS } from "../../constants/importFields";

interface Props {
  onRefresh: () => void;
}

const ControlPanel: React.FC<Props> = ({onRefresh}) => {
  const [loading, setLoading] = useState<string | null>(null);
  // const [source, setSource] = useState<ImportSource>("csv");
  const [mentorFile, setMentorFile] = useState<File | null>(null);
  const [menteeFile, setMenteeFile] = useState<File | null>(null);
  // const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState<ImportPreviewResponse | null>(null);

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

  // const handleCsvUpload = async () => {
  //   if (!mentorFile || !menteeFile) {
  //     alert("Please select both CSV files");
  //     return;
  //   }

  //   try {
  //     setUploading(true);

  //     const formData = new FormData();

  //     formData.append("mentor_file", mentorFile);
  //     formData.append("mentee_file", menteeFile);

  //     await uploadCsvFiles(formData);

  //     onRefresh();

  //     alert("CSV import successful");
  //   } catch (err) {
  //     console.error(err);
  //     alert("Failed to import CSVs");
  //   } finally {
  //     setUploading(false);
  //   }
  // };

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