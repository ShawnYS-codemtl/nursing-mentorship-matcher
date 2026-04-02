export interface Mentor {
  id: number;
  name: string;
}

export interface Mentee {
  id: number;
  name: string;
}

export interface Person {
  id: number;
  name: string;
  email: string;
}

export interface MatchReason {
  // flags
  explicit_choice?: boolean;
  constraints_violated?: boolean;

  // scoring components
  identity_extracurricular?: number;
  program_alignment?: number;
  specialty_alignment?: number;
  specialty_mismatch?: number;

  // explanations
  reasons?: string[];

  // allow future backend fields without breaking
  [key: string]: string | number | boolean | string[] | undefined;
}

export interface Match {
  id: number;
  created_at: string;

  mentor: Person;
  mentee: Person;

  score: number;

  match_type: string;
  match_reason: MatchReason;

  is_locked: boolean;
  is_manual_override: boolean;
}

export interface Stats {
  totalMentors: number;
  totalMentees: number;
  totalMatches: number;
}