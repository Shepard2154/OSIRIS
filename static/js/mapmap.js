// This example requires the Drawing library. Include the libraries=drawing
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=drawing">
var rectangle = null;
function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 41.391771, lng: -73.962449}, 
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });    
  
    var drawingManager = new google.maps.drawing.DrawingManager({
    //   drawingMode: google.maps.drawing.OverlayType.MARKER,
      drawingControl: true,
      drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: ['circle']
      }
    });
    drawingManager.setMap(map);
    google.maps.event.addDomListener(drawingManager, 'overlaycomplete', function(event) {
        if(event.type == google.maps.drawing.OverlayType.CIRCLE) {
          // any other 'rectangle' on the map is removed
          if(rectangle != null)
            rectangle.setMap(null);
            $('#twitter tbody').empty();
          rectangle = event.overlay
        }
      });
      

    google.maps.event.addListener(drawingManager, 'circlecomplete', function(circle) {
        // alert(circle.getCenter());
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
                        addGeofenceTwit(msg.twits[i]);
                  // alert('oke__________ke')
                    }
                    // $('#untilTwitsToBoard').val(msg.TwitsToBoard[sizze-1]['created_at'])
                }
                $("#geogeo").attr("style","visibility:view")
                // alert(sizze)
            },
            error: function(msg) {
                // $("#login").attr("style","color:red")
                // $("#password").attr("style","color:red")
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
        // alert(circle.getRadius()/1000);
        // alert(circle.getCenter());

      });
    
  }
  