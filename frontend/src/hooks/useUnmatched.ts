import { useEffect, useState } from "react";
import type { DetailedMentee, AvailableMentor } from "../types";
import { fetchUnmatched } from "../services/api";

export const useUnmatched = () => {
  const [mentees, setMentees] = useState<DetailedMentee[]>([]);
  const [mentors, setMentors] = useState<AvailableMentor[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUnmatched()
      .then((data) => {
        setMentees(data.unmatched_mentees);
        setMentors(data.available_mentors);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { mentees, mentors, loading, error };
};