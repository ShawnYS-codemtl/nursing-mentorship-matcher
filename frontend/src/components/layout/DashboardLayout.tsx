import React from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import type { Page } from "../../App";

interface Props {
  children: React.ReactNode;
  activePage: Page;
  onNavigate: (page: Page) => void;
}

const DashboardLayout: React.FC<Props> = ({ children, activePage, onNavigate }) => {
  return (
    <div className="dashboard-layout flex min-h-screen bg-gray-50">
      <Sidebar activePage={activePage} onNavigate={onNavigate} />
      <div className="main-content flex-1 flex flex-col">
        <Header />
        <main className="p-6 flex-1">{children}</main>
      </div>
    </div>
  );
};

export default DashboardLayout;
