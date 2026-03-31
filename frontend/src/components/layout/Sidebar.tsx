import React from "react";

const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-gray-100 p-4">
      <h2 className="font-bold mb-4">Dashboard</h2>
      <ul>
        <li>Dashboard</li>
        <li>Settings</li>
      </ul>
    </aside>
  );
};

export default Sidebar;