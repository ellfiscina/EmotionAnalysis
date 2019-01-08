var margin = {top: 20, right: 10, bottom: 20, left: 10};

function generateColorScale(n){
  var colors = paletteGenerator.generate(
    n, // Colors
    function(color){ // This function filters valid colors
      var hcl = color.hcl();
      return hcl[0]>=0 && hcl[0]<=360
        && hcl[1]>=30 && hcl[1]<=80
        && hcl[2]>=35 && hcl[2]<=80;
    },
    false, // Using Force Vector instead of k-Means
    50, // Steps (quality)
    false, // Ultra precision
    'Default' // Color distance type (colorblindness)
  );
  // Sort colors by differenciation first
  return paletteGenerator.diffSort(colors, 'Default');
}

function drawDispersion(data){
  var labels = ['positivo', 'negativo', 'alegria', 'tristeza', 'nojo',
                'antecipação', 'medo', 'surpresa', 'confiança', 'raiva']

  var width = $("#emotion-plot").width() - 50;
  var height = 650;

  var x = d3.scale
            .linear()
            .domain([0, data['positivo'].length])
            .range([0, width]);

  var xAxis = d3.svg.axis().scale(x).orient("bottom");

  var color = d3.scale.ordinal().range(generateColorScale(5));

  var svg = d3.select("#emotion-plot")
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.bottom + margin.top)
              .append("g")
                .attr("transform", "translate(" + margin.left + ", -300)")
                .style("shape-rendering", "crispEdges");

  svg.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(" + margin.right + "," + (height - margin.top + 300) + ")")
     .call(xAxis)
     .append("text")
       .attr("class", "label")
       .attr("x", width/2)
       .attr("y", 46)
       .style("text-anchor", "end")
       .text("Posição");

  for(var key in data){
    index = labels.indexOf(key);
    svg.append("g")
       .attr("class", key)
       .selectAll("rect")
         .data(data[key])
         .enter()
       .append("rect")
         .attr("x", d => x(d[0]))
         .attr("y", -60 * index + 240)
         .attr("width", 1)
         .attr("height", d => d[1] * 10)
         .attr("transform","translate(" + margin.right + "," + (height - margin.top) + "),scale(1,-1)")
         .style("fill", color(index))
         .style("stroke", color(index));
  }

  var legend = d3.select("#emotion-legend")
                 .append("svg")
                   .attr("width", width + margin.left + margin.right)
                   .attr("height", 20)
                 .selectAll(".legend")
                 .data(labels)
                 .enter()
                 .append("g")
                   .attr("class", "legend")
                   .attr("transform", (d, i) => "translate(" + i * -80 + ", 0)");

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
	drawDispersion(dist);
});
