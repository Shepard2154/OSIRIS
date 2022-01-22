downloadFullFollowers = function(){
    var selection = document.getElementById('selection123')
    var crossCount = $('#stat_cross_count').html()
    var start_person = $('#start_person').val()
    var end_person = $('#end_person').val()

    console.log('downloadFullFolllowers - start ', start_person, end_person)

    if (selection.value != "Выберите группу") {
        datta = String('{"ListInfluencersName":"'+selection.value+'","crossCount":"'+crossCount+'", "start_person":"'+start_person+'", "end_person":"'+end_person+'"}')
        $.ajax({
            type: "POST",
            url: "/downloadFullFollowers/",
            contentType:false,
            dataType: "json",
            data: datta,
            timeout:1500000000,
            success: function(msg) {
                $("#fullFollowers").attr("style","visibility: true;")
                sizze = Object.keys(msg.ListInfluencersNames).length
                if (sizze > 0) {
                    for (var i = 0; i < sizze; i++) {
                        addCAuserOnBoard(msg.ListInfluencersNames[i]);
                    }
                }

                $('#start_person').val(parseInt(start_person) + 20)
                $('#end_person').val(parseInt(end_person) + 20)
                console.log('downloadFullFolllowers - end ', $('#start_person').val(), $('#end_person').val())
            },
            error: function(msg) {
                if (msg.responseJSON.error == "Followers don't exist") alert('Подписчики закончились!')
                else alert('bad request')
            },
            beforeSend: function(){
              $("#overlay").fadeIn(300)
              disableScroll()
          },
         complete: function(){
          $("#overlay").fadeOut(300)
          enableScroll()
         }
          })
       }
    }