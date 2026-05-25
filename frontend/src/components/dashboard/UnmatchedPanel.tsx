import React, { useState } from "react";
import { useUnmatched } from "../../hooks/useUnmatched";
import { useSelectionController } from "../../hooks/useSelectionController";
import { overrideMatch } from "../../services/api";
import { useMatchScore } from "../../hooks/useMatchScore";

type SortField = "name" | "program" | "year_in_program";
type SortDir = "asc" | "desc";

function sortList<T extends { name: string; program: string; year_in_program: number }>(
  items: T[],
  field: SortField,
  dir: SortDir
): T[] {
  return [...items].sort((a, b) => {
    const av = field === "year_in_program" ? a[field] : a[field].toLowerCase();
    const bv = field === "year_in_program" ? b[field] : b[field].toLowerCase();
    if (av < bv) return dir === "asc" ? -1 : 1;
    if (av > bv) return dir === "asc" ? 1 : -1;
    return 0;
  });
}

const SORT_LABELS: Record<SortField, string> = { name: "Name", program: "Program", year_in_program: "Year" };

interface Props {
  refreshKey: number;
  onRefresh: () => void;
}

const UnmatchedPanel: React.FC<Props> = ({ refreshKey, onRefresh }) => {
  const { mentees, mentors, loading, error } = useUnmatched(refreshKey);
  const [collapsed, setCollapsed] = useState(false);
  const [menteeSortField, setMenteeSortField] = useState<SortField>("name");
  const [menteeSortDir, setMenteeSortDir] = useState<SortDir>("asc");
  const [mentorSortField, setMentorSortField] = useState<SortField>("name");
  const [mentorSortDir, setMentorSortDir] = useState<SortDir>("asc");
  const {
    selectedMentee,
    selectedMentor,
    sidePanelMode,
    openMenteePicker,
    openMentorPicker,
    closeSidePanel,
    selectMentee,
    selectMentor,
    resetSelection,
  } = useSelectionController();
  const { score, breakdown, loading: scoreLoading } = useMatchScore(selectedMentee, selectedMentor);

  const handleAssign = async () => {
    if (!selectedMentee || !selectedMentor) return;
    try {
      await overrideMatch({ mentor_id: selectedMentor.id, mentee_id: selectedMentee.id });
      resetSelection();
      onRefresh();
    } catch (err) {
      console.error(err);
      alert("Failed to assign match");
    }
  };

  if (loading) return <p className="text-sm text-gray-500">Loading unmatched mentees...</p>;
  if (error) return <p className="text-sm text-red-500">Error loading unmatched mentees</p>;

  return (
    <section className="unmatched-panel mb-4">
      <button
        onClick={() => setCollapsed((prev) => !prev)}
        className="w-full flex items-center justify-between px-1 py-2 hover:bg-gray-100 rounded group mb-2"
      >
        <h2 className="text-lg font-semibold text-gray-800">
          Manual Matching
          {mentees.length > 0 && (
            <span className="ml-2 text-sm font-normal text-gray-400">({mentees.length} unmatched)</span>
          )}
        </h2>
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform ${collapsed ? "-rotate-90" : ""}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {!collapsed && (
        <>
          {mentees.length === 0 ? (
            <p className="text-sm text-gray-400 py-4">All mentees have been matched.</p>
          ) : (
            <>
              <div className="grid grid-cols-3 gap-4 mb-4">
                {/* Mentee card */}
                <div
                  onClick={openMenteePicker}
                  className={`bg-blue-50 border rounded-lg p-4 min-h-[120px] cursor-pointer transition-all hover:ring-2 hover:ring-blue-300 ${
                    sidePanelMode === "mentee-picker" ? "ring-2 ring-blue-400" : "border-blue-200"
                  }`}
                >
                  <h3 className="text-sm font-semibold text-blue-800 mb-2">Selected Mentee</h3>
                  {selectedMentee ? (
                    <div className="space-y-0.5 text-sm">
                      <p className="font-medium text-gray-900">{selectedMentee.name}</p>
                      <p className="text-gray-500">{selectedMentee.email}</p>
                      <p className="text-gray-600">Program: {selectedMentee.program}</p>
                      <p className="text-gray-600">Year: {selectedMentee.year_in_program}</p>
                      <p className="text-gray-600">Specialties: {selectedMentee.specialties.join(", ")}</p>
                      <p className="text-gray-600">Languages: {selectedMentee.languages_needed.join(", ")}</p>
                    </div>
                  ) : (
                    <p className="text-blue-400 text-sm">Click to select a mentee</p>
                  )}
                </div>

                {/* Mentor card */}
                <div
                  onClick={openMentorPicker}
                  className={`bg-green-50 border rounded-lg p-4 min-h-[120px] cursor-pointer transition-all hover:ring-2 hover:ring-green-300 ${
                    sidePanelMode === "mentor-picker" ? "ring-2 ring-green-400" : "border-green-200"
                  }`}
                >
                  <h3 className="text-sm font-semibold text-green-800 mb-2">Selected Mentor</h3>
                  {selectedMentor ? (
                    <div className="space-y-0.5 text-sm">
                      <p className="font-medium text-gray-900">{selectedMentor.name}</p>
                      <p className="text-gray-500">{selectedMentor.email}</p>
                      <p className="text-gray-600">Program: {selectedMentor.program}</p>
                      <p className="text-gray-600">Year: {selectedMentor.year_in_program}</p>
                      <p className="text-gray-600">Specialties: {selectedMentor.specialties.join(", ")}</p>
                      <p className="text-gray-600">Languages: {selectedMentor.languages.join(", ")}</p>
                      <p className="text-gray-600">Capacity: {selectedMentor.remaining_capacity}</p>
                    </div>
                  ) : (
                    <p className="text-green-500 text-sm">Click to select a mentor</p>
                  )}
                </div>

                {/* Picker panel */}
                <div className="bg-white border border-gray-200 rounded-lg p-4 min-h-[120px] overflow-y-auto max-h-64">
                  {sidePanelMode === "none" && (
                    <p className="text-sm text-gray-400">Click a card to browse options</p>
                  )}

                  {sidePanelMode === "mentee-picker" && (
                    <>
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="text-sm font-semibold text-gray-700">Select Mentee</h3>
                        <button onClick={closeSidePanel} className="text-xs text-gray-400 hover:text-gray-600">
                          Close
                        </button>
                      </div>
                      <div className="flex gap-1 mb-2">
                        {(Object.keys(SORT_LABELS) as SortField[]).map((f) => (
                          <button
                            key={f}
                            onClick={() => {
                              if (menteeSortField === f) setMenteeSortDir((d) => (d === "asc" ? "desc" : "asc"));
                              else { setMenteeSortField(f); setMenteeSortDir("asc"); }
                            }}
                            className={`px-2 py-0.5 text-xs rounded border ${
                              menteeSortField === f
                                ? "bg-blue-100 border-blue-400 font-semibold text-blue-800"
                                : "border-gray-300 text-gray-500 hover:bg-gray-50"
                            }`}
                          >
                            {SORT_LABELS[f]}{menteeSortField === f ? (menteeSortDir === "asc" ? " ▲" : " ▼") : ""}
                          </button>
                        ))}
                      </div>
                      {sortList(mentees, menteeSortField, menteeSortDir).map((m) => (
                        <div
                          key={m.id}
                          onClick={() => selectMentee(m)}
                          className={`px-3 py-2 rounded text-sm cursor-pointer mb-1 ${
                            selectedMentee?.id === m.id
                              ? "bg-blue-100 text-blue-800 font-medium"
                              : "hover:bg-gray-100 text-gray-700"
                          }`}
                        >
                          {m.name} — {m.program} · Year {m.year_in_program}
                        </div>
                      ))}
                    </>
                  )}

                  {sidePanelMode === "mentor-picker" && (
                    <>
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="text-sm font-semibold text-gray-700">Select Mentor</h3>
                        <button onClick={closeSidePanel} className="text-xs text-gray-400 hover:text-gray-600">
                          Close
                        </button>
                      </div>
                      <div className="flex gap-1 mb-2">
                        {(Object.keys(SORT_LABELS) as SortField[]).map((f) => (
                          <button
                            key={f}
                            onClick={() => {
                              if (mentorSortField === f) setMentorSortDir((d) => (d === "asc" ? "desc" : "asc"));
                              else { setMentorSortField(f); setMentorSortDir("asc"); }
                            }}
                            className={`px-2 py-0.5 text-xs rounded border ${
                              mentorSortField === f
                                ? "bg-green-100 border-green-400 font-semibold text-green-800"
                                : "border-gray-300 text-gray-500 hover:bg-gray-50"
                            }`}
                          >
                            {SORT_LABELS[f]}{mentorSortField === f ? (mentorSortDir === "asc" ? " ▲" : " ▼") : ""}
                          </button>
                        ))}
                      </div>
                      {sortList(mentors, mentorSortField, mentorSortDir).map((m) => (
                        <div
                          key={m.id}
                          onClick={() => selectMentor(m)}
                          className={`px-3 py-2 rounded text-sm cursor-pointer mb-1 ${
                            selectedMentor?.id === m.id
                              ? "bg-green-100 text-green-800 font-medium"
                              : "hover:bg-gray-100 text-gray-700"
                          }`}
                        >
                          {m.name} — {m.program} · Cap: {m.remaining_capacity} · Year {m.year_in_program}
                        </div>
                      ))}
                    </>
                  )}
                </div>
              </div>

              {selectedMentee && selectedMentor && (
                <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  {scoreLoading ? (
                    <p className="text-sm text-gray-500">Calculating score...</p>
                  ) : (
                    <>
                      {breakdown?.constraints_violated && (
                        <div className="flex items-center gap-2 mb-3 px-3 py-2 bg-red-50 border border-red-200 rounded-md">
                          <span className="text-red-500">⚠</span>
                          <span className="text-sm text-red-700 font-medium">
                            Constraint violated — would score{" "}
                            <strong>{breakdown.potential_score ?? 0}/100</strong> if eligible
                          </span>
                        </div>
                      )}
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-sm font-semibold text-gray-700">Match Score</span>
                        <span className={`text-2xl font-bold ${breakdown?.constraints_violated ? "text-red-400" : "text-gray-900"}`}>
                          {score}
                        </span>
                      </div>
                      {breakdown && (() => {
                        const HIDDEN_KEYS = new Set(["reasons", "constraints_violated", "potential_score", "explicit_choice"]);
                        const reasons: string[] = Array.isArray(breakdown.reasons) ? breakdown.reasons : [];
                        const scoreFields = Object.entries(breakdown).filter(([k]) => !HIDDEN_KEYS.has(k));
                        return (
                          <>
                            <ul className="grid grid-cols-2 gap-x-6 gap-y-1 mb-3">
                              {scoreFields.map(([k, v]) => (
                                <li key={k} className="flex justify-between text-sm">
                                  <span className="text-gray-500">{k}</span>
                                  <span className="font-medium text-gray-700">{String(v)}</span>
                                </li>
                              ))}
                            </ul>
                            {reasons.length > 0 && (
                              <div className="border-t border-yellow-200 pt-3">
                                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Reasons</p>
                                <ul className="space-y-1">
                                  {reasons.map((r, i) => (
                                    <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                                      <span className="text-yellow-400 mt-0.5">•</span>
                                      {r}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </>
                        );
                      })()}
                    </>
                  )}
                </div>
              )}

              <button
                disabled={!selectedMentee || !selectedMentor}
                onClick={handleAssign}
                className={`w-full py-2 rounded-lg text-sm font-semibold transition-colors ${
                  selectedMentee && selectedMentor
                    ? "bg-blue-600 text-white hover:bg-blue-700"
                    : "bg-gray-200 text-gray-400 cursor-not-allowed"
                }`}
              >
                Match Selected Pair
              </button>
            </>
          )}
        </>
      )}
    </section>
  );
};

export default UnmatchedPanel;
