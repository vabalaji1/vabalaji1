import define1 from "./a33468b95d0b15b0@817.js";

function _1(md){return(
md`<div style="color: grey; font: 13px/25.5px var(--sans-serif); text-transform: uppercase;"><h1 style="display: none;">Choropleth</h1><a href="https://d3js.org/">D3</a> › <a href="/@d3/gallery">Gallery</a></div>

# Choropleth

Unemployment rate by U.S. county, August 2016. Data: [Bureau of Labor Statistics](http://www.bls.gov/lau/#tables).`
)}

function _chart(d3,data,topojson,us,Legend)
{
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
    countiesPaths.style("opacity", 0.3);

    d3.select(this)
      .transition()
      .duration(100)
      .style("opacity", 1)
      .style("stroke", "black")
      .style("stroke-width", 2); 
  })
  .on("mouseleave", function() {
    countiesPaths.style("opacity", 1);
    d3.select(this)
      .transition()
      .duration(100)
      .style("stroke", null) 
      .style("stroke-width", null); 
  });

  svg.append("path")
      .datum(statemesh)
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-linejoin", "round")
      .attr("d", path);

  return svg.node();
}




async function _data(FileAttachment){return(
(await FileAttachment("unemployment-x.csv").csv()).map((d) => (d.rate = +d.rate, d))
)}

function _us(FileAttachment){return(
FileAttachment("counties-albers-10m.json").json()
)}



function _8(Plot,topojson,us,data){return(
Plot.plot({
  projection: "identity",
  width: 975,
  height: 610,
  color: {scheme: "Reds", type: "quantize", n: 9, domain: [1, 10], label: "Unemployment rate (%)", legend: false},
  marks: [
    Plot.geo(topojson.feature(us, us.objects.counties), {
      fill: (map => d => map.get(d.id))(new Map(data.map(d => [d.id, d.rate]))),
    }),

    
    
    Plot.geo(topojson.mesh(us, us.objects.counties, (a, b) => a !== b), {stroke: "blue"}),
    Plot.geo(topojson.mesh(us, us.objects.states, (a, b) => a !== b), {stroke: "yellow"}),

    Plot.geo(topojson.mesh(us, us.objects.nation), {stroke: "black"}),
    
    Plot.tip(
      Plot.geo(topojson.feature(us, us.objects.counties), {
        fill: (map => d => map.get(d.id))(new Map(data.map(d => [d.id, d.rate])))
      }),
      {
        title: (d) => d.properties.name,
        anchor: "bottom", 
        textPadding: 3
      }
    )
  ]
})
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["counties-albers-10m.json", {url: new URL("./files/6b1776f5a0a0e76e6428805c0074a8f262e3f34b1b50944da27903e014b409958dc29b03a1c9cc331949d6a2a404c19dfd0d9d36d9c32274e6ffbc07c11350ee.json", import.meta.url), mimeType: "application/json", toString}],
    ["unemployment-x.csv", {url: new URL("./files/8a6057f29caa4e010854bfc31984511e074ff9042ec2a99f30924984821414fbaeb75e59654e9303db359dfa0c1052534691dac86017c4c2f992d23b874f9b6e.csv", import.meta.url), mimeType: "text/csv", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("chart")).define("chart", ["d3","data","topojson","us","Legend"], _chart);
  main.variable(observer()).define(["md"], _3);
  main.variable(observer("data")).define("data", ["FileAttachment"], _data);
  main.variable(observer("us")).define("us", ["FileAttachment"], _us);
  const child1 = runtime.module(define1);
  main.import("Legend", child1);
  main.variable(observer()).define(["md"], _7);
  main.variable(observer()).define(["Plot","topojson","us","data"], _8);
  return main;
}
