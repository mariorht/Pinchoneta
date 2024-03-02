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

// Crea una función de escala de color basada en el conteo de contribuciones
const colorScale = d3.scaleQuantize()
    .domain([0, d3.max(data, d => d.count)])
    .range(d3.schemeGreens[9]); // Utiliza 9 tonos de verde

// Crea el elemento SVG en ele contenedor con id "ussageChart"
const svg = d3.select("#usageChart").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("class", "calendar");

// Añade los cuadrados al SVG
const dayRects = svg.selectAll(".day")
    .data(data)
    .enter().append("rect")
    .attr("class", "day")
    .attr("width", cellSize)
    .attr("height", cellSize)
    .attr("x", d => d3.timeWeek.count(d3.timeYear(d.date), d.date) * cellSize)
    .attr("y", d => weekDays.indexOf(d3.timeFormat("%a")(d.date)) * cellSize)
    .attr("fill", d => colorScale(d.count))
    .text(d => `${d.date.toDateString()}: ${d.count}`);


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

dayRects.on("mouseover", function (event, d) {
    tooltip.style("visibility", "visible")
        .html(`Fecha: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Contribuciones: ${d.count}`);
})
    .on("mousemove", function (event) {
        tooltip.style("top", (event.pageY - 10) + "px")
            .style("left", (event.pageX + 10) + "px");
    })
    .on("mouseout", function () {
        tooltip.style("visibility", "hidden");
    });