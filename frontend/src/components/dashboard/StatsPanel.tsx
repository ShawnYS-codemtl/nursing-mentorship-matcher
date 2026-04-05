import React, {useState} from "react";
import { useStats } from "../../hooks/useStats";

const StatsPanel: React.FC = () => {
  const { stats, loading, error } = useStats();
  const [collapsed, setCollapsed] = useState(false);

  if (loading) return <p>Loading stats...</p>;
  if (error || !stats) return <p>Error loading stats</p>;

  return (
    <>
      <div className="flex items-center mb-2">
        <button
            onClick={() => setCollapsed((prev) => !prev)}
            className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
            {collapsed ? "▶" : "▼"}
        </button>
        <h2 className="text-lg font-bold mx-2">Stats</h2>

        
      </div>
      {!collapsed && 
      <section className="stats-panel mb-4 grid grid-cols-3 gap-4">
        <div className="bg-white p-4 shadow rounded flex-col flex">
          <p>Total Mentors: {stats.mentors}</p>
          <p>Total Mentees: {stats.mentees}</p>
          <p>Matches Made: {stats.matches}</p>
        </div>
        <div className="bg-white p-4 shadow rounded">
          <p>Unmatched mentees: {stats.unmatched_mentees}</p>
          <p>Available Mentors: {stats.available_mentors}</p>
        </div>
        <div className="bg-white p-4 shadow rounded">
          <p>Average Score: {stats.avg_score}</p>
          <p>Min Score: {stats.min_score}</p>
          <p>Max Score: {stats.max_score}</p>
          <p>Median Score: {stats.median_score}</p>
        </div>
      </section>
      }
    </>
  );
};

export default StatsPanel;