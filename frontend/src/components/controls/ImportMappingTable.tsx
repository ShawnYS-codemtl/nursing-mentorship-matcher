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
          {headers.map((header) => (
            <tr
              key={header}
              className="border-t"
            >
              <td className="p-2">
                {header}
              </td>

              <td className="p-2">
                <select
                  value={mapping[header] || "ignore"}
                  onChange={(e) =>
                    onChange(
                      header,
                      e.target.value
                    )
                  }
                  className="border rounded p-1 w-full"
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
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ImportMappingTable;