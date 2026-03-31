import React from "react";
import DashboardLayout from "../components/layout/DashboardLayout";
import StatsPanel from "../components/dashboard/StatsPanel";
import MatchesTable from "../components/dashboard/MatchesTable";
import UnmatchedPanel from "../components/dashboard/UnmatchedPanel";
import ControlPanel from "../components/controls/ControlPanel";

const DashboardPage: React.FC = () => {
  return (
    <DashboardLayout>
      {/* Metrics summary */}
      <StatsPanel />

      {/* Matches table */}
      <MatchesTable />

      {/* Unmatched section */}
      <UnmatchedPanel />

      {/* Control panel with buttons */}
      <ControlPanel />
    </DashboardLayout>
  );
};

export default DashboardPage;