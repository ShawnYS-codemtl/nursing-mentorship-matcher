import type { MatchSortKey } from "../../../types";

interface Props {
  label: string;
  column: MatchSortKey;
  sortKey: MatchSortKey| null;
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
      className={`cursor-pointer select-none text-left w-[${width}%]`}
      onClick={() => onSort(column)}
    >
      {label}{" "}
      {isActive && (sortDirection === "asc" ? "▲" : "▼")}
    </th>
  );
};

export default SortableHeader;