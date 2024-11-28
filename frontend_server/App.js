import React from 'react';
import NeatVisualizer from './Component/NeatVisualizer';
import ReactFlow from 'react-flow-renderer';
import 'react-flow-renderer/dist/style.css';
import WebSocketProdComponent from "./Component/WebSocketProdComponent";
import ScrollComponent from "./Component/ScrollComponent";
import BiomeVisualizer from "./Component/BiomeVisulizer";
import "./App.css";

const App = () => (
    <div>
        <div className={"element1"}>

        </div>
        <div className={"element1"}>
            <ScrollComponent>
                <WebSocketProdComponent/>
            </ScrollComponent>
        </div>
    </div>
);


export default App;
