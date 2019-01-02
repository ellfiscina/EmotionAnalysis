function drawDispersion(tokens, commonArray){
  var margin = {top: 20, right: 10, bottom: 20, left: 10};
  var width = $("#dispersion-plot").width() - 50;
  var height = 350;

  var x = d3.scale
            .linear()
            .domain([0, tokens.length])
            .range([0, width]);

  var xAxis = d3.svg.axis().scale(x).orient("bottom");

  var color = d3.scale.category10();

  var svg;

  svg = d3.select("#dispersion-plot")
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.bottom + margin.top)
          .append("g")
            .attr("transform", "translate(" + margin.left + ", 0)")
            .style("shape-rendering", "crispEdges");

  svg.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(" + margin.right + "," + (height - margin.top) + ")")
     .call(xAxis)
     .append("text")
       .attr("class", "label")
       .attr("x", width/2)
       .attr("y", 46)
       .style("text-anchor", "end")
       .text("Posição");

  commonArray.forEach(function(element, index, array){
    dataset = createDataset(tokens, element);

      svg.append("g")
         .attr("class", element)
         .selectAll("rect")
           .data(dataset)
           .enter()
         .append("rect")
           .attr("x", d=>x(d))
           .attr("y", -60 * index + 240)
           .attr("width", 1)
           .attr("height", 50)
           .attr("transform","translate(" + margin.right + "," + (height - margin.top) + "),scale(1,-1)")
           .style("fill", color(index))
           .style("stroke", color(index));
  });

  drawLegend();

  function createDataset(tokens, WORD){
    var x = [];

    for (i = 0; i < tokens.length; i++) {
      if(tokens[i] == WORD){
        x.push(i);
      }
    }

    return x;
  };

  function drawLegend(){
    var legend = d3.select("#dispersion-legend")
                   .append("svg")
                     .attr("width", width + margin.left + margin.right)
                     .attr("height", 20)
                   .selectAll(".legend")
                   .data(commonArray)
                   .enter()
                   .append("g")
                     .attr("class", "legend")
                     .attr("transform", (d, i) => "translate(" + i * -100 + ", 0)");

    legend.append("rect")
          .attr("x", width - 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", (d,i) => color(i));

    legend.append("text")
          .attr("x", width - 24)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(d => d);
  }
}

function drawBubble(data){
  var diameter = $("#bubble-plot").width();
  var color = d3.scale.category20b();

  var bubble = d3.layout
                 .pack()
                 .sort(null)
                 .size([diameter, diameter])
                 .padding(5);

  var svg = d3.select("#bubble-plot")
              .append("svg")
              .attr("width", diameter)
              .attr("height", diameter)
              .attr("class", "bubble");

  var nodes = bubble.nodes({children:data})
                    .filter(d => !d.children)
  var bubbles = svg.append("g")
                   .attr("transform", "translate(0,0)")
                   .selectAll(".bubble")
                   .data(nodes)
                   .enter();

  bubbles.append("circle")
         .attr("r", d => d.r)
         .attr("cx", d => d.x)
         .attr("cy", d => d.y)
         .style("fill", d => color(d.value))

  bubbles.append("text")
         .attr("x", d => d.x)
         .attr("y", d => d.y + 5)
         .attr("text-anchor", "middle")
         .text(d => d.text)
}

$(document).ready(function() {
  drawBubble(mostFrequent);
	drawDispersion(tokens, commonArray);
});
