import React, {useState} from "react";
import { useUnmatched } from "../../hooks/useUnmatched";
import { useSelectionController } from "../../hooks/useSelectionController";
import { overrideMatch } from "../../services/api";
import { useMatchScore } from "../../hooks/useMatchScore";

interface Props {
  refreshKey: number;
  onRefresh: () => void;
}

const UnmatchedPanel: React.FC<Props> = ({refreshKey, onRefresh}) => {
  const { mentees, mentors, loading, error } = useUnmatched(refreshKey);
  const [collapsed, setCollapsed] = useState(false);
  const {
    selectedMentee,
    selectedMentor,
    sidePanelMode,
    openMenteePicker,
    openMentorPicker,
    closeSidePanel,
    selectMentee,
    selectMentor,
    resetSelection,
  } = useSelectionController();
  const { score, breakdown, loading: scoreLoading } = useMatchScore(selectedMentee, selectedMentor);

  const handleAssign = async () => {
    if (!selectedMentee || !selectedMentor) return;

    try {
      await overrideMatch({
        mentor_id: selectedMentor.id,
        mentee_id: selectedMentee.id,
      });

      // ✅ Clear selections AFTER success
      resetSelection();

      onRefresh(); // 🔑 refresh all panels
    } catch (err) {
      console.error(err);
      alert("Failed to assign match");
    }
  };

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
        {selectedMentee && selectedMentor && <p><strong>Score:</strong> {score}</p>}
        <div className="grid grid-cols-3 gap-4 mb-4">
          {/* Mentee panel */}
          <div className="bg-white p-4 shadow rounded min-h-[150px] bg-blue-100"
               onClick={openMenteePicker}
          >
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
          <div className="bg-white p-4 shadow rounded min-h-[150px] bg-green-100"
          onClick={openMentorPicker}>
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
          <div className="bg-white p-4 shadow rounded min-h-[150px]">
            {sidePanelMode === "none" && (
              <p className="text-gray-400">Click a panel to browse options</p>
            )}
            {sidePanelMode === "mentee-picker" && (
            <>
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-bold">Select Mentee</h3>
                <button
                  onClick={closeSidePanel}
                  className="text-sm text-red-500"
                >
                  Close
                </button>
              </div>

              {mentees.map((m) => (
                <div
                  key={m.id}
                  onClick={() => {
                    selectMentee(m);
                    // setSidePanelMode("none");
                  }}
                  className={`p-2 rounded cursor-pointer ${
                  selectedMentee?.id === m.id ? "bg-blue-100" : "hover:bg-gray-100"}`}
                >
                  {m.name} ({m.program})
                </div>
              ))}
            </>
            )}
            {sidePanelMode === "mentor-picker" && (
            <>
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-bold">Select Mentor</h3>
                <button
                  onClick={closeSidePanel}
                  className="text-sm text-red-500"
                >
                  Close
                </button>
              </div>

              {mentors.map((m) => (
                <div
                  key={m.id}
                  onClick={() => {
                    selectMentor(m);
                    // setSidePanelMode("none");
                  }}
                  className={`p-2 rounded cursor-pointer ${
                  selectedMentor?.id === m.id ? "bg-blue-100" : "hover:bg-gray-100"}`}
                >
                  {m.name} ({m.program}) - Capacity: {m.remaining_capacity}
                </div>
              ))}
            </>
            )}
          </div>

        </div>
        {selectedMentee && selectedMentor && (
          <div className="my-2 p-2 bg-yellow-100 rounded">
            {scoreLoading ? (
              <p>Calculating score...</p>
            ) : (
              <>
                <p><strong>Score:</strong> {score}</p>

                {breakdown && (
                  <ul className="text-sm">
                    {Object.entries(breakdown).map(([k, v]) => (
                      <li key={k}>{k}: {String(v)}</li>
                    ))}
                  </ul>
                )}
              </>
            )}
          </div>
        )}

        <button
            disabled={!selectedMentee || !selectedMentor}
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={handleAssign}
          >
            Match Selected Pair
        </button>

        <div>
          <h2 className="text-lg font-bold mt-4 mb-2">Available Mentees</h2>
          {mentees.map((m) => (
            <div
              key={m.id}
              onClick={() => selectMentee(m)}
              className={`cursor-pointer p-2 rounded ${
                selectedMentee?.id === m.id ? "bg-blue-100" : "hover:bg-gray-100"
              }`}
            >
              {m.name} ({m.program}) - Year: {m.year_in_program}
            </div>
          ))}

          <h2 className="text-lg font-bold mt-4 mb-2">Available Mentors</h2>

          {mentors.map((m) => (
            <div
              key={m.id}
              onClick={() => selectMentor(m)}
              className={`cursor-pointer p-2 rounded ${
                selectedMentor?.id === m.id ? "bg-green-100" : "hover:bg-gray-100"
              }`}
            >
              {m.name} ({m.program}) - Year: {m.year_in_program}
            </div>
          ))}
        </div>
      </>
      }
      
    </section>
  );
};

export default UnmatchedPanel;