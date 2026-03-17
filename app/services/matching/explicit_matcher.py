class ExplicitMatcher:
    def __init__(self, mentors, mentees):
        self.mentors = mentors
        self.mentees = mentees

        self.mentor_lookup = {m.id: m for m in mentors}
        self.mentee_lookup = {m.id: m for m in mentees}

        self.mentor_capacity = {
            m.id: getattr(m, "max_mentees", 1) for m in mentors
        }

        self.matched_mentees = set()
        self.matches = []

    # ---------- Public API ----------

    def run(self):
        self._match_mutual()
        self._match_mentor_driven()
        self._match_mentee_driven()

        return self.matches, self._get_remaining()

    # ---------- Phase 1: Mutual ----------

    def _match_mutual(self):
        for mentor in self.mentors:
            if self._is_full(mentor):
                continue

            for mentee_id in mentor.preferred_mentees or []:
                mentee = self.mentee_lookup.get(mentee_id)

                if not self._valid_pair(mentor, mentee):
                    continue

                if mentee.preferred_mentor_id == mentor.id:
                    self._assign(mentor, mentee)

                    if self._is_full(mentor):
                        break

    # ---------- Phase 2: Mentor-driven ----------

    def _match_mentor_driven(self):
        for mentor in self.mentors:
            if self._is_full(mentor):
                continue

            for mentee_id in mentor.preferred_mentees or []:
                mentee = self.mentee_lookup.get(mentee_id)

                if not self._valid_pair(mentor, mentee):
                    continue

                self._assign(mentor, mentee)

                if self._is_full(mentor):
                    break

    # ---------- Phase 3: Mentee-driven ----------

    def _match_mentee_driven(self):
        for mentee in self.mentees:
            if mentee.id in self.matched_mentees:
                continue

            mentor_id = mentee.preferred_mentor_id
            if not mentor_id:
                continue

            mentor = self.mentor_lookup.get(mentor_id)
            if not mentor or self._is_full(mentor):
                continue

            self._assign(mentor, mentee)

    # ---------- Core helpers ----------

    def _assign(self, mentor, mentee):
        self.matches.append((mentor, mentee))
        self.matched_mentees.add(mentee.id)
        self.mentor_capacity[mentor.id] -= 1

    def _is_full(self, mentor):
        return self.mentor_capacity.get(mentor.id, 0) <= 0

    def _valid_pair(self, mentor, mentee):
        if not mentee:
            return False
        if mentee.id in self.matched_mentees:
            return False
        return True

    def _get_remaining(self):
        remaining_mentors = [
            m for m in self.mentors if not self._is_full(m)
        ]

        remaining_mentees = [
            m for m in self.mentees if m.id not in self.matched_mentees
        ]

        return remaining_mentors, remaining_mentees