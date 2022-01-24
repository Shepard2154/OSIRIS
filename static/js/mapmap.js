var rectangle = null;
function initMap() {
  $('#start_tweet').val(parseInt(0))
  $('#end_tweet').val(parseInt(20))

    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 41.391771, lng: -73.962449}, 
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });    
  
    var drawingManager = new google.maps.drawing.DrawingManager({
      drawingControl: true,
      drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: ['circle']
      }
    });
    drawingManager.setMap(map);
    google.maps.event.addDomListener(drawingManager, 'overlaycomplete', function(event) {
        if(event.type == google.maps.drawing.OverlayType.CIRCLE) {
          if(rectangle != null)
            rectangle.setMap(null);
            $('#twitter tbody').empty();
          rectangle = event.overlay
        }
      });
      

    google.maps.event.addListener(drawingManager, 'circlecomplete', function(circle) {
        datta = String('{"center":"'+circle.getCenter()+'","radius":"'+circle.getRadius()/1000+'"}')
        $.ajax({
            type: "POST",
            url: "/addGeofenceOnBoard/",
            contentType:false,
            dataType: "json",
            data: datta,
            success: function(msg) {
                sizze = Object.keys(msg.twits).length
                if (sizze > 0) {
                    $("#geofenceBoard").html("")
                    for (var i = 0; i < sizze; i++) {
                        addGeofenceTwit(msg.twits[i])
                    }
                }
                $("#geogeo").attr("style","visibility:view")
            },
            error: function(msg) {
                alert('bad request')
            },
            beforeSend: function(){
              $("#overlay").fadeIn(300);
              disableScroll()
          },
         complete: function(){
          $("#overlay").fadeOut(300);
          enableScroll()
         }
        });
      });
    
  }
  