import React, { useState } from "react";
import { useMatches } from "../../hooks/useMatches";
import MatchRow from "./matches/MatchRow";
import { unmatch } from "../../services/api";

interface Props {
  refreshKey: number;
  onRefresh: () => void;
}

const MatchesTable: React.FC<Props> = ({refreshKey, onRefresh}) => {
  const { matches, loading, error } = useMatches(refreshKey);
  const [collapsed, setCollapsed] = useState(false);

  const handleUnmatch = async (matchId: number) => {
    try {
        await unmatch(matchId);
        onRefresh();
    } catch (err) {
        console.error(err);
        alert("Failed to unmatch");
    }
    };

  if (loading) return <p>Loading matches...</p>;
  if (error) return <p>Error loading matches</p>;

  return (
    <section className="matches-table mb-2">

        <div className="flex items-center mb-2">
             <button
                onClick={() => setCollapsed((prev) => !prev)}
                className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
            >
                {collapsed ? "▶" : "▼"}
            </button>

            <h2 className="text-lg font-bold mx-2">Matches</h2>

           
        </div>
        { !collapsed && 
            <table className="w-full border table-fixed">
                <thead>
                <tr className="bg-gray-100">
                    <th className="w-[5%] text-left"></th>
                    <th className="w-[10%] text-left">Id</th>
                    <th className="w-[20%] text-left">Mentor</th>
                    <th className="w-[20%] text-left">Mentee</th>
                    <th className="w-[10%] text-left">Score</th>
                    <th className="w-[15%] text-left">Match Type</th>
                    <th className="w-[10%] text-left">Lock</th>
                    <th className="w-[10%] text-left">Action</th>
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
                    matches.map((match) => (
                        <MatchRow key={match.id} match={match} onUnmatch={handleUnmatch} />
                    ))
                )}
                </tbody>
            </table>
        }
    </section>
  );
};

export default MatchesTable;