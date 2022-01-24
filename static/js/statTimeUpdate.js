statTimeUpdate = function() {
    cross_count = parseInt($('#volume').val())
    // followers_count = parseInt($("#stat_followers_count").html())
    if (cross_count == 0) {
        cross_count = 1
    } 
    $('#stat_cross_count').html(cross_count)
    // alert(cross_count)
    var selection = document.getElementById('selection123')
    if (selection.value != "Выберите группу") {
        datta = String('{"cross_count":"'+cross_count+'","ListInfluencersName":"'+selection.value+'"}')
        $.ajax({
            type: "POST",
            url: "/statTimeUpdate/",
            contentType:false,
            dataType: "json",
            data: datta,
            success: function(msg) {
                countt = msg.followersCross
                $("#stat_followers_count2").html(countt)
                // $("#stat_loadtime_count2").html(sec2time(countt * 1.6))                
                // alert(countt)
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

statTimeUpdate2 = function() {
    // alert("lol");
    twit_count = parseInt($('#volume').val())
    ca_count = parseInt($("#stat_ca_count").html())
    // followers_count = parseInt($("#stat_followers_count").html())

    $('#stat_twit_count').html(twit_count)
    // alert(twit_count)
    var selection = document.getElementById('selection123123')
    if (selection.value != "Выберите группу") {        
        // alert(twit_count)
        // alert(ca_count)

        $("#stat_loadtime_count3").html(sec2time(twit_count * 0.14 * ca_count))
        }
    }