import React from 'react';
import ReactFlow, { Background, Controls } from 'react-flow-renderer';
import 'react-flow-renderer/dist/style.css';

const CustomNode = ({ data }) => {
    return (
        <div style={{
            backgroundColor: '#4caf50',
            border: '2px solid #388e3c',
            borderRadius: '50%', // Runde Knoten
            width: '60px',
            height: '60px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            color: '#fff',
        }}>
            <strong>{data.label}</strong>
        </div>
    );
};

const NeatVisualizer = ({ networkData }) => {
    const nodeTypes = { customNode: CustomNode };

    // Nodes erstellen
    const nodes = networkData.nodes.map((node, index) => ({
        id: node.id, // ID bleibt als String
        data: {
            label: `Node ${node.id}`,
        },
        position: { x: 200 * index, y: 100 }, // Positionierung in einer Linie
        type: 'customNode',
    }));

    // Edges erstellen
    const edges = networkData.connections
        .filter((conn) => conn.enabled) // Nur aktive Verbindungen
        .map((conn) => ({
            id: `e${conn.input}-${conn.output}`,
            source: conn.input, // Verwendet dieselbe ID wie die Nodes
            target: conn.output, // Verwendet dieselbe ID wie die Nodes
            animated: true, // Animierte Verbindungen
            style: { stroke: '#ff5722', strokeWidth: 2 },
        }));

    return (
        <div style={{ height: '600px', width: '100%', border: '1px solid black' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
                fitView
            >
                <Background color="#aaa" gap={16} />
                <Controls />
            </ReactFlow>
        </div>
    );
};

export default NeatVisualizer;
