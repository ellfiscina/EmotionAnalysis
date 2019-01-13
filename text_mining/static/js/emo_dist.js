var margin = {top: 20, right: 25, bottom: 15, left: 25};
var width = $("#emotion-plot").width() - 50;
var height = 300;
var distSvg;
var x, y;

function drawSVG(){
  distSvg = d3.select("#emotion-plot")
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.bottom + margin.top)
          .append("g")
            .attr("class", "outter")
            .attr("transform", "translate(10, 0)")
            .style("shape-rendering", "crispEdges");
}

function drawXAxis(){
  var xAxis = d3.svg.axis().scale(x).orient("bottom");
  var yAxis = d3.svg.axis().scale(y).orient("left");

  distSvg.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(" + (margin.right + margin.left) + "," +
             (height - margin.bottom) + ")")
       .style("font-size", "smaller")
     .call(xAxis)
     .append("text")
       .attr("class", "label")
       .attr("x", width/2)
       .attr("y", 46)
       .style("text-anchor", "end")
       .text("Trecho (100 sentenças)");

  distSvg.append("g")
       .attr("class", "y axis")
       .attr("transform", "translate(" + (margin.right + margin.left) + ", 5)")
       .style("font-size", "smaller")
     .call(yAxis)
     .append("text")
       .attr("class", "label")
       .attr("x", -30)
       .attr("y", height/2)
       .style("text-anchor", "end")
       .text("Qtd");
}

function drawDispersion(data, key){
  line = d3.svg.line()
           .defined(d => !isNaN(d[1]))
           .x(d => x(d[0]))
           .y(d => y(d[1]))

  distSvg.append("g")
         .attr("transform", "translate(" + (margin.right + margin.left) + ", 0)")
         .append("path")
         .datum(data[key])
         .attr("class", "dist-" + key)
         .attr("fill", "none")
         .attr("stroke-width", 1.5)
         .attr("stroke-linejoin", "round")
         .attr("stroke-linecap", "round")
         .attr("d", line);
}

function cleanSVG(key){
  distSvg.selectAll(".dist-" + key).remove();
}

function maxValue(data){
  var maximum = []
  for(var key in data) {
    maximum.push(d3.max(data[key], d => d[1]))
  }
  return maximum
}

$(document).ready(function(){
  x = d3.scale
        .linear()
        .domain([0, dist["positivo"].length])
        .range([0, width]);

  y = d3.scale
        .linear()
        .domain([0, d3.max(maxValue(dist), d => d)])
        .range([height - margin.top, 0]);

  drawSVG();
  drawXAxis();

  for(var key in dist){
    drawDispersion(dist, key);
  }

  var $checkboxes = $('input[name="emotion"]');

  $checkboxes.change(function(){
    if ($(this).is(':not(:checked)')){
      cleanSVG($(this).val())
    }
    else {
      drawDispersion(dist, $(this).val());
    }
  });
});
