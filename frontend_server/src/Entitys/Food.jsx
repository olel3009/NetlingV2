const Food = ({ data }) => {
    const { x, y, width, height } = data; // Extrahiere x und y aus den Daten
    return (
        <div
            style={{
                width: `${width}px`,
                height: `${height}px`,
                backgroundColor: "orange",
                position: "absolute",
                transform: `translate(${x}px, ${y}px)`,
                transition: "transform 0.016s linear",
            }}
        ></div>
    );
}
export default Food;