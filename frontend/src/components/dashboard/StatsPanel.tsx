import React from "react";

const StatsPanel: React.FC = () => {
  return (
    <section className="stats-panel mb-4 grid grid-cols-3 gap-4">
      <div className="bg-white p-4 shadow rounded">Total Mentors: 0</div>
      <div className="bg-white p-4 shadow rounded">Total Mentees: 0</div>
      <div className="bg-white p-4 shadow rounded">Matches Made: 0</div>
    </section>
  );
};

export default StatsPanel;