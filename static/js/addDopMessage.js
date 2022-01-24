addDopMessage = function () {
    var accountName = $('#anzlyzeInput').val();
    var created_at = $('#untilTwitsToBoard').val();
    if (accountName != "") {
        datta = String('{"accountName":"'+accountName+'","created_at":"'+created_at+'"}')
        $.ajax({
            type: "POST",
            url: "/addDopMessage/",
            contentType:false,
            dataType: "json",
            data: datta,
            success: function(msg) {
                sizze = Object.keys(msg.TwitsToBoard).length
                if (sizze > 0) {
                    for (var i = 0; i < sizze; i++) {
                        addMessageOnBoard(msg.TwitsToBoard[i]);
                    }
                    $('#untilTwitsToBoard').val(msg.TwitsToBoard[sizze-1]['created_at'])
                }
            },
            error: function(msg) {
                if (msg.responseJSON.error == "TwitsToBoard not found") alert('Твиты не найдены! Вы анализировали пользователя через Персоны?')
                else alert('bad request')
            },
            beforeSend: function(){
              $("#overlay").fadeIn(300);
              disableScroll()
          },
         complete: function(){
          $("#overlay").fadeOut(300);
          enableScroll()
         }
})}}