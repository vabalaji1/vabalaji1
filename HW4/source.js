chart  = {
    const color = d3.scaleQuantize([1, 10], d3.schemeReds[9]);
    const boundaryColor = d3.scaleQuantize([1, 10], d3.schemeBlues[9]);
    const path = d3.geoPath();
    const format = d => `${d}%`;
    const valuemap = new Map(data.map(d => [d.id, d.rate]));
  
    const counties = topojson.feature(us, us.objects.counties);
    const states = topojson.feature(us, us.objects.states);
    const statemap = new Map(states.features.map(d => [d.id, d]));
  
    const statemesh = topojson.mesh(us, us.objects.states, (a, b) => a !== b);
  
    const svg = d3.create("svg")
        .attr("width", 975)
        .attr("height", 610)
        .attr("viewBox", [0, 0, 975, 610])
        .attr("style", "max-width: 100%; height: auto;");
  
    svg.append("g")
        .attr("transform", "translate(610,20)")
        .append(() => Legend(color, {title: "Unemployment rate (%)", width: 260}));
  
    const countiesPaths = svg.append("g")
      .selectAll("path")
      .data(counties.features)
      .join("path")
        .attr("fill", d => color(valuemap.get(d.id)))
        .attr("d", path)
        .attr("stroke", "yellow");
  
  countiesPaths.append("title")
    .text(d => {
      const stateInfo = statemap.get(d.id.slice(0, 2));
      return `State: ${stateInfo.properties.name}\nCounty: ${d.properties.name}\n${format(valuemap.get(d.id))}`;
    })
  
    // Hover functionality
    countiesPaths
    .on("mouseenter", function(event, d) {
      // Reduce the opacity of all paths to make them appear lighter
      countiesPaths.style("opacity", 0.3);
  
      // Highlight the hovered path by setting its opacity to 1 and changing the stroke
      d3.select(this)
        .transition()
        .duration(100)
        .style("opacity", 1) // Highlight the current path
        .style("stroke", "black") // Change the stroke to make it stand out
        .style("stroke-width", 2); // Increase stroke width
    })
    .on("mouseleave", function() {
      // Reset the opacity of all paths to make them fully opaque again
      countiesPaths.style("opacity", 1);
  
      // Revert the stroke of the hovered path to its original state
      d3.select(this)
        .transition()
        .duration(100)
        .style("stroke", null) // Revert stroke to original (or "none" if it was not set)
        .style("stroke-width", null); // Revert stroke width to original
    });
  
    svg.append("path")
        .datum(statemesh)
        .attr("fill", "none")
        .attr("stroke", "blue")
        .attr("stroke-linejoin", "round")
        .attr("d", path);
  
    return svg.node();
  }