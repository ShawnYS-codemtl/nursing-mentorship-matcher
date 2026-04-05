import { useEffect, useState } from "react";
import type { Stats } from "../types";
import { fetchStats } from "../services/api";

export const useStats = (refreshKey: number) => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats()
      .then((data) => setStats(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [refreshKey]);

  return { stats, loading, error };
};