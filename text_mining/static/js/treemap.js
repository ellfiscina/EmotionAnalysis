function main(root) {
  var margin = { top: 40, right: 0, bottom: 0, left: 0 };
  var width = $("#tree-plot").width() - 50;
  var height = 650;
  var transitioning;

  var x = d3.scale
            .linear()
            .domain([0, width])
            .range([0, width]);

  var y = d3.scale
            .linear()
            .domain([0, height])
            .range([0, height]);

  var treemap = d3.layout.treemap()
                         .value(d => d.value)
                         .children((d, depth) => depth ? null : d._children)
                         .sort((a, b) => a.value - b.value)
                         .ratio(height / width * 0.5 * (1 + Math.sqrt(5)))
                         .round(false);

  var svg = d3.select("#tree-plot")
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.bottom + margin.top)
                .style("margin-left", -margin.left + "px")
                .style("margin.right", -margin.right + "px")
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                .style("shape-rendering", "crispEdges");

  var div = d3.select("#tree-plot")
              .append("div")
              .attr("class", "tooltip")
              .style("opacity", 0);

  var grandparent = svg.append("g")
                       .attr("class", "grandparent");

  grandparent.append("rect")
             .attr("y", -margin.top)
             .attr("width", width)
             .attr("height", margin.top);

  grandparent.append("text")
             .attr("x", 6)
             .attr("y", 10 - margin.top)
             .attr("dy", ".75em");

  initialize(root);
  accumulate(root);
  layout(root);
  display(root);

  function initialize(root) {
    root.x = root.y = 0;
    root.dx = width;
    root.dy = height;
    root.depth = 0;
  }

  function accumulate(data) {
    return (data._children = data.children)
        ? data.value = data.children.reduce((p, v) => p + accumulate(v), 0)
        : data.value;
  }

  function layout(data) {
    if (data._children) {
      treemap.nodes({_children: data._children});
      data._children.forEach(function(c) {
        c.x = data.x + c.x * data.dx;
        c.y = data.y + c.y * data.dy;
        c.dx *= data.dx;
        c.dy *= data.dy;
        c.parent = data;
        layout(c);
      });
    }
  }

  function display(data) {
    grandparent.datum(data.parent)
               .on("click", transition_out)
               .select("text")
               .text(data.name + ": "+ data.value + " palavras");

    var g1 = svg.insert("g", ".grandparent")
                .datum(data)
                .attr("class", "depth");

    var g = g1.selectAll("g")
              .data(data._children)
              .enter()
              .append("g");

    g.filter(d => d._children)
     .classed("children", true)
     .on("click", transition_in);

    g.on("mouseover", function(d) {
        div.transition()
           .duration(50)
           .style("opacity", 1)
           .style("height", (d.desc!=null ? (Math.ceil(d.desc.length/75)*19+107) + "px" : "107px"));
        div.html(
          "<br/><br/>"+ d.name.toUpperCase() + "<br/> <br/>" + d.value +
          " palavras (" + percentage(d.value, data.value) + "%)"
          )
           .style("left", Math.max(Math.min((d3.event.pageX - 350),430),20) + "px")
           .style("top", Math.min((d3.event.pageY-70),200) + "px");
        })
      .on("mouseout", function() {
        div.transition()
           .duration(50)
           .style("opacity", 0);
    });

    g.append("rect")
     .attr("class", function(d){
        return d.parent.name == 'Emoções'
          ? "parent " + d.name.toLowerCase()
          : "parent " + d.parent.name.toLowerCase();
      })
     .call(rect)
     .append("title")
     .text(d => d.value);

    g.append("foreignObject")
     .call(rect)
     .attr("class","foreignobj")
     .append("xhtml:div")
     .attr("dy", ".75em")
     .html(function(d) {
        if(parseInt( x(d.x + d.dx) - x(d.x) ) >   50 )
          return d.name + ": "+ percentage(d.value, data.value) + "%";
        else
          return "";
      })
     .attr("class", "textdiv");


    function transition_in(data) {
      if (transitioning || !data) return;
      transitioning = true;

      arrow = grandparent.append("text")
                         .attr('font-family', 'Font Awesome\ 5 Free')
                         .attr("class", "fa fas")
                         .attr("x", width - 50)
                         .attr("y", 25 - margin.top)
                         .text("\uf106")
                         .style("opacity", 0);

      arrow.transition()
           .duration(500)
           .style("opacity", 1);

      g.selectAll(".child")
       .data(d => d.parent._children || [d])
       .enter()
       .append("rect")
       .attr("class", "child")
       .call(rect);

      var g2 = display(data);
      var t1 = g1.transition().duration(750);
      var t2 = g2.transition().duration(750);

      x.domain([data.x, data.x + data.dx]);
      y.domain([data.y, data.y + data.dy]);

      svg.style("shape-rendering", null);

      svg.selectAll(".depth")
         .sort((a, b) => a.depth - b.depth);

      g2.selectAll(".textdiv")
        .style("color", "rgba(0, 0, 0, 0)");

      t1.selectAll("rect").call(rect);
      t2.selectAll("rect").call(rect);

      t1.selectAll(".textdiv").style("display", "block");
      t2.selectAll(".textdiv").style("display", "block");

      g2.transition()
        .delay(650)
        .duration(100)
        .selectAll(".textdiv")
        .style("color", "rgba(0, 0, 0, 1)");

      t1.selectAll(".foreignobj").call(foreign);
      t2.selectAll(".foreignobj").call(foreign);

      t1.remove().each("end", function() {
        svg.style("shape-rendering", "crispEdges");
        transitioning = false;
      });
    }


    function transition_out(data) {
      if (transitioning || !data) return;
      transitioning = true;

      arrow.transition()
           .duration(500)
           .style("opacity", 0  );

      var g2 = display(data),
          t1 = g1.transition().duration(750),
          t2 = g2.transition().duration(750);

      x.domain([data.x, data.x + data.dx]);
      y.domain([data.y, data.y + data.dy]);

      svg.style("shape-rendering", null);

      svg.selectAll(".depth").sort((a, b) => a.depth - b.depth);

      g2.selectAll(".textdiv").style("color", "rgba(0, 0, 0, 0)");

      t1.selectAll("rect").call(rect);
      t2.selectAll("rect").call(rect);

      t1.selectAll(".textdiv").style("display", "block");
      t2.selectAll(".textdiv").style("display", "block");

      g2.transition()
        .delay(650)
        .duration(100)
        .selectAll(".textdiv")
        .style("color", "rgba(0, 0, 0, 1)");

      t1.selectAll(".foreignobj").call(foreign);
      t2.selectAll(".foreignobj").call(foreign);

      t1.remove().each("end", function() {
        svg.style("shape-rendering", "crispEdges");
        transitioning = false;
      });
    }

    return g;
  }

  function rect(rect) {
    rect.attr("x", d => x(d.x))
        .attr("y", d => y(d.y))
        .attr("width", d => x(d.x + d.dx) - x(d.x))
        .attr("height", d => y(d.y + d.dy) - y(d.y))
        .attr("fill", "#eeeeee");
  }

  function foreign(foreign){
    foreign.attr("x", d => x(d.x))
           .attr("y", d => y(d.y))
           .attr("width", d => x(d.x + d.dx) - x(d.x))
           .attr("height", d => y(d.y + d.dy) - y(d.y));
  }

  function percentage(value, total) {
    return +(value/total * 100).toFixed(2);
  }
}

$(document).ready(function() {
 	data = JSON.parse(document.getElementById('data').textContent)
	main(JSON.parse(data))
});
