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
                alert(msg.ListsInfluencers)
                document.location.reload();
            },
            error: function(msg) {
                alert('bad request')
            }
          });
       }
    }