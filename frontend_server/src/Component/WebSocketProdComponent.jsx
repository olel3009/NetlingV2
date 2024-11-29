import React, { useEffect, useRef, useState } from "react";
import Netling from "../Entitys/Netling";
import Food from "../Entitys/Food";
import NetlingDataCard from "./NetlingDataCard";
import "../App.css";
import "./BiomeVisualizer.css";

const BiomeWebSocketVisualizer = () => {
    const [biomeMap, setBiomeMap] = useState([]); // Biome-Karte (2D-Array)
    const [biomeClasses, setBiomeClasses] = useState({}); // Klasse-zu-Name-Mapping
    const [entities, setEntities] = useState([]); // Alle Entitäten
    const [selectedEntity, setSelectedEntity] = useState(null); // Ausgewählte Entität
    const [entityData, setEntityData] = useState(null); // Daten der ausgewählten Entität
    const [error, setError] = useState(null);
    const canvasRef = useRef(null); // Referenz auf das Canvas-Element
    const [values, setValues] = useState([500, 500]); // Größe des Bereichs
    const [selectedEntityClick, setSelectedEntityClick] = useState(null); // ID der geklickten Entität
    const [isFollowing, setIsFollowing] = useState(false); // Status, ob gerade gefolgt wird

    // Daten laden
    useEffect(() => {
        const fetchBiomeData = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/getBiome");
                if (!response.ok) {
                    throw new Error(`HTTP-Fehler! Status: ${response.status}`);
                }
                const data = await response.json();

                setBiomeMap(data.map || []); // Speichert die Karte
                const classesMapping = {};
                data.classes.forEach((cls) => {
                    classesMapping[cls.id] = cls.name; // ID zu Name Mapping
                });
                setBiomeClasses(classesMapping); // Speichert die Biome-Klassen
            } catch (err) {
                setError(err.message);
            }
        };

        fetchBiomeData();
    }, []);

    // WebSocket Verbindung
    useEffect(() => {
        const socket = new WebSocket("ws://127.0.0.1:8000/ws/");

        socket.onopen = () => {
            console.log("WebSocket verbunden!");
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                setEntities(data);
            } catch (error) {
                console.error("Fehler beim Parsen der Nachricht:", error);
            }
        };

        socket.onerror = (error) => {
            console.error("WebSocket Fehler: ", error);
        };

        socket.onclose = () => {
            console.warn("WebSocket-Verbindung geschlossen. Versuche erneut zu verbinden...");
            setTimeout(() => {
                socket = new WebSocket("ws://127.0.0.1:8000/ws/");
            }, 1000);
        };

        return () => {
            socket.close();
        };
    }, []);

    // Canvas zeichnen, wenn die Biome-Daten geladen sind
    useEffect(() => {
        if (biomeMap.length && canvasRef.current) {
            const canvas = canvasRef.current;
            const ctx = canvas.getContext("2d");

            // Canvas entsprechend der Originalgröße skalieren
            const canvasWidth = values[0];
            const canvasHeight = values[1];

            canvas.width = canvasWidth * 2; // Verdoppele die Breite des Canvas
            canvas.height = canvasHeight * 2; // Verdoppele die Höhe des Canvas
            ctx.scale(2, 2); // Skaliere den Canvas-Inhalt entsprechend

            const cellSizeX = values[0] / biomeMap[0].length; // Größe einer Zelle in x-Richtung
            const cellSizeY = values[1] / biomeMap.length; // Größe einer Zelle in y-Richtung

            // Raster zeichnen
            biomeMap.forEach((row, y) => {
                row.forEach((cell, x) => {
                    ctx.fillStyle = getBiomeColor(biomeClasses[cell]); // Farbe der Zelle
                    ctx.fillRect(x * cellSizeX, y * cellSizeY, cellSizeX, cellSizeY); // Rechteck zeichnen
                });
            });
        }
    }, [biomeMap, biomeClasses, values]);

    const fetchEntityData = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/getObject/${id}`);
            if (!response.ok) {
                throw new Error(`Fehler: ${response.statusText}`);
            }
            const data = await response.json();
            setEntityData(data);
        } catch (error) {
            console.error("Fehler beim Abrufen der Entitätsdaten:", error);
        }
    };

    const handleEntityClick = (entity) => {
        setSelectedEntityClick(entity.id);
        setSelectedEntity(entity);
        setIsFollowing(true); // AutoFollow aktivieren
        if (entity.type === "Agent") {
            fetchEntityData(entity.id);
        } else {
            setEntityData(null);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key !== null) {
            setSelectedEntityClick(null);
            setIsFollowing(false); // AutoFollow stoppen
        }
    };

    useEffect(() => {
        window.addEventListener("keydown", handleKeyDown);
        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, []);

    // Kontinuierliche AutoFollow-Funktion
    useEffect(() => {
        const interval = setInterval(() => {
            if (isFollowing && selectedEntityClick) {
                const entity = entities.find((e) => e.id === selectedEntityClick);
                if (entity) {
                    const targetX = Math.max(entity.x - window.innerWidth / 2, 0);
                    const targetY = Math.max(entity.y - window.innerHeight / 2, 0);

                    const currentScrollX = window.scrollX;
                    const currentScrollY = window.scrollY;

                    // Nur scrollen, wenn die Änderung signifikant ist
                    if (
                        Math.abs(currentScrollX - targetX) > 10 ||
                        Math.abs(currentScrollY - targetY) > 10
                    ) {
                        window.scrollTo({
                            left: targetX,
                            top: targetY,
                        });
                    }
                }
            }
        }, 100); // Überprüft alle 100ms die Position

        return () => clearInterval(interval);
    }, [isFollowing, selectedEntityClick, entities]);

    // Fehler anzeigen
    if (error) {
        return <div>Fehler beim Laden der Biome: {error}</div>;
    }

    // Noch keine Daten verfügbar
    if (!biomeMap.length) {
        return <div>Biomedaten werden geladen...</div>;
    }

    return (
        <div style={{ position: "relative" }}>
            <canvas ref={canvasRef} style={{ border: "1px solid #ddd" }}></canvas>
            <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}>
                {entities.map((entity) => (
                    <div
                        key={entity.id}
                        onClick={() => handleEntityClick(entity)}
                        style={{
                            position: "absolute",
                            left: `${entity.x}px`,
                            top: `${entity.y}px`,
                            width: `${entity.width}px`,
                            height: `${entity.height}px`,
                            cursor: "pointer",
                        }}
                    >
                        {entity.type === "Agent" && <Netling data={entity} />}
                        {entity.type === "Food" && <Food data={entity} />}
                    </div>
                ))}
            </div>
            <div
                style={{
                    position: "relative",
                    width: "300px",
                    marginTop: "20px",
                    border: "1px solid #ccc",
                    padding: "10px",
                }}
            >
                <h2>Netling Data</h2>
                {entityData ? (
                    <NetlingDataCard data={entityData} />
                ) : (
                    <p>Wähle einen Agenten, um Details anzuzeigen.</p>
                )}
            </div>
        </div>
    );
};

// Farben für die verschiedenen Biome-Namen
const getBiomeColor = (biomeName) => {
    const colors = {
        Fauna: "#FFD700", // Gelb für Fauna
        Savanne: "#228B22", // Grün für Savanne
    };
    return colors[biomeName] || "#ccc"; // Standardfarbe für unbekannte Biome
};

export default BiomeWebSocketVisualizer;
