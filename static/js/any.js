renDeringCloud = function (Ca) {
    $("#container1").html("")

    var data = Ca.out_pos
  
    var chart = anychart.tagCloud(data);
    chart.title('Positive')
    chart.fromAngle(-35);
    chart.toAngle(25);
    chart.anglesCount(5);
    chart.mode("spiral");

    var customColorScale = anychart.scales.ordinalColor();
   
    customColorScale.colors(["#00C322"]);
    
    chart.colorScale(customColorScale);


  
    // format tooltips
    var formatter = "{%value}{scale:(1)(1000)(1000)(1000)|()( thousand)( million)( billion)}";
    var tooltip = chart.tooltip();
    tooltip.format(formatter);
  
    // add an event listener
    chart.listen("pointClick", function(e){
      // alert(e.point.get("x"))
      // alert()
      $("#overlay_pop_up_text").html("")
      mass = Ca.out.names_sent_pos[String(e.point.get("x"))]
      sze = Object.keys(mass).length
      for (var i = 0; i < sze; i++) {
        $("#overlay_pop_up_text").html($("#overlay_pop_up_text").html() + "<p>"+mass[i]+"</p>"+'<hr size="2" color="#ff0000" align="center">')
      }
      $("#overlay_pop_up").attr("style","display: inline;")
      // var url = "https://en.wikipedia.org/wiki/" + e.point.get("x");
      // window.open(url, "_blank");
    });
    
    // display chart
    chart.container("container1");
    chart.draw();

    $("#container2").html("")

    var data = Ca.out_neutral
  
    // create a tag cloud chart
    var chart = anychart.tagCloud(data);
  
    // set the chart title
    chart.title('Neutral')
    // set array of angles, by which words will be placed
    // chart.angles([0, -45, 90])
    // enable color range
    // chart.colors();
    chart.fromAngle(-30);
    chart.toAngle(30);
    chart.anglesCount(5);
    chart.mode("spiral");

    var customColorScale = anychart.scales.ordinalColor();
    // customColorScale.names([
    //     'pos',
    //     'neutral',
    //     'neg'
    // ]);
    customColorScale.colors(["#00b8e6"]);
    
    // set the color scale as the color scale of the chart
    chart.colorScale(customColorScale);
    // chart.colorRange(true);
    // set color range length
    // chart.colorRange().length('80%');
    // chart.legend(true);
    // chart.colorRange()

  
    // format tooltips
    var formatter = "{%value}{scale:(1)(1000)(1000)(1000)|()( thousand)( million)( billion)}";
    var tooltip = chart.tooltip();
    tooltip.format(formatter);
  
    // add an event listener
    chart.listen("pointClick", function(e){
      // alert()
      $("#overlay_pop_up_text").html("")
      mass = Ca.out.names_sent_neutral[String(e.point.get("x"))]
      sze = Object.keys(mass).length
      for (var i = 0; i < sze; i++) {
        $("#overlay_pop_up_text").html($("#overlay_pop_up_text").html() + "<p>"+mass[i]+"</p>"+'<hr size="2" color="#ff0000" align="center">')
      }
      $("#overlay_pop_up").attr("style","display: inline;")

    });
  
    // display chart
    chart.container("container2");
    chart.draw();

    $("#container3").html("")

    var data = Ca.out_neg
  
    // create a tag cloud chart
    var chart = anychart.tagCloud(data);
  
    // set the chart title
    chart.title('Negative')
    // set array of angles, by which words will be placed
    // chart.angles([0, -45, 90])
    // enable color range
    // chart.colors();
    chart.fromAngle(-25);
    chart.toAngle(35);
    chart.anglesCount(5);
    chart.mode("spiral");

    var customColorScale = anychart.scales.ordinalColor();
    // customColorScale.names([
    //     'pos',
    //     'neutral',
    //     'neg'
    // ]);
    customColorScale.colors(["#ff4d4d"]);
    
    // set the color scale as the color scale of the chart
    chart.colorScale(customColorScale);
    // chart.colorRange(true);
    // set color range length
    // chart.colorRange().length('80%');
    // chart.legend(true);
    // chart.colorRange()

  
    // format tooltips
    var formatter = "{%value}{scale:(1)(1000)(1000)(1000)|()( thousand)( million)( billion)}";
    var tooltip = chart.tooltip();
    tooltip.format(formatter);
  
    // add an event listener
    chart.listen("pointClick", function(e){
      // alert()
      $("#overlay_pop_up_text").html("")
      mass = Ca.out.names_sent_neg[String(e.point.get("x"))]
      sze = Object.keys(mass).length
      for (var i = 0; i < sze; i++) {
        $("#overlay_pop_up_text").html($("#overlay_pop_up_text").html() + "<p>"+mass[i]+"</p>"+'<hr size="2" color="#ff0000" align="center">')
      }
      $("#overlay_pop_up").attr("style","display: inline;")

    });
  
    // display chart
    chart.container("container3");
    chart.draw();
  }