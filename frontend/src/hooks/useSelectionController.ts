import { useState } from "react";
import type { DetailedMentee, AvailableMentor } from "../types";

type SidePanelMode = "none" | "mentee-picker" | "mentor-picker";

export function useSelectionController() {
  const [selectedMentee, setSelectedMentee] = useState<DetailedMentee | null>(null);
  const [selectedMentor, setSelectedMentor] = useState<AvailableMentor | null>(null);
  const [sidePanelMode, setSidePanelMode] = useState<SidePanelMode>("none");

  // --- OPENERS ---
  const openMenteePicker = () => setSidePanelMode("mentee-picker");
  const openMentorPicker = () => setSidePanelMode("mentor-picker");
  const closeSidePanel = () => setSidePanelMode("none");

  // --- SELECTION ---
  const selectMentee = (mentee: DetailedMentee) => {
    setSelectedMentee(mentee);
    // closeSidePanel();
  };

  const selectMentor = (mentor: AvailableMentor) => {
    setSelectedMentor(mentor);
    // closeSidePanel();
  };

  // --- RESET ---
  const resetSelection = () => {
    setSelectedMentee(null);
    setSelectedMentor(null);
    closeSidePanel();
  };

  return {
    selectedMentee,
    selectedMentor,
    sidePanelMode,

    openMenteePicker,
    openMentorPicker,
    closeSidePanel,

    selectMentee,
    selectMentor,

    resetSelection,
  };
}