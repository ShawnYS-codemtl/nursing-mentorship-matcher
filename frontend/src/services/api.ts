import type { Match, Stats, Mentee } from "../types";

const BASE_URL = "http://127.0.0.1:5000";

export const fetchMatches = async (): Promise<Match[]> => {
  const res = await fetch(`${BASE_URL}/matches`);
  if (!res.ok) throw new Error("Failed to fetch matches");
  return res.json();
};

export const fetchStats = async (): Promise<Stats> => {
  const res = await fetch(`${BASE_URL}/stats`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
};

export const fetchUnmatched = async (): Promise<Mentee[]> => {
  const res = await fetch(`${BASE_URL}/unmatched`);
  if (!res.ok) throw new Error("Failed to fetch unmatched mentees");
  return res.json();
};