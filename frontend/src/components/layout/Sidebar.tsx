import React from "react";

const Sidebar: React.FC = () => {
  return (
    <aside className="w-40 bg-white border-r border-gray-200 flex flex-col pt-6 px-3">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2 mb-3">Navigation</p>
      <ul className="flex flex-col gap-1">
        <li>
          <a className="flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium text-gray-900 bg-blue-50 border border-blue-100">
            Dashboard
          </a>
        </li>
        <li>
          <a className="flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:bg-gray-100 cursor-pointer">
            Settings
          </a>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
