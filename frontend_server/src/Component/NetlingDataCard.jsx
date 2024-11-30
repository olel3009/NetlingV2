import 'react-flow-renderer/dist/style.css';
import 'react-flow-renderer/dist/theme-default.css';
import ReactFlow from 'react-flow-renderer';
import 'react-flow-renderer/dist/style.css';
import React from 'react';


const NetlingDataCard = ({ data }) => {
    //data = {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel, "brain": self.brain.collect()}
    const { x, y, r, width, height, id, type, foodlevel, brain} = data; // Extrahiere x und y aus den Daten
    return (
        <div>
            <p>Position: {x}, {y}</p>
            <p>Rotation: {r}</p>

        </div>
    );
}
export default NetlingDataCard;
