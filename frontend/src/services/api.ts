import type { Match, Stats, UnmatchedResponse, OverrideMatchRequest, ScoreBreakdown } from "../types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

// ─── Session management ──────────────────────────────────────────────────────

const SESSION_KEY = "nursingMatcherSession";

export const getSessionCode = (): string | null => localStorage.getItem(SESSION_KEY);
export const setSessionCode = (code: string): void => localStorage.setItem(SESSION_KEY, code);
export const clearSessionCode = (): void => localStorage.removeItem(SESSION_KEY);

const sessionHeader = (): Record<string, string> => {
  const code = getSessionCode();
  return code ? { "X-Session-ID": code } : {};
};

// ─── API calls ───────────────────────────────────────────────────────────────

export const fetchMatches = async (): Promise<Match[]> => {
  const res = await fetch(`${BASE_URL}/matches`, { headers: sessionHeader() });
  if (!res.ok) throw new Error("Failed to fetch matches");
  return res.json();
};

export const fetchStats = async (): Promise<Stats> => {
  const res = await fetch(`${BASE_URL}/stats`, { headers: sessionHeader() });
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
};

export const fetchUnmatched = async (): Promise<UnmatchedResponse> => {
  const res = await fetch(`${BASE_URL}/unmatched`, { headers: sessionHeader() });
  if (!res.ok) throw new Error("Failed to fetch unmatched mentees");
  return res.json();
};

export const uploadCsvFiles = async (formData: FormData) => {
  const res = await fetch(`${BASE_URL}/import/preview`, {
    method: "POST",
    headers: sessionHeader(),
    body: formData,
  });
  if (!res.ok) throw new Error("CSV Upload failed");
  return res.json();
};

export const confirmImport = async (formData: FormData) => {
  const res = await fetch(`${BASE_URL}/import/confirm`, {
    method: "POST",
    headers: sessionHeader(),
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
    headers: sessionHeader(),
  });

  if (!res.ok) throw new Error("Matching failed");
  return res.json();
};

export const exportData = async (): Promise<void> => {
  const res = await fetch(`${BASE_URL}/export`, { headers: sessionHeader() });

  if (!res.ok) throw new Error("Export failed");

  const blob = await res.blob();

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "matches.csv";
  document.body.appendChild(a);
  a.click();

  a.remove();
  window.URL.revokeObjectURL(url);
};

export const unmatch = async (matchId: number): Promise<void> => {
  const res = await fetch(`${BASE_URL}/matches/${matchId}`, {
    method: "DELETE",
    headers: sessionHeader(),
  });

  if (!res.ok) throw new Error("Failed to unmatch");
};

export const overrideMatch = async (body: OverrideMatchRequest): Promise<void> => {
  const res = await fetch(`${BASE_URL}/matches/override`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...sessionHeader(),
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
    headers: {
      "Content-Type": "application/json",
      ...sessionHeader(),
    },
    body: JSON.stringify({ is_locked }),
  });

  if (!res.ok) {
    throw new Error("Failed to toggle match lock");
  }

  return res.json();
}

export const resetDatabase = async (): Promise<void> => {
  const res = await fetch(`${BASE_URL}/reset-db`, {
    method: "POST",
    headers: sessionHeader(),
  });
  if (!res.ok) throw new Error("Reset failed");
};

export async function getMatchScore(payload: {
  mentor_id: number;
  mentee_id: number;
}): Promise<{
  score: number;
  breakdown: ScoreBreakdown;
}> {
  const res = await fetch(`${BASE_URL}/match-score`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...sessionHeader(),
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error("Failed to fetch score");

  return res.json();
}
