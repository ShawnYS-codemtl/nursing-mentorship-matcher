import React, { useState } from "react";
import { useMatches } from "../../hooks/useMatches";
import MatchRow from "./matches/MatchRow";
import SortableHeader from "./matches/SortableHeader";
import { unmatch, toggleMatchLock } from "../../services/api";
import type { Match, MatchSortKey, SortDirection } from "../../types";

interface Props {
  refreshKey: number;
  onRefresh: () => void;
}

const MatchesTable: React.FC<Props> = ({ refreshKey, onRefresh }) => {
  const { matches, setMatches, loading, error } = useMatches(refreshKey);
  const [collapsed, setCollapsed] = useState(false);
  const [sortKey, setSortKey] = useState<MatchSortKey>("id");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const SORT_ACCESSORS: Record<MatchSortKey, (match: Match) => string | number | boolean> = {
    id: (m) => m.id,
    mentor_name: (m) => m.mentor.name,
    mentee_name: (m) => m.mentee.name,
    score: (m) => m.score,
    match_type: (m) => m.match_type,
    is_locked: (m) => m.is_locked,
  };

  const handleUnmatch = async (matchId: number) => {
    try {
      await unmatch(matchId);
      onRefresh();
    } catch (err) {
      console.error(err);
      alert("Failed to unmatch");
    }
  };

  const handleSort = (key: MatchSortKey) => {
    if (sortKey === key) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDirection("asc");
    }
  };

  async function handleToggleLock(matchId: number, newState: boolean) {
    try {
      await toggleMatchLock(matchId, newState);
      onRefresh();
      setMatches((prev) =>
        prev.map((m) => (m.id === matchId ? { ...m, is_locked: newState } : m))
      );
    } catch (err) {
      console.error(err);
    }
  }

  if (loading) return <p className="text-sm text-gray-500">Loading matches...</p>;
  if (error) return <p className="text-sm text-red-500">Error loading matches</p>;

  const accessor = SORT_ACCESSORS[sortKey];
  const sortedMatches = [...matches].sort((a, b) => {
    const aVal = accessor(a);
    const bVal = accessor(b);
    if (typeof aVal === "number" && typeof bVal === "number") {
      return sortDirection === "asc" ? aVal - bVal : bVal - aVal;
    }
    return sortDirection === "asc"
      ? String(aVal).localeCompare(String(bVal))
      : String(bVal).localeCompare(String(aVal));
  });

  return (
    <section className="matches-table mb-4">
      <button
        onClick={() => setCollapsed((prev) => !prev)}
        className="w-full flex items-center justify-between px-1 py-2 hover:bg-gray-100 rounded group mb-2"
      >
        <h2 className="text-lg font-semibold text-gray-800">
          Matches
          {matches.length > 0 && (
            <span className="ml-2 text-sm font-normal text-gray-400">({matches.length})</span>
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
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
          <table className="w-full border-collapse table-fixed">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-200">
                <th className="w-[5%] px-3 py-2" />
                <SortableHeader label="ID"         column="id"          sortKey={sortKey} sortDirection={sortDirection} width={8}  onSort={handleSort} />
                <SortableHeader label="Mentor"     column="mentor_name" sortKey={sortKey} sortDirection={sortDirection} width={20} onSort={handleSort} />
                <SortableHeader label="Mentee"     column="mentee_name" sortKey={sortKey} sortDirection={sortDirection} width={20} onSort={handleSort} />
                <SortableHeader label="Score"      column="score"       sortKey={sortKey} sortDirection={sortDirection} width={9}  onSort={handleSort} />
                <SortableHeader label="Match Type" column="match_type"  sortKey={sortKey} sortDirection={sortDirection} width={15} onSort={handleSort} />
                <SortableHeader label="Lock"       column="is_locked"   sortKey={sortKey} sortDirection={sortDirection} width={10} onSort={handleSort} />
                <th className="w-[13%] px-3 py-2 text-left text-sm font-semibold text-gray-700">Action</th>
              </tr>
            </thead>
            <tbody>
              {matches.length === 0 ? (
                <tr>
                  <td colSpan={8} className="text-center py-8 text-gray-400 text-sm">
                    No matches yet
                  </td>
                </tr>
              ) : (
                sortedMatches.map((match) => (
                  <MatchRow
                    key={match.id}
                    match={match}
                    onUnmatch={handleUnmatch}
                    onToggle={handleToggleLock}
                  />
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
};

export default MatchesTable;
