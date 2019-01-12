var margin = {top: 20, right: 10, bottom: 20, left: 10};

function drawDispersion(data){
  var labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
                'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']

  var width = $("#dispersion-plot").width() - 50;
  var height = 450;

  var x = d3.scale
            .linear()
            .domain([0, data.length])
            .range([0, width]);

  var xAxis = d3.svg.axis().scale(x).orient("bottom");

  var color = d3.scale.ordinal().range(generateColorScale(5));

  var svg = d3.select("#dispersion-plot")
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
       .text("Trecho (100 sentenças)");

  for (var key in data) {
    svg.append("g")
       .attr("class", key)
       .selectAll("rect")
         .data(data[key])
         .enter()
       .append("rect")
         .attr("x", d => d[0])
         .attr("y", -60 * labels.indexOf(key) + 240)
         .attr("width", 1)
         .attr("height", d => d[1] * 5)
         .attr("transform","translate(" + margin.right + "," + (height - margin.top) + "),scale(1,-1)")
         .style("fill", color(labels.indexOf(key)))
         .style("stroke", color(labels.indexOf(key)));
  }

  var legend = d3.select("#dispersion-legend")
                 .append("svg")
                   .attr("width", width + margin.left + margin.right)
                   .attr("height", 20)
                 .selectAll(".legend")
                 .data(labels)
                 .enter()
                 .append("g")
                   .attr("class", "legend")
                   .attr("transform", (d, i) => "translate(" + i * -50 + ", 0)");

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

$(document).ready(function() {
  drawDispersion(tokens, commonArray);
});
