function main(data, color) {
  var margin = { top: 20, right: 20, bottom: 20, left: 80 };
  var width = $("#treeword-plot").width() - 50;
  var height = 500 - margin.top - margin.bottom;
  var duration = d3.event && d3.event.altKey ? 5000 : 500;
  var i = 0;

  var root = data;
      root.x0 = height / 2;
      root.y0 = 0;

  var tree = d3.layout.tree()
                      .size([height, width]);

  var diagonal = d3.svg.diagonal()
                       .projection(d => [d.y, d.x]);

  var svg = d3.select("#treeword-plot")
              .append("svg")
                .attr("width", width + margin.right + margin.left)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", "translate(150," +
                      margin.top + ")");

  root.children.forEach(toggleAll);
  update(root);

  function update(data) {
    var nodes = tree.nodes(root).reverse();

    nodes.forEach(d => d.y = d.depth == 2 ? d.depth * 200 : d.depth * 100);

    var node = svg.selectAll("g.node")
                  .data(nodes, d => d.id || (d.id = ++i));

    var nodeEnter = node.enter()
                        .append("g")
                        .attr("class", "node")
                        .attr("transform", "translate(" + data.y0 + "," + data.x0 + ")")
                        .on("click", function(d) {
                            toggle(d);
                            update(d);
                        });

    nodeEnter.append("circle")
             .attr("r", 0)
             .style("fill", d => d._children ? "#5c97bf" : "#fff");

    nodeEnter.append("text")
             .attr("class", d => d.children || d._children ? "tree-root" : "tree-leaf")
             .attr("x", d => d.children || d._children ? -10 : 10)
             .attr("dy", ".35em")
             .attr("text-anchor", d => d.children || d._children ? "end" : "start")
             .text(d => d.name)
             .style("fill-opacity", 0)
             .style("fill", d => d.children || d._children ? color : "#000");

    var nodeUpdate = node.transition()
                         .duration(duration)
                         .attr("transform", d => "translate(" + d.y + "," + d.x + ")");

    nodeUpdate.select("circle")
              .attr("r", 4.5)
              .style("fill", d => d._children ? "#5c97bf" : "#fff");

    nodeUpdate.select("text")
              .style("fill-opacity", 1);

    var nodeExit = node.exit()
                       .transition()
                       .duration(duration)
                       .attr("transform", "translate(" + data.y + "," + data.x + ")")
                       .remove();

    nodeExit.select("circle")
            .attr("r", 0);

    nodeExit.select("text")
            .style("fill-opacity", 0);

    var link = svg.selectAll("path.link")
                  .data(tree.links(nodes), d => d.target.id);

    link.enter()
        .insert("path", "g")
          .attr("class", "link")
          .attr("d", function(d) {
            var o = {x: data.x0, y: data.y0};
            return diagonal({source: o, target: o});
          })
        .transition()
          .duration(duration)
          .attr("d", diagonal);

    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    link.exit()
        .transition()
        .duration(duration)
        .attr("d", function(d) {
          var o = {x: data.x, y: data.y};
          return diagonal({source: o, target: o});
        })
        .remove();

    nodes.forEach(function(d) {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }

  function toggle(d) {
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else {
      d.children = d._children;
      d._children = null;
    }
  }

  function toggleAll(d) {
    if (d.children) {
      d.children.forEach(toggleAll);
      toggle(d);
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

  // main(data[0], "#27ae60")
  // main(data[1], "#8e44ad")
  main(data, "#8e44ad")
});
