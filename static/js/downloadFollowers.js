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

                $('#start_person').val(0)
                $('#end_person').val(20)
                console.log('donwloadFollowers - start of all', $('#start_person').val(), typeof($('#start_person').val()), $('#end_person').val())
            },
            error: function(msg) {
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