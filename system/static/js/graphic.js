/**
 * Created by shibatanaoto on 2016/03/07.
 */

window.addEventListener("load", function(){
    var canvas = d3.select("div.link");
    var svg = canvas.append("svg")
        .attr("width",600)
        .attr("height",800)
        .attr("viewBox", "0,-25,200,200");
    query_params = {site_id: 2};
    base_url = [location.protocol, '/', location.host, "django.cgi", "link.json"].join('/');
    http_url = [base_url, $.param(query_params)].join('?');
    var data = JSON.parse(sync_communicate_http(http_url));
    var tree = d3.layout.tree().size([200,150]);
    //階層構造をとるデータからデータの配列を生成する．
    //生成されたデータにはparent,children,depth,x,yと言ったパラメータが付加される．
    var nodes = tree.nodes(data);
    svg.selectAll("path")
        .data(tree.links(nodes))    //リンク情報を取得
        .enter().append("path")
        .attr("d", d3.svg.diagonal())   //ノード間を絆ぐ
        .attr("fill", "none")
        .attr("stroke", "lightgray")
        .attr("stroke-width", "2");
    svg.selectAll("circle")
        .data(nodes).enter().append("circle")
        .attr("cx", function(d){return d.x})
        .attr("cy", function(d){return d.y})
        .attr("r", 15)
        .on("mouseover", function(d){return mouseover(d, this);})
        .on("mouseout", mousedown)
        .style("fill", "white")
        .style("stroke", function(d){return d.name == "root" ? "red":"blue";})
        .style("stroke-width", 2);
    svg.selectAll("text")
        .data(nodes).enter().append("text")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .attr("text-anchor", "middle")
        .attr("font-size", 2)
        .attr("font-family", "sans-serif")
        .text(function(d){return d.title})
        .style("fill", "black");
    //svg.selectAll("div")
    //    .data(nodes).enter().append("text")
    //    .attr("x", function(d){return d.x})
    //    .attr("y", function(d){return d.y + 7})
    //    .attr("text-anchor", "middle")
    //    .attr("font-size", 2)
    //    .attr("font-family", "sans-serif")
    //    .text(function(d){return d.url;})
    //    .style("fill", "black");
},false);

function mouseover(data, sel){

    if (data.name == "root") {
        d3.select(sel).style("fill", "red");
    } else {
        d3.select(sel).style("fill", "blue");
    }

    var keys = Object.keys(data);
    dataset = [];
    for(var i=0; i<keys.length; i++)
    {
      if (keys[i] != "children" && keys[i] != "x" && keys[i] != "y" && keys[i] != "depth" && keys[i] != "parent")
      {
        tmp = {
            column: keys[i],
            value: data[keys[i]]
        };
        dataset.push(tmp);
      }
    }

    var tbody = d3.select("div#table")
        .append('table')
        .attr("class", "table")
        .attr("id", "table")
        .attr("border", "3.5")
        .append('tbody');
    tbody.selectAll("tr")
        .data(dataset).enter()
        .append("tr")
        .append("th")
        .attr("id", "link")
        .text(function(d){
            return d.column;
        });
    var tr = tbody.selectAll("tr");
    tr.data(dataset).append("td").text(function(d){
       return d.value;
    });
}

function mousedown(){
    d3.select(this).style("fill", "white");
    $('table').remove();
}

function sync_communicate_http(url){
    //$.ajax({
    //      url: url,
    //      dataType: 'json',
    //      async: true,
    //      complete: function(data){
    //        var data_json = data.responseText;
    //        console.log(data_json);
    //        return data_json;
    //      }
    //});
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}
