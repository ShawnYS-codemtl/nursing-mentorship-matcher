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