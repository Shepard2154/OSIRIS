removeUserFromList = function(accountName) {
    // var accountName = $('#addUserToListInput').val();
    // accountName = accountName.val()
    // alert(accountName)
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
                // alert('success_remove22')
                $('#'+accountName).remove()
                // window.location.replace("/");
                //$(".dropdownhidden_demo2").html($(".dropdownhidden_demo2").html()+"<li><a href='#'>"+NewListInfluencersName+"</a></li>")
                statUpdate()
                //alert(msg.status_code)
                // $("#imageEmptyList").remove()
                // $('#addUserToListInput').val("")
                // addPersonOnBoard(msg.Influencer)
                // $("#section2").attr("style","visibility: true;")
                // alert('success_remove')
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