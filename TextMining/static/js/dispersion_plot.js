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

function main(tokens, commonArray){
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

$(document).ready(function() {
	main(tokens, commonArray);
});
