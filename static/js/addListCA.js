addListCa = function() {
    var NewListCaName = $("#ListCaName").val()
    if (NewListCaName == null || NewListCaName == "") {
        txt = "Отсутствует название";
      } else {

            caBoard = document.getElementsByClassName('causer')
            sze = Object.keys(caBoard).length
            if (sze > 0) {
                var CaNames = []
                // $("#geofenceBoard").html("")
                for (var i = 0; i < sze; i++) {
                    CaNames[i] = caBoard[i].id
                    // alert('oke__________ke')
                  }
                
              }
            // alert(CaNames)

            datta = String('{"NewListCaName":"'+NewListCaName+'","CaNames":"'+CaNames+'"}')
            $.ajax({
                type: "POST",
                url: "/addListCa/",
                contentType:false,
                dataType: "json",
                data: datta,
                success: function(msg) {
                    // window.location.replace("/");
                    //$(".dropdownhidden_demo2").html($(".dropdownhidden_demo2").html()+"<li><a href='#'>"+NewListInfluencersName+"</a></li>")
                    
                    alert("Успешно")
                    // $("#analyzeButton").click()
                    // alert('success_data_load')
                },
                error: function(msg) {
                    alert('bad request')
            }
          });
       }
    }