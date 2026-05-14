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
  year: number;
  program: string;
}

export interface DetailedMentee {
  id: number;
  name: string;
  email: string;
  program: string;
  year_in_program: number;
  specialties: string[];
  languages_needed: string[];
  race_ethnicity: string;
  lgbtq_status: string;
  extracurricular_interests: string[];
}


export interface AvailableMentor {
  id: number;
  name: string;
  email: string;

  capacity: number;
  current_matches: number;
  remaining_capacity: number;

  program: string;
  year_in_program: number;
  specialties: string[];
  languages: string[];
  race_ethnicity: string;
  lgbtq_status: string;
  extracurricular_interests: string[];
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
    mentors: number;
    mentees: number;
    matches: number;
    unmatched_mentees: number;
    available_mentors: number;
    avg_score: number;
    min_score: number;
    max_score: number;
    median_score: number;
}

export interface UnmatchedResponse {
  unmatched_mentees: DetailedMentee[];
  available_mentors: AvailableMentor[];
}

export type ImportSource = "csv" | "google_sheets";

export interface ImportRequest {
  source: ImportSource;
}

export interface OverrideMatchRequest {
  mentor_id: number;
  mentee_id: number;
}

export type ScoreBreakdown = {
  explicit_choice: boolean;
  constraints_violated: boolean;
  reasons: string[];

  program_alignment: number;
  specialty_alignment: number;
  identity_extracurricular: number;
  specialty_mismatch: number;

  [key: string]: number | boolean | string[];
};

export type SortDirection = "asc" | "desc";

export type MatchSortKey =
  | "id"
  | "mentor_name"
  | "mentee_name"
  | "score"
  | "match_type"
  | "is_locked";

export type ColumnMapping = Record<string, string>;

export interface MappingPreview {
  headers: string[];
  mapping: ColumnMapping;
  unmatched: string[];
}

export interface ImportPreviewResponse {
  mentor: MappingPreview;
  mentee: MappingPreview;
}