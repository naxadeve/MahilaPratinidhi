class HStackedChart extends React.Component{
  constructor(props){
    super(props)
    this.hstackedChart = this.hstackedChart.bind(this);
  }

  componentDidMount(){
    //alert("component did mont" +this.props.data[0].dataName)

    this.hstackedChart(this.props.data[0].data, this.props.data[0].dataName);

  }

  componentWillReceiveProps(nextProps){
    alert("component did receive");
    d3.selectAll('.stacked-bar').selectAll("*").remove();
    this.hstackedChart(nextProps.data[0].data,nextProps.data[0].dataName);
  }

  hstackedChart(data,dataName,variable_colors){

    console.log("rawdata",data)

     data = data.sort(function (a, b) {
       console.log("a",a);
       console.log("b",b);
         //return d3.ascending(+a.total, +b.total);
     });


    if (dataName== "party"){


        var legend_array =["Communist Party of Nepal","Nepali Congress","Federal Socialist Forum",
        "Rastriya Janata Party Nepal"];
        var count = 2;
    }

    else if(dataName== "provincial") {

        var legend_array= ["1","2","3","4","5","6","7"];
        count =0;
    }

    else if (dataName== "vs") {

        var legend_array= ["province", "federal", "national"];
        count =1;

    }



  var margin = {top: 20, right: 170, bottom: 50, left: 130};

  var width = 700 - margin.left - margin.right,
      height = 550 - margin.top - margin.bottom;

  var svg = d3.selectAll(".hstacked-bar").filter(function(d,i){
    return i === count;
  })
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    //var parse = d3.time.format("%Y").parse;

//["redDelicious", "mcintosh", "oranges", "pears"]
    // Transpose the data into layers


    var dataset = d3.layout.stack()(legend_array.map(function(fruit) {
      return data.map(function(d) {
        return {x: d.label, y: +d[fruit]};
      });
    }));

    console.log("datasetttt",dataset)

    var y = d3.scale.ordinal()
      .domain(dataset[0].map(function(d) { return d.x; }))
      .rangeRoundBands([10, height-10], 0.02);

      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickPadding([0.6])



        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis);

    var x = d3.scale.linear()
      .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
      .range([0,width]);

      var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(6)
        .tickSize(-height, 0, 0)
        .tickFormat( function(d) { return d } );


        svg.append("g")
          .attr("class", "x-axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);



    var colors = [	 "#69131a","#e86c75","#faa2ad","#ac779d","#4b1b31" ,"#f441a6","#f44141"];
    var default_colors =["#ff6367","#98b000","#00cc7a","#00a5f9","#fb00f6","#f441a6","#f44141"];

    var colors = variable_colors || default_colors;

    var groups = svg.selectAll("g.cost")
      .data(dataset)
      .enter().append("g")
      .attr("class", "cost")
      .style("fill", function(d, i) { return colors[i]; });


      var rect = groups.selectAll("rect")
        .data(function(d) { return d; })
        .enter()
        .append("rect")
        .attr("y", function(d) { return y(d.x); })
        .attr("x", function(d) { return x(d.y0); })
        .attr("width", function(d) { return  x(d.y0 + d.y) -x(d.y0) ; })
        .attr("height", y.rangeBand())


        var legend = svg.selectAll(".legend")
          .data(colors.slice(0,legend_array.length))
          .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });

        legend.append("rect")
          .attr("x", width - 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", function(d, i) {return colors.slice()[i];});

        legend.append("text")
          .attr("x", width + 5)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "start")
          .style("fill","white")
          .style("font-size","xx-small")
          .text(function(d, i) {
            switch (i) {
              case 0: return legend_array[0];
              case 1: return legend_array[1];
              case 2: return legend_array[2];
              case 3: return legend_array[3];
              case 4: return legend_array[4];
              case 5: return legend_array[5];
              case 6: return legend_array[6];
              case 7: return legend_array[7];

            }
          });



  } //end of function

  render(){

    return(<svg className="hstacked-bar" />);
  }



} //end of class
