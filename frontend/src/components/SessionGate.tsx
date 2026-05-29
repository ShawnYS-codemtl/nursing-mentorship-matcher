import { useState } from "react";
import { setSessionCode } from "../services/api";

interface SessionGateProps {
  onJoin: (code: string) => void;
}

function generateCode(): string {
  const adjectives = ["blue", "swift", "calm", "bold", "kind", "bright", "clear", "warm"];
  const nouns = ["river", "maple", "cedar", "stone", "crane", "ember", "tide", "peak"];
  const adj = adjectives[Math.floor(Math.random() * adjectives.length)];
  const noun = nouns[Math.floor(Math.random() * nouns.length)];
  const num = Math.floor(100 + Math.random() * 900);
  return `${adj}-${noun}-${num}`;
}

export default function SessionGate({ onJoin }: SessionGateProps) {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  function handleJoin() {
    const trimmed = code.trim().toLowerCase();
    if (!trimmed) {
      setError("Please enter or generate a workspace code.");
      return;
    }
    if (!/^[a-z0-9][a-z0-9\-]{1,}$/.test(trimmed)) {
      setError("Code must be lowercase letters, numbers, and hyphens only.");
      return;
    }
    setSessionCode(trimmed);
    onJoin(trimmed);
  }

  function handleGenerate() {
    setCode(generateCode());
    setError("");
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") handleJoin();
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 w-full max-w-md p-10">
        {/* Header */}
        <div className="mb-8">
          <div className="border-l-4 border-blue-600 pl-4 mb-2">
            <h1 className="text-2xl font-bold text-gray-900 leading-tight">Mentorship Dashboard</h1>
            <p className="text-sm text-gray-500 mt-0.5">McGill Nursing — Mentorship Matching</p>
          </div>
        </div>

        {/* Body */}
        <p className="text-sm text-gray-600 mb-6">
          Enter a <strong>workspace code</strong> to access your session, or generate a new one to
          start fresh. Share the code with teammates to collaborate on the same dataset.
        </p>

        <div className="space-y-3">
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide">
            Workspace Code
          </label>

          <div className="flex gap-2">
            <input
              type="text"
              value={code}
              onChange={(e) => { setCode(e.target.value); setError(""); }}
              onKeyDown={handleKeyDown}
              placeholder="e.g. mcgill-fall-2025"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleGenerate}
              className="text-sm px-3 py-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-50 transition-colors whitespace-nowrap"
            >
              Generate
            </button>
          </div>

          {error && <p className="text-xs text-red-500">{error}</p>}

          <button
            onClick={handleJoin}
            className="w-full bg-blue-600 text-white rounded-lg py-2.5 text-sm font-semibold hover:bg-blue-700 transition-colors"
          >
            Join / Create Workspace
          </button>
        </div>
      </div>
    </div>
  );
}
