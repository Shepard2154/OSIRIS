uploadGeoTweets = function(){
    var start_tweet = $('#start_tweet').val()
    var end_tweet = $('#end_tweet').val()

    $('#start_tweet').val(parseInt(start_tweet) + 20)
    $('#end_tweet').val(parseInt(end_tweet) + 20)

    var start_tweet = $('#start_tweet').val()
    var end_tweet = $('#end_tweet').val()

    console.log('uploadGetTweets - start ', start_tweet, end_tweet)

    datta = String('{"start_tweet":"'+start_tweet+'", "end_tweet":"'+end_tweet+'"}')
    $.ajax({
        type: "POST",
        url: "/uploadGeoTweets/",
        contentType: false,
        dataType: "json",
        data: datta,
        timeout: 1500000000,
        success: function(msg) {
            sizze = Object.keys(msg.twits).length
            if (sizze > 0) {
                for (var i = 0; i < sizze; i++) {
                    addGeofenceTwit(msg.twits[i])
                }
            }

            console.log('uploadGetTweets - end ', $('#start_tweet').val(), $('#end_tweet').val())
        },
        error: function(msg) {
            if (msg.responseJSON.error == "There are not geotweets"){
                $('#start_tweet').val(parseInt(0))
                $('#end_tweet').val(parseInt(20))
                alert('Геотвиты закончились!')
            } 
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