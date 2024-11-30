// index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App'; // Die Haupt-App-Komponente
import './index.css';
import Sandbox from './Sandbox'; // Die Sandbox-Komponente
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <Router>
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="/sandbox" element={<Sandbox />} />
            </Routes>
        </Router>
    </React.StrictMode>
);
