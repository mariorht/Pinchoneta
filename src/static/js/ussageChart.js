function generateUsageChart(usageData, elementId) {
    // Configuración básica
    const cellSize = 12; // tamaño de los cuadrados
    const width = 960;
    const height = 136;
    const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

    // Convierte los datos de uso en un array de objetos
    const data = Object.keys(usageData).map(date => ({
        date: new Date(date),
        count: usageData[date]
    }));

    // Define los umbrales de conteo de consumo y los colores correspondientes
    const colorScale = d3.scaleThreshold()
        .domain([1, 2, 3, 4, 5]) // Define tus umbrales de conteo aquí
        .range(["#edf8e9", "#bae4b3", "#74c476", "#31a354", "#006d2c"]); // Colores correspondientes a los rangos


    // Crea el elemento SVG en el contenedor especificado por elementId
    const svg = d3.select(elementId).append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("class", "calendar");

    // Añade los cuadrados al SVG
    svg.selectAll(".day")
        .data(data)
        .enter().append("rect")
        .attr("class", "day")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("x", d => d3.timeWeek.count(d3.timeYear(d.date), d.date) * cellSize)
        .attr("y", d => weekDays.indexOf(d3.timeFormat("%a")(d.date)) * cellSize)
        .attr("fill", d => colorScale(d.count));

    // Tooltip para mostrar información al pasar el mouse
    const tooltip = d3.select("body").append("div")
        .attr("class", "d3_tooltip")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("background", "white")
        .style("border", "solid 1px #aaa")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style("pointer-events", "none");

    svg.selectAll(".day")
        .on("mouseover", function (event, d) {
            tooltip.style("visibility", "visible")
                .html(`Fecha: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Consumo: ${d.count}`);
        })
        .on("mousemove", function (event) {
            tooltip.style("top", (event.pageY - 10) + "px")
                .style("left", (event.pageX + 10) + "px");
        })
        .on("mouseout", function () {
            tooltip.style("visibility", "hidden");
        });
}
