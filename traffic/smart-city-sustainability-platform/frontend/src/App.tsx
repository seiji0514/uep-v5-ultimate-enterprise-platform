import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Sensors from './pages/Sensors';
import Environment from './pages/Environment';
import Traffic from './pages/Traffic';
import Energy from './pages/Energy';
import ESG from './pages/ESG';
import Alerts from './pages/Alerts';
import DecisionSupport from './pages/DecisionSupport';
import Layout from './components/Layout';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sensors" element={<Sensors />} />
          <Route path="/environment" element={<Environment />} />
          <Route path="/traffic" element={<Traffic />} />
          <Route path="/energy" element={<Energy />} />
          <Route path="/esg" element={<ESG />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/decision-support" element={<DecisionSupport />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

