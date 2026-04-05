import React, {useState} from "react";
import { useUnmatched } from "../../hooks/useUnmatched";

const UnmatchedPanel: React.FC = () => {
  const { mentees, mentors, loading, error } = useUnmatched();
  const [collapsed, setCollapsed] = useState(false);

  if (loading) return <p>Loading unmatched mentees...</p>;
  if (error) return <p>Error loading unmatched mentees</p>;

  return (
    <section className="unmatched-panel mb-4">
      <div className="flex items-center mb-2">
        <button
          onClick={() => setCollapsed((prev) => !prev)}
          className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
          {collapsed ? "▶" : "▼"}
        </button>
        <h2 className="text-lg font-bold mx-2">Unmatched Mentees</h2>
      </div>

      {!collapsed && 
        <div>
        {mentees.map((m) => (
          <div key={m.id}>
            {m.name} ({m.program})
          </div>
        ))}

        <h2 className="text-lg font-bold mt-4 mb-2">Available Mentors</h2>

        {mentors.map((m) => (
          <div key={m.id}>
            {m.name} - Remaining: {m.remaining_capacity}
          </div>
        ))}
        </div>
      }
    </section>
  );
};

export default UnmatchedPanel;