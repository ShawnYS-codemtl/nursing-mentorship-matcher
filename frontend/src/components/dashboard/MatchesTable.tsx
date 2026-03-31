import React from "react";

const MatchesTable: React.FC = () => {
  return (
    <section className="matches-table mb-4">
      <h2 className="text-lg font-bold mb-2">Matches</h2>
      <table className="w-full border">
        <thead>
          <tr>
            <th>Mentor</th>
            <th>Mentee</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan={3} className="text-center py-4">
              No matches yet
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  );
};

export default MatchesTable;