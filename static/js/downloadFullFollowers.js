downloadFullFollowers = function(){
    var selection = document.getElementById('selection123')
    var crossCount = $('#stat_cross_count').html()
    // alert(crossCount)
    // alert(crossCount.value)
    // alert(crossCount.html())
    if (selection.value != "Выберите группу") {
        datta = String('{"ListInfluencersName":"'+selection.value+'","crossCount":"'+crossCount+'"}')
        $.ajax({
            type: "POST",
            url: "/downloadFullFollowers/",
            contentType:false,
            dataType: "json",
            data: datta,
            timeout:1500000000,
            success: function(msg) {
                $("#caBoard").html("")
                $("#fullFollowers").attr("style","visibility: true;")
                // alert("all_good")
                sizze = Object.keys(msg.ListInfluencersNames).length
                if (sizze > 0) {
                    for (var i = 0; i < sizze; i++) {
                        addCAuserOnBoard(msg.ListInfluencersNames[i]);
                  // alert('oke__________ke')
                    }
                }
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
       }
    }