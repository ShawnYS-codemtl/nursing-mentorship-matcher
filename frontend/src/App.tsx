import { useState } from "react";
import DashboardPage from "./pages/DashboardPage";
import UserGuidePage from "./pages/UserGuidePage";
import SessionGate from "./components/SessionGate";
import { getSessionCode, setSessionCode } from "./services/api";

export type Page = "dashboard" | "guide";

function App() {
  const [sessionCode, setSessionCodeState] = useState<string | null>(getSessionCode());
  const [activePage, setActivePage] = useState<Page>("dashboard");

  if (!sessionCode) {
    return (
      <SessionGate
        onJoin={(code) => {
          setSessionCode(code);
          setSessionCodeState(code);
        }}
      />
    );
  }

  return activePage === "dashboard"
    ? <DashboardPage onNavigate={setActivePage} />
    : <UserGuidePage onNavigate={setActivePage} />;
}

export default App;
