import React, { useState } from "react";
import { useStats } from "../../hooks/useStats";

interface Props {
  refreshKey: number;
}

const StatsPanel: React.FC<Props> = ({ refreshKey }) => {
  const { stats, loading, error } = useStats(refreshKey);
  const [collapsed, setCollapsed] = useState(false);

  if (loading) return <p className="text-sm text-gray-500">Loading stats...</p>;
  if (error || !stats) return <p className="text-sm text-red-500">Error loading stats</p>;

  const cards = [
    { label: "Total Mentors",       value: stats.mentors },
    { label: "Total Mentees",       value: stats.mentees },
    { label: "Matches Made",        value: stats.matches },
    { label: "Unmatched Mentees",   value: stats.unmatched_mentees },
    { label: "Available Mentors",   value: stats.available_mentors },
    { label: "Avg Score",           value: stats.avg_score },
    { label: "Min / Max Score",     value: `${stats.min_score} / ${stats.max_score}` },
  ];

  return (
    <section className="mb-4">
      <button
        onClick={() => setCollapsed((prev) => !prev)}
        className="w-full flex items-center justify-between px-1 py-2 hover:bg-gray-100 rounded group mb-2"
      >
        <h2 className="text-lg font-semibold text-gray-800">Stats</h2>
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform ${collapsed ? "-rotate-90" : ""}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {!collapsed && (
        <div className="grid grid-cols-7 gap-3">
          {cards.map(({ label, value }) => (
            <div key={label} className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <p className="text-2xl font-bold text-gray-900">{value}</p>
              <p className="text-xs text-gray-500 mt-1">{label}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default StatsPanel;
