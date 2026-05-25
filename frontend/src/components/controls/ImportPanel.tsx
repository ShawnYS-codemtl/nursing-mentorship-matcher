import React, { useState } from "react";
import { uploadCsvFiles, confirmImport } from "../../services/api";
import type { ColumnMapping, ImportPreviewResponse } from "../../types";
import ImportMappingTable from "./ImportMappingTable";
import { MENTEE_FIELDS, MENTOR_FIELDS } from "../../constants/importFields";

interface Props {
  onRefresh: () => void;
}

function getDuplicateFields(mapping: ColumnMapping): Set<string> {
  const counts = Object.values(mapping).reduce<Record<string, number>>((acc, v) => {
    if (v && v !== "ignore") acc[v] = (acc[v] ?? 0) + 1;
    return acc;
  }, {});
  return new Set(Object.entries(counts).filter(([, c]) => c > 1).map(([f]) => f));
}

function parseImportError(err: unknown): { message: string; details: string[] } {
  let message = "Import failed. Please try again.";
  const details: string[] = [];
  try {
    const body = JSON.parse((err as Error).message);
    if (body.error === "Validation failed") {
      message = "Validation failed. Fix the issues below and try again.";
      const fmt = (errors: any[], label: string) =>
        (errors ?? []).forEach((e) => {
          if (e.missing_fields?.length)
            details.push(`${label} row ${e.row}: missing — ${e.missing_fields.join(", ")}`);
          (e.invalid_fields ?? []).forEach((f: any) =>
            details.push(`${label} row ${e.row}: invalid value for "${f.field}" (got: ${JSON.stringify(f.value)})`)
          );
        });
      fmt(body.mentor_errors, "Mentor");
      fmt(body.mentee_errors, "Mentee");
    } else if (body.error) {
      message = body.error;
    }
  } catch { /* non-JSON error — keep generic message */ }
  return { message, details };
}

const ImportPanel: React.FC<Props> = ({ onRefresh }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [mentorFile, setMentorFile] = useState<File | null>(null);
  const [menteeFile, setMenteeFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<ImportPreviewResponse | null>(null);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [importing, setImporting] = useState(false);
  const [importError, setImportError] = useState<{ message: string; details: string[] } | null>(null);

  const handlePreviewUpload = async () => {
    if (!mentorFile || !menteeFile) return;

    try {
      setLoadingPreview(true);
      setImportError(null);
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
    if (!mentorFile || !menteeFile || !preview) return;

    const mentorDups = getDuplicateFields(preview.mentor.mapping);
    const menteeDups = getDuplicateFields(preview.mentee.mapping);
    if (mentorDups.size > 0 || menteeDups.size > 0) {
      const details: string[] = [];
      if (mentorDups.size > 0) details.push(`Mentor CSV: duplicate fields — ${[...mentorDups].join(", ")}`);
      if (menteeDups.size > 0) details.push(`Mentee CSV: duplicate fields — ${[...menteeDups].join(", ")}`);
      setImportError({ message: "Fix duplicate mappings before importing.", details });
      return;
    }

    try {
      setImporting(true);
      setImportError(null);
      const formData = new FormData();
      formData.append("mentor_file", mentorFile);
      formData.append("mentee_file", menteeFile);
      formData.append("mentor_mapping", JSON.stringify(preview.mentor.mapping));
      formData.append("mentee_mapping", JSON.stringify(preview.mentee.mapping));
      await confirmImport(formData);
      onRefresh();
      setPreview(null);
    } catch (err) {
      console.error(err);
      setImportError(parseImportError(err));
    } finally {
      setImporting(false);
    }
  };

  return (
    <section className="import-panel mb-2">
      <button
        onClick={() => setCollapsed((prev) => !prev)}
        className="w-full flex items-center justify-between px-1 py-2 hover:bg-gray-100 rounded group mb-2"
      >
        <h2 className="text-lg font-semibold text-gray-800">Import CSV Files</h2>
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform ${collapsed ? "-rotate-90" : ""}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {!collapsed && (
        <div className="border rounded p-4 bg-gray-50">
          <div className="flex flex-col gap-2">
            <div>
              <label className="block font-semibold mb-1">Mentor CSV</label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setMentorFile(e.target.files?.[0] || null)}
              />
            </div>
            <div>
              <label className="block font-semibold mb-1">Mentee CSV</label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setMenteeFile(e.target.files?.[0] || null)}
              />
            </div>
          </div>

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
                  setImportError(null);
                  setPreview((prev) => {
                    if (!prev) return prev;
                    return {
                      ...prev,
                      mentor: {
                        ...prev.mentor,
                        mapping: { ...prev.mentor.mapping, [column]: value },
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
                  setImportError(null);
                  setPreview((prev) => {
                    if (!prev) return prev;
                    return {
                      ...prev,
                      mentee: {
                        ...prev.mentee,
                        mapping: { ...prev.mentee.mapping, [column]: value },
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
                  ${importing ? "bg-gray-300 text-gray-500" : "bg-green-600 text-white hover:bg-green-700"}
                `}
              >
                {importing ? "Importing..." : "Confirm Import"}
              </button>

              {importError && (
                <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg text-sm">
                  <p className="font-semibold text-red-700">{importError.message}</p>
                  {importError.details.length > 0 && (
                    <ul className="mt-1 space-y-0.5 text-red-600 list-disc list-inside">
                      {importError.details.map((d, i) => <li key={i}>{d}</li>)}
                    </ul>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default ImportPanel;
