var margin = {top: 20, right: 20, bottom: 20, left: 20};
var width = $("#emotion-plot").width() - 50;
var height = 250;
var distSvg;

function drawSVG(){
  distSvg = d3.select("#emotion-plot")
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.bottom + margin.top)
          .append("g")
            .attr("class", "outter")
            .attr("transform", "translate(20, 0)")
            .style("shape-rendering", "crispEdges");
}

function drawDispersion(data, key){
  var x = d3.scale
            .linear()
            .domain([0, data[key].length])
            .range([0, width]);

  var xAxis = d3.svg.axis().scale(x).orient("bottom");

  distSvg.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(" + margin.right + "," + (height - margin.top) + ")")
     .call(xAxis)
     .append("text")
       .attr("class", "label")
       .attr("x", width/2)
       .attr("y", 46)
       .style("text-anchor", "end")
       .text("Posição");

  distSvg.append("g")
     .selectAll("rect")
       .data(data[key])
       .enter()
     .append("rect")
       .attr("class", "dist-" + key)
       .attr("x", d => x(d[0]))
       .attr("y", 240)
       .attr("width", 1)
       .attr("height", d => d[1] * 25)
       .attr("transform","translate(" + margin.right + "," + (height - margin.top + 240) + "),scale(1,-1)");
}

function cleanSVG(){
  distSvg.selectAll("*").remove();
}

$(document).ready(function(){
  drawSVG();
  drawDispersion(dist, 'positivo');

  var $radios = $('input[name="emotion"]');

  $radios.change(function(){
    var $checked = $radios.filter(function(){
      return $(this).prop('checked');
    });

    cleanSVG();
    drawDispersion(dist, $checked.val());
  });
});
