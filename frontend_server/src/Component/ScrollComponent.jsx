import React, { useEffect } from "react";

const ScrollComponent = ({ children }) => {
    useEffect(() => {
        const handleKeyDown = (e) => {
            const step = 100; // Schrittweite für das Scrollen

            if (e.key === "ArrowUp") {
                window.scrollBy({ top: -step, left: 0, behavior: "smooth" }); // Nach oben scrollen
            } else if (e.key === "ArrowDown") {
                window.scrollBy({ top: step, left: 0, behavior: "smooth" }); // Nach unten scrollen
            } else if (e.key === "ArrowLeft") {
                window.scrollBy({ top: 0, left: -step, behavior: "smooth" }); // Nach links scrollen
            } else if (e.key === "ArrowRight") {
                window.scrollBy({ top: 0, left: step, behavior: "smooth" }); // Nach rechts scrollen
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, []);

    return (
        <div
            style={{
                overflow: "hidden", // Scrollbars ausblenden
                height: "100vh", // Volle Fensterhöhe
                width: "100vw", // Volle Fensterbreite
            }}
        >
            {children}
        </div>
    );
};

export default ScrollComponent;
