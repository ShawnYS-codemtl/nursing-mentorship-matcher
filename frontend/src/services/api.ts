import type { Match, Stats, UnmatchedResponse, ImportRequest } from "../types";

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

export const fetchUnmatched = async (): Promise<UnmatchedResponse> => {
  const res = await fetch(`${BASE_URL}/unmatched`);
  if (!res.ok) throw new Error("Failed to fetch unmatched mentees");
  return res.json();
};

export const importData = async (body: ImportRequest): Promise<void> => {
    const res = await fetch(`${BASE_URL}/import`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error("Import failed");
    // return res.json();
}

export const runMatching = async () => {
  const res = await fetch(`${BASE_URL}/run-matching`, {
    method: "POST",
  });

  if (!res.ok) throw new Error("Matching failed");
  return res.json();
};

export const exportData = async (): Promise<void> => {
  const res = await fetch(`${BASE_URL}/export`);

  if (!res.ok) throw new Error("Export failed");

  const blob = await res.blob();

  // Create download link
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "matches.csv"; // matches backend filename
  document.body.appendChild(a);
  a.click();

  // Cleanup
  a.remove();
  window.URL.revokeObjectURL(url);
};

export const unmatch = async (matchId: number): Promise<void> => {
  const res = await fetch(`${BASE_URL}/matches/${matchId}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error("Failed to unmatch");
};

