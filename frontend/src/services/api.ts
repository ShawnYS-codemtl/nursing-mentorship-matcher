import type { Match, Stats, UnmatchedResponse, OverrideMatchRequest, ScoreBreakdown } from "../types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

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

export const uploadCsvFiles = async (formData: FormData) => {
  const res = await fetch(`${BASE_URL}/import/preview`, {
        method: "POST",
        body: formData,
    });
    if (!res.ok) throw new Error("CSV Upload failed");
    return res.json()
}

export const confirmImport = async (formData: FormData) => {
  const res = await fetch(
    `${BASE_URL}/import/confirm`, {
      method: "POST",
      body: formData,
    });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(JSON.stringify(data, null, 2));
  }

  return data;
};

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

export const overrideMatch = async (
  body: OverrideMatchRequest
): Promise<void> => {
  const res = await fetch(`${BASE_URL}/matches/override`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || "Override match failed");
  }
};

export async function toggleMatchLock(id: number, is_locked: boolean) {
  const res = await fetch(`${BASE_URL}/matches/${id}/lock`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_locked }),
  });

  if (!res.ok) {
    throw new Error("Failed to toggle match lock");
  }

  return res.json();
}

export const resetDatabase = async (): Promise<void> => {
  const res = await fetch(`${BASE_URL}/reset-db`, { method: "POST" });
  if (!res.ok) throw new Error("Reset failed");
};

export async function getMatchScore(payload: {
  mentor_id: number;
  mentee_id: number;
}): Promise<{
  score: number;
  breakdown: ScoreBreakdown;
}>  {
  const res = await fetch(`${BASE_URL}/match-score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error("Failed to fetch score");

  return res.json();
}