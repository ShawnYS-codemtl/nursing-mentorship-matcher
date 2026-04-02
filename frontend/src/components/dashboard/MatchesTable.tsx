import React from "react";
import { useMatches } from "../../hooks/useMatches";

const MatchesTable: React.FC = () => {
  const { matches, loading, error } = useMatches();

  if (loading) return <p>Loading matches...</p>;
  if (error) return <p>Error loading matches</p>;

  return (
    <section className="matches-table mb-4">
      <h2 className="text-lg font-bold mb-2">Matches</h2>
      <table className="w-full border">
        <thead>
          <tr>
            <th>Id</th>
            <th>Mentor</th>
            <th>Mentee</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {matches.length === 0 ? (
            <tr>
              <td colSpan={3} className="text-center py-4">
                No matches yet
              </td>
            </tr>
          ) : (
            matches.map((m) => (
              <tr key={`${m.mentor.id}-${m.mentee.id}`}>
                <td>{m.id}</td>
                <td>{m.mentor.name}</td>
                <td>{m.mentee.name}</td>
                <td>{m.score}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
};

export default MatchesTable;