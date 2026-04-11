import { useEffect, useState } from "react";
import { getMatchScore } from "../services/api";
import type { DetailedMentee, AvailableMentor, ScoreBreakdown } from "../types";

export function useMatchScore(
  selectedMentee: DetailedMentee | null,
  selectedMentor: AvailableMentor | null
) {
  const [score, setScore] = useState<number | null>(null);
  const [breakdown, setBreakdown] = useState<ScoreBreakdown | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!selectedMentee || !selectedMentor) {
      setScore(null);
      setBreakdown(null);
      return;
    }

    let cancelled = false;

    const fetchScore = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await getMatchScore({
          mentor_id: selectedMentor.id,
          mentee_id: selectedMentee.id,
        });

        if (cancelled) return;

        setScore(res.score);
        setBreakdown(res.breakdown);

      } catch (err: unknown) {
        
        if (cancelled) return;
        const message =
            err instanceof Error ? err.message : "Failed to fetch score";
        setError(message);

      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchScore();

    return () => {
      cancelled = true;
    };
  }, [selectedMentee, selectedMentor]);

  return { score, breakdown, loading, error };
}