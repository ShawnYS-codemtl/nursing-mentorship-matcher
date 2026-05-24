import type { MatchSortKey } from "../../../types";

interface Props {
  label: string;
  column: MatchSortKey;
  sortKey: MatchSortKey | null;
  sortDirection: "asc" | "desc";
  width: number;
  onSort: (key: MatchSortKey) => void;
}

const SortableHeader: React.FC<Props> = ({
  label,
  column,
  sortKey,
  sortDirection,
  width,
  onSort,
}) => {
  const isActive = sortKey === column;

  return (
    <th
      style={{ width: `${width}%` }}
      className="cursor-pointer select-none text-left px-3 py-2 hover:bg-gray-200 text-sm font-semibold text-gray-700"
      onClick={() => onSort(column)}
    >
      <span className="flex items-center gap-1">
        {label}
        {isActive && (
          <svg
            className={`w-3 h-3 text-blue-600 transition-transform ${sortDirection === "desc" ? "rotate-180" : ""}`}
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
          </svg>
        )}
      </span>
    </th>
  );
};

export default SortableHeader;
