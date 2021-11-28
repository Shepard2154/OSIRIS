getTwits = function () {
    var accountName = $('#anzlyzeInput').val();
    var until = $('#untilTwits').val();
    var since = $('#sinceTwits').val();
    if (accountName != "") {
        datta = String('{"accountName":"'+accountName+'","until":"'+until+'","since":"'+since+'"}')
        $.ajax({
            type: "POST",
            url: "/getTwits/",
            contentType:false,
            dataType: "json",
            data: datta,
            success: function(msg) {
                $("#analyzeButton").click()
            },
            error: function(msg) {
                alert('bad request')
            },
            beforeSend: function(){
              $("#overlay").fadeIn(300);
              disableScroll()
          },
         complete: function(){
         }
          });
    }
  }