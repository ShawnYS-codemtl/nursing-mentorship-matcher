import React, { useState } from "react";
import type { Match } from "../../../types";
import MatchBreakdown from "./MatchBreakdown";

interface Props {
  match: Match;
  onUnmatch: (matchId: number) => void;
  onToggle: (matchId: number, newState: boolean) => void;
}

const MatchRow: React.FC<Props> = ({ match, onUnmatch, onToggle }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <>
      <tr
        className="cursor-pointer hover:bg-blue-50 border-t border-gray-100"
        onClick={() => setExpanded((prev) => !prev)}
      >
        <td className="px-3 py-2 text-gray-400 text-xs">
          {expanded ? "▼" : "▶"}
        </td>
        <td className="px-3 py-2 text-sm text-gray-600">{match.id}</td>
        <td className="px-3 py-2 text-sm font-medium text-gray-900">{match.mentor.name}</td>
        <td className="px-3 py-2 text-sm font-medium text-gray-900">{match.mentee.name}</td>
        <td className="px-3 py-2 text-sm text-gray-700">{match.score}</td>
        <td className="px-3 py-2 text-sm text-gray-500">{match.match_type}</td>
        <td className="px-3 py-2">
          <button
            onClick={(e) => { e.stopPropagation(); onToggle(match.id, !match.is_locked); }}
            className={`px-2 py-1 rounded text-xs font-medium border transition-colors ${
              match.is_locked
                ? "bg-amber-100 text-amber-800 border-amber-300 hover:bg-amber-200"
                : "bg-gray-100 text-gray-600 border-gray-300 hover:bg-gray-200"
            }`}
          >
            {match.is_locked ? "Locked" : "Unlocked"}
          </button>
        </td>
        <td className="px-3 py-2">
          <button
            onClick={(e) => { e.stopPropagation(); onUnmatch(match.id); }}
            className="px-2 py-1 rounded text-xs font-medium border border-red-300 text-red-600 hover:bg-red-50 transition-colors"
          >
            Unmatch
          </button>
        </td>
      </tr>

      {expanded && (
        <tr className="bg-gray-50 border-t border-gray-100">
          <td colSpan={8} className="px-6 py-4">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Mentor</h3>
                <div className="space-y-1 text-sm">
                  <p><span className="text-gray-500">Name:</span> <span className="font-medium">{match.mentor.name}</span></p>
                  <p><span className="text-gray-500">Email:</span> {match.mentor.email}</p>
                  <p><span className="text-gray-500">Year:</span> {match.mentor.year}</p>
                  <p><span className="text-gray-500">Program:</span> {match.mentor.program}</p>
                </div>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Mentee</h3>
                <div className="space-y-1 text-sm">
                  <p><span className="text-gray-500">Name:</span> <span className="font-medium">{match.mentee.name}</span></p>
                  <p><span className="text-gray-500">Email:</span> {match.mentee.email}</p>
                  <p><span className="text-gray-500">Year:</span> {match.mentee.year}</p>
                  <p><span className="text-gray-500">Program:</span> {match.mentee.program}</p>
                </div>
              </div>
              <div className="col-span-2 border-t border-gray-200 pt-4">
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
