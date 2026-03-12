import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'ダッシュボード' },
    { path: '/sensors', label: 'IoTセンサー' },
    { path: '/environment', label: '環境データ' },
    { path: '/traffic', label: '交通データ' },
    { path: '/energy', label: 'エネルギーデータ' },
    { path: '/esg', label: 'ESGレポート' },
    { path: '/alerts', label: 'アラート' },
    { path: '/decision-support', label: '判断支援' },
  ];

  return (
    <div className="layout">
      <header className="header">
        <h1>スマートシティ×サステナビリティ統合プラットフォーム</h1>
      </header>
      <nav className="sidebar">
        <ul>
          {menuItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={location.pathname === item.path ? 'active' : ''}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default Layout;

