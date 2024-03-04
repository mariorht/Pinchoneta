function generateUsageChart(usageData, elementId) {
    // Configuración básica
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const cellSize = 12; // tamaño de los cuadrados
    const cellMargin = 2; // margen entre los cuadrados
    const cellSizeWithMargin = cellSize + cellMargin; // tamaño total de cada cuadrado incluyendo el margen
    const total_width = 960
    const width = total_width - margin.left - margin.right; // ancho ajustado para márgenes
    const total_height = 136
    const height = total_height - margin.top - margin.bottom; // altura ajustada para márgenes
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
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`); // Mueve el grupo hacia abajo y hacia la derecha para los márgenes

    // Añade los cuadrados al SVG con separación
    const dayRects = svg.selectAll(".day")
        .data(data)
        .enter().append("rect")
        .attr("class", "day")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("x", d => d3.timeWeek.count(d3.timeYear(d.date), d.date) * cellSizeWithMargin + cellMargin)
        .attr("y", (d, i) => weekDays.indexOf(d3.timeFormat("%a")(d.date)) * cellSizeWithMargin + cellMargin)
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



    // Crea los ejes X e Y utilizando las escalas y añadiéndolos al SVG
    const xScale = d3.scaleTime()
        .domain([d3.timeYear(new Date(data[0].date)), d3.timeYear.offset(new Date(data[0].date), 1)])
        .range([0, cellSizeWithMargin*52]);

    const yScale = d3.scaleBand()
        .domain(weekDays)
        .range([cellSizeWithMargin*7, 0]);

    const xAxis = d3.axisBottom(xScale).ticks(d3.timeMonth.every(1)).tickSize(0).tickFormat(d3.timeFormat('%b')).tickPadding(5);
    const yAxis = d3.axisLeft(yScale).tickSize(0).tickPadding(5);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0,${cellSizeWithMargin*7})`)
        .call(xAxis)
        .select(".domain").remove();

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .select(".domain").remove();

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
