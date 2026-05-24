import React from "react";
import type { MatchReason } from "../../../types";

interface Props {
  reason: MatchReason;
}

const MatchBreakdown: React.FC<Props> = ({ reason }) => {
  const scoreRows: { label: string; value: number | undefined }[] = [
    { label: "Program Alignment",     value: reason.program_alignment },
    { label: "Specialty Alignment",   value: reason.specialty_alignment },
    { label: "Extracurricular",       value: reason.identity_extracurricular },
    { label: "Specialty Mismatch",    value: reason.specialty_mismatch },
  ];

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Match Breakdown</h3>

      <div className="grid grid-cols-2 gap-x-8 gap-y-2 mb-3">
        {scoreRows.filter(({ value }) => value !== undefined).map(({ label, value }) => (
          <div key={label} className="flex justify-between items-center">
            <span className="text-sm text-gray-500">{label}</span>
            <span className={`text-sm font-semibold ${(value ?? 0) < 0 ? "text-red-600" : "text-blue-700"}`}>
              {value}
            </span>
          </div>
        ))}

        {reason.constraints_violated !== undefined && (
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">Constraints Violated</span>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
              reason.constraints_violated
                ? "bg-red-100 text-red-700"
                : "bg-green-100 text-green-700"
            }`}>
              {reason.constraints_violated ? "Yes" : "No"}
            </span>
          </div>
        )}

        {reason.explicit_choice !== undefined && (
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">Explicit Choice</span>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
              reason.explicit_choice
                ? "bg-blue-100 text-blue-700"
                : "bg-gray-100 text-gray-500"
            }`}>
              {reason.explicit_choice ? "Yes" : "No"}
            </span>
          </div>
        )}
      </div>

      {reason.reasons && reason.reasons.length > 0 && (
        <div className="border-t border-gray-200 pt-3">
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Reasons</h4>
          <ul className="space-y-1">
            {reason.reasons.map((r, i) => (
              <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-gray-300 mt-0.5">•</span>
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MatchBreakdown;
