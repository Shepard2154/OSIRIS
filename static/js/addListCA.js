addListCa = function() {
    var NewListCaName = $("#ListCaName").val()
    if (NewListCaName == null || NewListCaName == "") {
        txt = "Отсутствует название";
      } else {

            caBoard = document.getElementsByClassName('causer')
            sze = Object.keys(caBoard).length
            if (sze > 0) {
                var CaNames = []
                for (var i = 0; i < sze; i++) {
                    CaNames[i] = caBoard[i].id
                  }
                
              }
            datta = String('{"NewListCaName":"'+NewListCaName+'","CaNames":"'+CaNames+'"}')
            $.ajax({
                type: "POST",
                url: "/addListCa/",
                contentType:false,
                dataType: "json",
                data: datta,
                success: function(msg) {
                    alert("Успешно")
                },
                error: function(msg) {
                    alert('bad request')
            }
          });
       }
    }