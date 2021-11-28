downloadFollowers = function(){
    var selection = document.getElementById('selection123')
    if (selection.value != "Выберите группу") {
        datta = String('{"ListInfluencersName":"'+selection.value+'"}')
        $.ajax({
            type: "POST",
            url: "/downloadFollowers/",
            contentType:false,
            dataType: "json",
            data: datta,
            timeout:1500000000,
            success: function(msg) {
                $("#filterFollowers").attr("style","visibility: true;")
                alert("all_good")
            },
            error: function(msg) {
                // $("#login").attr("style","color:red")
                // $("#password").attr("style","color:red")
                console.log(msg)
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