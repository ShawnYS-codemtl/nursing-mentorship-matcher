import React from "react";
import type { MatchReason } from "../../../types";

interface Props {
  reason: MatchReason;
}

const MatchBreakdown: React.FC<Props> = ({ reason }) => {
  return (
    <div>
      <h3 className="font-bold mb-2">Match Breakdown</h3>

      {/* Score components */}
      <div className="grid grid-cols-2 gap-2 text-sm">
        {reason.program_alignment !== undefined && (
          <p>Program Alignment: {reason.program_alignment}</p>
        )}

        {reason.specialty_alignment !== undefined && (
          <p>Specialty Alignment: {reason.specialty_alignment}</p>
        )}

        {reason.identity_extracurricular !== undefined && (
          <p>Extracurricular: {reason.identity_extracurricular}</p>
        )}

        {reason.specialty_mismatch !== undefined && (
          <p>Specialty Mismatch: {reason.specialty_mismatch}</p>
        )}

        {reason.constraints_violated !== undefined && (
          <p>
            Constraints Violated:{" "}
            {reason.constraints_violated ? "Yes" : "No"}
          </p>
        )}

        {reason.explicit_choice !== undefined && (
          <p>
            Explicit Choice:{" "}
            {reason.explicit_choice ? "Yes" : "No"}
          </p>
        )}
      </div>

      {/* Reasons list */}
      {reason.reasons && reason.reasons.length > 0 && (
        <div className="mt-3">
          <h4 className="font-semibold">Reasons:</h4>
          <ul className="list-disc ml-5">
            {reason.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MatchBreakdown;