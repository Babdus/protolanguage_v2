var path = "../data/generated/tree.json"
    d3.json(path, function(error, data) {
        var width = 900,
            height = 900,
            nodeRadius = 4;

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
            .size([360, radius - 120]);

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
//                d: linksGenerator,
                d: function(d) {
                    sx = d.source.y * Math.cos((d.source.x - 90) / 180 * Math.PI)
                    sy = d.source.y * Math.sin((d.source.x - 90) / 180 * Math.PI)
                    tx = d.target.y * Math.cos((d.target.x - 90) / 180 * Math.PI)
                    ty = d.target.y * Math.sin((d.target.x - 90) / 180 * Math.PI)
                    ax = d.source.y * Math.cos((d.target.x - 90) / 180 * Math.PI)
                    ay = d.source.y * Math.sin((d.target.x - 90) / 180 * Math.PI)
                    if(d.source.x > d.target.x)
                        return "M" + sx + " " + sy + " " + "A" + d.source.y + " " + d.source.y + " 0 0 0 " + ax + " " + ay + "L" + tx + " " + ty;
                    else
                        return "M" + tx + " " + ty + " " + "L" + ax + " " + ay + "A" + d.source.y + " " + d.source.y + " 0 0 0 " + sx + " " + sy;
                },
                fill: 'none',
                stroke: '#ccc',
                'stroke-width': 3
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
            .text(function(d) { return d.data.children.length == 0 ? d.data.name : '' });
    });