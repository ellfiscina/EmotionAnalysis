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

function drawDispersion(tokens, commonArray){
  var width = $("#dispersion-plot").width() - 50;
  var height = 350;

  var x = d3.scale
            .linear()
            .domain([0, tokens.length])
            .range([0, (width - margin.top)]);

  var xAxis = d3.svg.axis().scale(x).ticks(5).orient("bottom");

  var color = d3.scale.ordinal().range(generateColorScale(5));

  var svg = d3.select("#dispersion-plot")
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.bottom + margin.top)
                .attr("class", "dist-svg")
              .append("g")
                .attr("transform", "translate(" + margin.left + ", 0)")
                .style("shape-rendering", "crispEdges");

  svg.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(" + margin.right + "," +
           (height - margin.top) + ")")
     .call(xAxis)
     .append("text")
       .attr("class", "label")
       .attr("x", width/2)
       .attr("y", 46)
       .style("text-anchor", "end")
       .text("Posição");

  commonArray.forEach(function(element, index, array){
    dataset = createDataset(tokens, element);
      g = svg.append("g")
             .attr("class", element)
             .selectAll("rect")
              .data(dataset)
              .enter();
      dist = g.append("rect")
              .attr("x", d=>x(d))
              .attr("y", -60 * (4 - index) + 240)
              .attr("width", 1)
              .attr("height", 50)
              .attr("transform","translate(" + margin.right + "," +
                   (height - margin.top) + "),scale(1,-1)")
              .style("fill", color(index))
              .style("stroke", color(index));

      var tip = d3.tip().attr("class", "d3-tip").html(element + " - " + index);
      dist.call(tip);

      dist.on("mouseover", function(d) {
        tip.show(d);
       })
       .on("mouseout", function(d) {
        tip.hide(d);
       });
  });

  var legend = d3.select("#dispersion-legend")
                 .append("svg")
                   .attr("width", width + margin.left + margin.right)
                   .attr("height", 20)
                   .attr("class", "legend-svg")
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

  function createDataset(tokens, WORD){
    var x = [];

    for (i = 0; i < tokens.length; i++) {
      if(tokens[i] == WORD){
        x.push(i);
      }
    }

    return x;
  };
}

function drawCloud(data, n){
  data = data.slice(0,n)

  var width = $("#cloud-plot").width() - margin.top;
  var height = $("#cloud-plot").height() - margin.top;
  var color = d3.scale.ordinal().range(generateColorScale(50));

  var cloud = d3.layout
                .pack()
                .sort(null)
                .size([width, width])
                .padding(width/15);

  var svg = d3.select("#cloud-plot")
              .append("svg")
              .attr("width", width)
              .attr("height", height)
              .attr("class", "cloud");

  var nodes = cloud.nodes({children:data})
                   .filter(d => !d.children)

  var g = svg.append("g")
                .attr("transform", "translate(0,30)")
                .selectAll(".cloud")
                .data(nodes)
                .enter();

  tags = g.append("text")
          .attr("x", d => d.x)
          .attr("y", d => d.y + 5)
          .attr("text-anchor", "middle")
          .style('fill', d => color(d.value))
          .style("font-size", d => d.r + "px")
          .text(d => d.text);

  var tip = d3.tip().attr("class", "d3-tip").html(d => d.value);
  tags.call(tip);

  tags.on("mouseover", function(d) {
        d3.select(this).style("font-size", d => d.r + 10);
        tip.show(d);
      })
      .on("mouseout", function(d) {
        d3.select(this).style("font-size", d => d.r);
        tip.hide(d);
      });
}

function populateSelect(words){
  words.forEach(function(element, index){
    $('#word-dist-sel').append('<option value="' + element + '">' + element + '</option>');
  });
}

$(document).ready(function() {
  var words = new Set(filtered);

  populateSelect(words);
  drawCloud(mostFrequent, 150);
  drawDispersion(tokens, commonArray);

  $('#amount').change(function(){
    d3.select('svg.cloud').remove();
    drawCloud(mostFrequent, $(this).val());
  });

  $('#word-submit').on('click', function(){
    d3.select('.dist-svg').remove();
    d3.select('.legend-svg').remove();
    drawDispersion(tokens, [$('#word-dist').val()]);
  });
});
