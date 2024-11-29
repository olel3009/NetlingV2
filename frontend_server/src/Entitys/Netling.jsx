const Netling = ({ data }) => {
    const { x, y, r, width, height } = data; // Extrahiere x und y aus den Daten
    return (
        <div
            style={{
                width: `${height}px`,
                height: `${width}px`,
                backgroundColor: "black",
                position: "absolute",
                transform: `translate(${x}px, ${y}px) rotate(${r}deg)`,
            }}
        ></div>
    );
};
export default Netling;

