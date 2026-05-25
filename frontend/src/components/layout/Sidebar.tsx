import React from "react";
import type { Page } from "../../App";

interface SidebarProps {
  activePage: Page;
  onNavigate: (page: Page) => void;
}

const NAV_ITEMS: { label: string; page: Page }[] = [
  { label: "Dashboard", page: "dashboard" },
  { label: "User Guide", page: "guide" },
];

const Sidebar: React.FC<SidebarProps> = ({ activePage, onNavigate }) => {
  return (
    <aside className="w-40 bg-white border-r border-gray-200 flex flex-col pt-6 px-3">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2 mb-3">Navigation</p>
      <ul className="flex flex-col gap-1">
        {NAV_ITEMS.map(({ label, page }) => (
          <li key={page}>
            <button
              onClick={() => onNavigate(page)}
              className={`w-full text-left flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                activePage === page
                  ? "text-gray-900 bg-blue-50 border border-blue-100"
                  : "text-gray-500 hover:bg-gray-100 border border-transparent"
              }`}
            >
              {label}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
