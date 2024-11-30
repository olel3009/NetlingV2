// src/Sandbox.jsx
import React from 'react';
import LeaderBoard from "./Component/LeaderCard";
import 'bootstrap/dist/css/bootstrap.min.css';
const entities = [
    { name: 'Entity 1', foodLevel: 75 },
    { name: 'Entity 2', foodLevel: 50 },
    { name: 'Entity 3', foodLevel: 90 },
    { name: 'Entity 4', foodLevel: 65 },
];
const Sandbox = () => {
    return (
        <div style={{ padding: "20px"}} className="container-sm">
            <LeaderBoard entities={entities} />
        </div>
    );
};

export default Sandbox;
