var path = "../data/generated/tree.json"
    d3.json(path, function(error, data) {
        var width = 900,
            height = 900,
            nodeRadius = 8;

        var svg = d3.select('body')
            .append('svg')
            .attrs({
                width: width,
                height: height
            });

        var radius = width / 2;
        var mainGroup = svg.append('g')
            .attr("transform", "translate(" + radius + "," + radius + ")");

        var cluster = d3.cluster()
            .size([360, radius - 100]);

        //  assigns the data to a hierarchy using parent-child relationships
        var root = d3.hierarchy(data, function(d) {
            return d.children;
        });

        cluster(root);

        var linksGenerator = d3.linkRadial()
            .angle(function(d) { return d.x / 180 * Math.PI; })
            .radius(function(d) { return d.y; });

        mainGroup.selectAll('path')
            .data(root.links())
            .enter()
            .append('path')
            .attrs({
                d: linksGenerator,
                fill: 'none',
                stroke: '#ccc',
            });

        var nodeGroups = mainGroup.selectAll("g")
            .data(root.descendants())
            .enter()
            .append("g")
            .attr("transform", function(d) {
                return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")";
            });

        nodeGroups.append("circle")
            .attrs({
                r: nodeRadius,
                fill: '#fff',
                stroke: 'steelblue',
                'stroke-width': 3
            });

        nodeGroups.append("text")
            .attrs({
                dy: ".31em",
                dx: function(d) {
                    return d.x < 180 ? ".31em" : "-.31em";
                },
                'text-anchor': function(d) {
                    return d.x < 180 ? "start" : "end";
                },
                'transform': function(d) {
                    return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)";
                }
            })
            .style('font', '14px sans-serif')
            .style('margin', '5px')
            .text(function(d) { return d.data.children.length == 0 ? d.data.name : '' });
    });