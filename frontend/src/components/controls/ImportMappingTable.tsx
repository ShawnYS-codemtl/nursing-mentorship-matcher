import type { ColumnMapping } from "../../types";

interface Props {
  title: string;

  headers: string[];

  mapping: ColumnMapping;

  fields: string[];

  onChange: (
    column: string,
    value: string
  ) => void;
}

const ImportMappingTable: React.FC<Props> = ({
  title,
  headers,
  mapping,
  fields,
  onChange,
}) => {
  const fieldCounts = Object.values(mapping).reduce<Record<string, number>>((acc, v) => {
    if (v && v !== "ignore") acc[v] = (acc[v] ?? 0) + 1;
    return acc;
  }, {});
  const duplicateFields = new Set(
    Object.entries(fieldCounts).filter(([, c]) => c > 1).map(([f]) => f)
  );

  return (
    <div className="border rounded p-4 bg-white shadow">
      <h3 className="font-bold text-lg mb-4">
        {title}
      </h3>

      <table className="w-full table-fixed border">
        <thead>
          <tr className="bg-gray-100">
            <th className="text-left p-2 w-2/3 break-words">
              CSV Column
            </th>

            <th className="text-left p-2 w-1/3">
              System Field
            </th>
          </tr>
        </thead>

        <tbody>
          {headers.map((header) => {
            const currentValue = mapping[header] || "ignore";
            const isDuplicate = duplicateFields.has(currentValue);
            return (
              <tr
                key={header}
                className="border-t"
              >
                <td className="p-2 text-sm">
                  {header}
                </td>

                <td className="p-2">
                  <div className="flex items-center gap-2">
                    <select
                      value={currentValue}
                      onChange={(e) =>
                        onChange(
                          header,
                          e.target.value
                        )
                      }
                      className={`border rounded p-1 w-full text-sm ${
                        isDuplicate
                          ? "border-red-400 bg-red-50 text-red-800"
                          : ""
                      }`}
                    >
                      {fields.map((field) => (
                        <option
                          key={field}
                          value={field}
                        >
                          {field}
                        </option>
                      ))}
                    </select>
                    {isDuplicate && (
                      <span className="text-red-500 text-xs whitespace-nowrap">⚠ duplicate</span>
                    )}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {duplicateFields.size > 0 && (
        <p className="mt-3 text-sm text-red-600">
          Mapped more than once: <span className="font-semibold">{[...duplicateFields].join(", ")}</span>
        </p>
      )}
    </div>
  );
};

export default ImportMappingTable;
