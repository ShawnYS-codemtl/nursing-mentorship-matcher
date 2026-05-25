import { useState } from "react";
import DashboardPage from "./pages/DashboardPage";
import UserGuidePage from "./pages/UserGuidePage";

export type Page = "dashboard" | "guide";

function App() {
  const [activePage, setActivePage] = useState<Page>("dashboard");

  return activePage === "dashboard"
    ? <DashboardPage onNavigate={setActivePage} />
    : <UserGuidePage onNavigate={setActivePage} />;
}

export default App;
