import React, { useState } from "react";
import DashboardLayout from "../components/layout/DashboardLayout";
import StatsPanel from "../components/dashboard/StatsPanel";
import MatchesTable from "../components/dashboard/MatchesTable";
import UnmatchedPanel from "../components/dashboard/UnmatchedPanel";
import ControlPanel from "../components/controls/ControlPanel";
import type { Page } from "../App";

interface Props {
  onNavigate: (page: Page) => void;
}

const DashboardPage: React.FC<Props> = ({ onNavigate }) => {
  const [refreshKey, setRefreshKey] = useState(0);

  const refresh = () => setRefreshKey((prev) => prev + 1);

  return (
    <DashboardLayout activePage="dashboard" onNavigate={onNavigate}>
      {/* Metrics summary */}
      <StatsPanel refreshKey={refreshKey} />

      {/* Matches table */}
      <MatchesTable refreshKey={refreshKey} onRefresh={refresh} />

      {/* Unmatched section */}
      <UnmatchedPanel refreshKey={refreshKey} onRefresh={refresh}/>

      {/* Control panel with buttons */}
      <ControlPanel onRefresh={refresh}/>
    </DashboardLayout>
  );
};

export default DashboardPage;
