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

const MatchesTable: React.FC<Props> = ({refreshKey, onRefresh}) => {

    const { matches, setMatches, loading, error } = useMatches(refreshKey);
    const [collapsed, setCollapsed] = useState(false);

    const [sortKey, setSortKey] = useState<MatchSortKey>("id");
    const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

    const SORT_ACCESSORS: Record< MatchSortKey,(match: Match) => string | number | boolean> = {
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
            setSortDirection(prev => (prev === "asc" ? "desc" : "asc"));
        } else {
            setSortKey(key);
            setSortDirection("asc");
        }
    };

    async function handleToggleLock(matchId: number, newState: boolean) {
        try {
            await toggleMatchLock(matchId, newState);
            onRefresh()
            setMatches(prev =>
            prev.map(m =>
                m.id === matchId ? { ...m, is_locked: newState } : m
            )
            );
        } catch (err) {
            console.error(err);
        }
    }

    if (loading) return <p>Loading matches...</p>;
    if (error) return <p>Error loading matches</p>;

    const accessor = SORT_ACCESSORS[sortKey];

    const sortedMatches = [...matches].sort((a, b) => {
        const aVal = accessor(a);
        const bVal = accessor(b);

        if (typeof aVal === "number" && typeof bVal === "number") {
            return sortDirection === "asc"
            ? aVal - bVal
            : bVal - aVal;
        }

        return sortDirection === "asc"
            ? String(aVal).localeCompare(String(bVal))
            : String(bVal).localeCompare(String(aVal));
    });

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
                        <SortableHeader
                            label="Id"
                            column="id"
                            sortKey={sortKey}
                            sortDirection={sortDirection}
                            width={10}
                            onSort={handleSort}
                        />
                        <SortableHeader
                            label="Mentor"
                            column="mentor_name"
                            sortKey={sortKey}
                            sortDirection={sortDirection}
                            width={20}
                            onSort={handleSort}
                        />
                        <SortableHeader
                            label="Mentee"
                            column="mentee_name"
                            sortKey={sortKey}
                            sortDirection={sortDirection}
                            width={20}
                            onSort={handleSort}
                        />
                        <SortableHeader
                            label="Score"
                            column="score"
                            sortKey={sortKey}
                            sortDirection={sortDirection}
                            width={10}
                            onSort={handleSort}
                        />
                        <SortableHeader
                            label="Match Type"
                            column="match_type"
                            sortKey={sortKey}
                            sortDirection={sortDirection}
                            width={15}
                            onSort={handleSort}
                        />
                        <SortableHeader
                            label="Lock"
                            column="is_locked"
                            sortKey={sortKey}
                            sortDirection={sortDirection}
                            width={10}
                            onSort={handleSort}
                        />
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
                        sortedMatches.map((match) => (
                            <MatchRow key={match.id} match={match} onUnmatch={handleUnmatch} onToggle={handleToggleLock} />
                        ))
                    )}
                    </tbody>
                </table>
            }
        </section>
    );
};

export default MatchesTable;