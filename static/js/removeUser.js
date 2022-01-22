removeUserFromList = function(accountName) {
    var selection = document.getElementById('selection123')
    if ((accountName != "") && (selection.value != "Выберите группу")) {
        datta = String('{"accountName":"'+accountName+'","ListInfluencersName":"'+selection.value+'"}')
        $.ajax({
            type: "POST",
            url: "/removeUserFromList/",
            contentType:false,
            dataType: "json",
            data: datta,
            success: function(msg) {
                $('#'+accountName).remove()
                statUpdate()
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
       }
    }