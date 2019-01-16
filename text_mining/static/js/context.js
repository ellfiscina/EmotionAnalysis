function main(data) {
  var margin = { top: 40, right: 0, bottom: 0, left: 0 };
  var width = $("#treeword-plot").width() - 50;
  var height = 200;
  var i = 0;
  var root = data;
      root.x0 = height / 2;
      root.y0 = 0;

  var tree = d3.layout.tree().size([height, width]);

  var diagonal = d3.svg.diagonal()
                      .projection(d => [d.y, d.x]);

  var svg = d3.select("#treeword-plot")
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.bottom + margin.top)
                .style("margin-left", -margin.left + "px")
                .style("margin.right", -margin.right + "px")
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                .style("shape-rendering", "crispEdges");

  update(root);

  function update(root){
    var duration = d3.event && d3.event.altKey ? 5000 : 500;

    var nodes = tree.nodes(root).reverse();
    nodes.forEach(d => d.y = d.depth * 180);

    var node = svg.selectAll("g.node")
                  .data(nodes, d => d.id || (d.id = ++i));

    var nodeEnter = node.enter()
                        .append("svg")
                        .attr("class", "node")
                        .attr("transform", d => "translate(" + root.y0 + "," + root.x0 + ")")
                        .on("click", function(d) { toggle(d); update(d); });
    nodeEnter.append("circle")
             .attr("r", 1e-6)
             .style("fill", d => d._children ? "lightsteelblue" : "#fff");
    nodeEnter.append("text")
             .attr("x", d => d.children || d._children? -10 : 10)
             .attr("dy", ".35em")
             .attr("text-anchor", d => d.children || d._children ? "end" : "start")
             .text(d => d.name)
             .style("fill-opacity", 1e-6);

    var nodeUpdate = node.transition()
                         .duration(duration)
                         .attr("transform", d => "translate(" + d.y + "," + d.x + ")")
    nodeUpdate.select("circle")
              .attr("r", 4.5)
              .style("fill", d => d._children ? "lightsteelblue" : "#fff")
    nodeUpdate.select("text")
              .style("fill-opacity", 1)

    var nodeExit = node.exit().transition()
                              .duration(duration)
                              .attr("transform", d => "translate(" + root.y + "," + root.x + ")")
    nodeExit.select("circle")
            .attr("r", 1e-6)
    nodeExit.select("text")
              .style("fill-opacity", 1e-6)

    var link = svg.selectAll("path.link")
                  .data(tree.links(nodes), d => d.target.id)
    link.enter()
        .insert("path", "g")
        .attr("d", function(d) {
          var o = {x: root.x0, y: root.y0};
          return diagonal({root: o, target: o});
        })
        .transition()
          .duration(duration)
          .attr("d", diagonal);
    link.transition()
        .duration(duration)
        .attr("d", diagonal);
    link.exit().transition()
               .duration(duration)
               .attr("d", function(d) {
                 var o = {x: root.x, y: root.y};
                 return diagonal({root: o, target: o});
               })
               .remove();

    nodes.forEach(function(d) {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }

  function toggleAll(d){
    if (d.children){
      d.children.forEach(toggleAll);
      toggle(d);
    }
  }

  function toggle(d){
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else {
      d.children = d._children;
      d._children = null;
    }
  }
}


$(document).ready(function() {
  $word = $('#max-word').html()
  var re = new RegExp($word,"g");
  $('div.n-grams').each(function() {
    $(this).html($(this).html().replace(re, '<span style="color: red">$&</span>'));
  });

  var data = JSON.parse(document.getElementById('treeword').textContent)
  main(data)
  // main(JSON.parse(data))
});
