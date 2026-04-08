import React, { useState } from "react";
import type { Match } from "../../../types";
import MatchBreakdown from "./MatchBreakdown";

interface Props {
  match: Match;
  onUnmatch: (matchId: number) => void;
}

const MatchRow: React.FC<Props> = ({ match, onUnmatch }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <>
      {/* Main row */}
      <tr
        className="cursor-pointer hover:bg-blue-100"
        onClick={() => setExpanded((prev) => !prev)}
      >
        <td className="w-[5%] border-t">{expanded ? "▼" : "▶"}</td>
        <td className="w-[10%] border-t">{match.id}</td>
        <td className="w-[20%] text-left border-t">{match.mentor.name}</td>
        <td className="w-[20%] text-left border-t">{match.mentee.name}</td>
        <td className="w-[10%] border-t">{match.score}</td>
        <td className="w-[15%] border-t">{match.match_type}</td>
        <td className="w-[10%] text-left border-t">Lock</td>
        <td className="w-[10%] text-left border-t">
            <button
              onClick={(e) => {
                e.stopPropagation(); // 🔑 prevent row expand toggle
                onUnmatch(match.id);
              }}
              className="text-red-500 hover:underline"
            >
              Unmatch
            </button>

        </td>
      </tr>

      {/* Expanded row */}
      {expanded && (
        <tr className="bg-gray-50">
          <td colSpan={8} className="p-4 full">
            <div className="grid grid-cols-2 gap-6">

              {/* Mentor details */}
              <div>
                <h3 className="font-bold mb-2">Mentor</h3>
                <p><strong>Name:</strong> {match.mentor.name}</p>
                <p><strong>Email:</strong> {match.mentor.email}</p>
              </div>

              {/* Mentee details */}
              <div>
                <h3 className="font-bold mb-2">Mentee</h3>
                <p><strong>Name:</strong> {match.mentee.name}</p>
                <p><strong>Email:</strong> {match.mentee.email}</p>
              </div>

              {/* Match breakdown */}
              <div className="col-span-2">
                <MatchBreakdown reason={match.match_reason} />
              </div>

            </div>
          </td>
        </tr>
      )}
    </>
  );
};

export default MatchRow;