addNewListInfluencers = function() {
    var NewListInfluencersName = prompt("Введите название для нового списка:");
    if (NewListInfluencersName == null || NewListInfluencersName == "") {
        txt = "Отсутствует название";
      } else {
        datta = String('{"NewListInfluencersName":"'+NewListInfluencersName+'"}')
        $.ajax({
            type: "POST",
            url: "/addNewListInfluencers/",
            contentType:false,
            dataType: "json",
            data: datta,
            success: function(msg) {
                // window.location.replace("/");
                //$(".dropdownhidden_demo2").html($(".dropdownhidden_demo2").html()+"<li><a href='#'>"+NewListInfluencersName+"</a></li>")
                
                alert(msg.ListsInfluencers)
                // $("#analyzeButton").click()
                // alert('success_data_load')
            },
            error: function(msg) {
                // $("#login").attr("style","color:red")
                // $("#password").attr("style","color:red")
                alert('bad request')
            }
          });
       }
    }