import React, {useState} from "react";
import { useUnmatched } from "../../hooks/useUnmatched";
import type { DetailedMentee, AvailableMentor } from "../../types";

const UnmatchedPanel: React.FC = () => {
  const { mentees, mentors, loading, error } = useUnmatched();
  const [collapsed, setCollapsed] = useState(false);
  const [selectedMentee, setSelectedMentee] = useState<DetailedMentee | null>(null);
  const [selectedMentor, setSelectedMentor] = useState<AvailableMentor | null>(null);

  if (loading) return <p>Loading unmatched mentees...</p>;
  if (error) return <p>Error loading unmatched mentees</p>;

  return (
    <section className="unmatched-panel mb-4">
      <div className="flex items-center mb-2">
        <button
          onClick={() => setCollapsed((prev) => !prev)}
          className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
          {collapsed ? "▶" : "▼"}
        </button>
        <h2 className="text-lg font-bold mx-2">Unmatched Mentees</h2>
      </div>


      {!collapsed && 
      <>
        <div className="grid grid-cols-3 gap-4 mb-4">
          {/* Mentee panel */}
          <div className="bg-white p-4 shadow rounded min-h-[150px] bg-blue-100">
            <h3 className="font-bold mb-2">Selected Mentee</h3>

            {selectedMentee ? (
              <>
                <p><strong>{selectedMentee.name}</strong></p>
                <p>{selectedMentee.email}</p>
                <p>Program: {selectedMentee.program}</p>
                <p>Year: {selectedMentee.year_in_program}</p>
                <p>Specialties: {selectedMentee.specialties.join(", ")}</p>
                <p>Interests: {selectedMentee.extracurricular_interests.join(", ")}</p>
                <p>Languages: {selectedMentee.languages_needed.join(", ")}</p>
                <p>LGBTQ: {selectedMentee.lgbtq_status}</p>
                <p>Ethnicity: {selectedMentee.race_ethnicity}</p>
              </>
            ) : (
              <p className="text-gray-400">Select a mentee</p>
            )}
          </div>

          {/* Mentor panel */}
          <div className="bg-white p-4 shadow rounded min-h-[150px] bg-green-100">
            <h3 className="font-bold mb-2">Selected Mentor</h3>

            {selectedMentor ? (
              <>
                <p><strong>{selectedMentor.name}</strong></p>
                <p>{selectedMentor.email}</p>
                <p>Program: {selectedMentor.program}</p>
                <p>Year: {selectedMentor.year_in_program}</p>
                <p>Specialties: {selectedMentor.specialties.join(", ")}</p>
                <p>Interests: {selectedMentor.extracurricular_interests.join(", ")}</p>
                <p>Languages: {selectedMentor.languages.join(", ")}</p>
                <p>LGBTQ: {selectedMentor.lgbtq_status}</p>
                <p>Ethnicity: {selectedMentor.race_ethnicity}</p>
                <p>Capacity: {selectedMentor.remaining_capacity}</p>
              </>
            ) : (
              <p className="text-gray-400">Select a mentor</p>
            )}
          </div>
        </div>

        <button
            disabled={!selectedMentee || !selectedMentor}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Match Selected Pair
        </button>

        <div>
          <h2 className="text-lg font-bold mt-4 mb-2">Available Mentees</h2>
          {mentees.map((m) => (
            <div
              key={m.id}
              onClick={() => setSelectedMentee(m)}
              className={`cursor-pointer p-2 rounded ${
                selectedMentee?.id === m.id ? "bg-blue-100" : "hover:bg-gray-100"
              }`}
            >
              {m.name} ({m.program})
            </div>
          ))}

          <h2 className="text-lg font-bold mt-4 mb-2">Available Mentors</h2>

          {mentors.map((m) => (
            <div
              key={m.id}
              onClick={() => setSelectedMentor(m)}
              className={`cursor-pointer p-2 rounded ${
                selectedMentor?.id === m.id ? "bg-green-100" : "hover:bg-gray-100"
              }`}
            >
              {m.name} - Remaining: {m.remaining_capacity}
            </div>
          ))}
        </div>
      </>
      }
      
    </section>
  );
};

export default UnmatchedPanel;