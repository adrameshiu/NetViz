var margin = {top: 0, right: 30, bottom: 50, left: 60},
  width = 650 - margin.left - margin.right,
  height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");



 // We load the JSON network file.
d3.json("graph_out.json", function(error, graph) {
	// Within this block, the network has been loaded
	// and stored in the 'graph' object.

  

  function initChart(){
    //all your code for initChart here
    	// We load the nodes and links into the force-directed
	// graph and initialise the dynamics.
	force.nodes(graph.nodes)
  .links(graph.links)
  .start();

// We create a < line> SVG element for each link
// in the graph.
var link = svg.selectAll(".link")
  .data(graph.links)
  .enter().append("line")
  .attr("class", "link");

// We create a < circle> SVG element for each node
// in the graph, and we specify a few attributes.
var node = svg.selectAll(".node")
  .data(graph.nodes)
  .enter().append("circle")
  .attr("class", "node")
  .attr("r", 5)  // radius
  .style("fill", function(d) {
    // We colour the node depending on the degree.
    return color(d.degree); 
  })
  .call(force.drag);

// The label each node its node number from the networkx graph.
node.append("title")
  .text(function(d) { return d.id; });



// We bind the positions of the SVG elements
// to the positions of the dynamic force-directed graph,
// at each time step.
force.on("tick", function() {
  link.attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });

  node.attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; });
});

};

initChart();
});


// // Read dummy data
// d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_researcherNetwork.json", function( data) {

//   // List of node names
//   var allNodes = data.nodes.map(function(d){return d.name})

//   // List of groups
//   var allGroups = data.nodes.map(function(d){return d.grp})
//   allGroups = [...new Set(allGroups)]

//   // A color scale for groups:
//   var color = d3.scaleOrdinal()
//     .domain(allGroups)
//     .range(d3.schemeSet3);

//   // A linear scale for node size
//   var size = d3.scaleLinear()
//     .domain([1,10])
//     .range([2,10]);

//   // A linear scale to position the nodes on the X axis
//   var x = d3.scalePoint()
//     .range([0, width])
//     .domain(allNodes)

//   // In my input data, links are provided between nodes -id-, NOT between node names.
//   // So I have to do a link between this id and the name
//   var idToNode = {};
//   data.nodes.forEach(function (n) {
//     idToNode[n.id] = n;
//   });

//   // Add the links
//   var links = svg
//     .selectAll('mylinks')
//     .data(data.links)
//     .enter()
//     .append('path')
//     .attr('d', function (d) {
//       start = x(idToNode[d.source].name)    // X position of start node on the X axis
//       end = x(idToNode[d.target].name)      // X position of end node
//       return ['M', start, height-30,    // the arc starts at the coordinate x=start, y=height-30 (where the starting node is)
//         'A',                            // This means we're gonna build an elliptical arc
//         (start - end)/2, ',',    // Next 2 lines are the coordinates of the inflexion point. Height of this point is proportional with start - end distance
//         (start - end)/2, 0, 0, ',',
//         start < end ? 1 : 0, end, ',', height-30] // We always want the arc on top. So if end is before start, putting 0 here turn the arc upside down.
//         .join(' ');
//     })
//     .style("fill", "none")
//     .attr("stroke", "grey")
//     .style("stroke-width", 1)

//   // Add the circle for the nodes
//   var nodes = svg
//     .selectAll("mynodes")
//     .data(data.nodes.sort(function(a,b) { return +b.n - +a.n }))
//     .enter()
//     .append("circle")
//       .attr("cx", function(d){ return(x(d.name))})
//       .attr("cy", height-30)
//       .attr("r", function(d){ return(size(d.n))})
//       .style("fill", function(d){ return color(d.grp)})
//       .attr("stroke", "white")

//   // And give them a label
//   var labels = svg
//     .selectAll("mylabels")
//     .data(data.nodes)
//     .enter()
//     .append("text")
//       .attr("x", 0)
//       .attr("y", 0)
//       .text(function(d){ return(d.name)} )
//       .style("text-anchor", "end")
//       .attr("transform", function(d){ return( "translate(" + (x(d.name)) + "," + (height-15) + ")rotate(-45)")})
//       .style("font-size", 6)

//   // Add the highlighting functionality
//   nodes
//     .on('mouseover', function (d) {
//       // Highlight the nodes: every node is green except of him
//       nodes
//         .style('opacity', .2)
//       d3.select(this)
//         .style('opacity', 1)
//       // Highlight the connections
//       links
//         .style('stroke', function (link_d) { return link_d.source === d.id || link_d.target === d.id ? color(d.grp) : '#b8b8b8';})
//         .style('stroke-opacity', function (link_d) { return link_d.source === d.id || link_d.target === d.id ? 1 : .2;})
//         .style('stroke-width', function (link_d) { return link_d.source === d.id || link_d.target === d.id ? 4 : 1;})
//       labels
//         .style("font-size", function(label_d){ return label_d.name === d.name ? 16 : 2 } )
//         .attr("y", function(label_d){ return label_d.name === d.name ? 10 : 0 } )

//     })
//     .on('mouseout', function (d) {
//       nodes.style('opacity', 1)
//       links
//         .style('stroke', 'grey')
//         .style('stroke-opacity', .8)
//         .style('stroke-width', '1')
//       labels
//         .style("font-size", 6 )

//     })
// })





// d3.select('div')
//     .selectAll('p')
//     .data([1,2,3])
//     .enter()
//     .append('p')
//     .text(dta => dta);

// var svg = d3.select("#d3example")
//     .append("svg")
//     .attr("width", width)
//     .attr("height", height);

// var exampleData = [{"name": "A"}, {"name": "B"}, {"name": "C"}, {"name": "D"}];
// var node = svg.append("g")
//         .selectAll("nodes")
//         .data(exampleData)
//         .enter();

// var circles = node.append("circle")
//     .attr("cx", () => {return Math.random() * width})
//     .attr("cy", () => {return Math.random() * height})
//     .attr("r", 40)
//     .style("fill", rgb(239, 192, 80));