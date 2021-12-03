getTwits = function () {
    var accountName = document.getElementById("acc_username").innerHTML.slice(1)
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
                document.getElementById('anzlyzeInput').value = accountName;
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