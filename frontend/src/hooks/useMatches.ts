import { useEffect, useState } from "react";
import type { Match } from "../types";
import { fetchMatches } from "../services/api";

export const useMatches = () => {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMatches()
      .then((data) => setMatches(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { matches, loading, error };
};