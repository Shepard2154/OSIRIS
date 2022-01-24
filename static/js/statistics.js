statUpdate = function() {
    all_followers = document.getElementsByName('acc_followers_count')
    all_following = document.getElementsByName('acc_following_count')
    // all_border = document.getElementsByName('border_color')
    countt = 0
    sizze = Object.keys(all_followers).length
    // alert(all_followers[0].innerHTML)
    for (var i = 0; i < sizze; i++) {
        count_followers_one = parseInt(all_followers[i].innerHTML)
        countt = countt + count_followers_one;
        // alert('oke__________ke')
    }
    // sizze2 = Object.keys(all_border).length
    // alert(sizze2)
    $("#stat_followers_count").html(countt)
    $("#stat_acc_count").html(sizze)

    $('#stat_loadtime_count').html(sec2time(countt * 0.013646371))
    // aa = now + dd
    // $('#stat_loadtime_count').html(aa.toLocaleString("ru", options))

    $("#volume").attr("min","1")
    $("#volume").attr("max",sizze)
    $("#volume").attr("value","1")
    $("#volume").val("1") 
    $('#stat_cross_count').html("1")

    

}

function sec2time(timeInSeconds) {
    var pad = function(num, size) { return ('000' + num).slice(size * -1); },
    time = parseFloat(timeInSeconds).toFixed(3),
    days = Math.floor(time / 60 / 60 / 24)
    hours = Math.floor(time / 60 / 60),
    minutes = Math.floor(time / 60) % 60,
    seconds = Math.floor(time - minutes * 60)
    if (days == 0){
        if (hours == 0) {
            if (minutes == 0){
                return pad(seconds, 2) + ' сек.';
            }
            return pad(minutes, 2) + ' мин. ' + pad(seconds, 2) + ' сек.'; 
        }
        return pad(hours, 2) + ' ч. ' + pad(minutes, 2) + ' мин. ' + pad(seconds, 2) + ' сек.'; 
    }
    return pad(days, 3) + ' дн. ' + pad(hours, 2) + ' ч. ' + pad(minutes, 2) + ' мин.'; 
}