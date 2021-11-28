analyzze = function () {
  var accountName = $('#anzlyzeInput').val();
  if (accountName != "") {
      datta = String('{"accountName":"'+accountName+'"}')
      $.ajax({
          type: "POST",
          url: "/getInfoAboutTwitterAccountName/",
          contentType:false,
          dataType: "json",
          data: datta,
          success: function(msg) {
              account = msg.accountName
              $("#acc_name").html(account);
              $("#acc_twitter_link").attr("href","https://twitter.com/"+msg.screen_name)
              $("#acc_twitter_link").attr("title","@"+msg.screen_name+"'s Twitter Profile")
              $("#acc_username").html("@" + msg.screen_name)
              $("#acc_username_2").attr("href","https://twitter.com/"+msg.screen_name)
              $("#acc_username_2").attr("title","@"+msg.screen_name+"'s Twitter Profile")
              $("#acc_image").attr("src",msg.profile_image_url)
              $("#acc_image").attr("title","@"+msg.screen_name+"'s Profile Picture")
              $("#acc_image").attr("alt","@"+msg.screen_name+"'s Profile Picture")
              $("#acc_tweet_count").html(msg.tweets)
              $("#acc_tweet_count").attr("href","https://twitter.com/"+msg.screen_name+"/with_replies")
              $("#acc_following_count").html(msg.following)
              $("#acc_following_count").attr("href","https://twitter.com/"+msg.screen_name+"/following")
              $("#acc_followers_count").html(msg.followers)
              $("#acc_followers_count").attr("href","https://twitter.com/"+msg.screen_name+"/followers")
              $("#acc_likes_count").html(msg.likes)
              $("#acc_likes_count").attr("href","https://twitter.com/"+msg.screen_name+"/likes")
              $("#acc_media_count").html(msg.media)
              $("#acc_media_count").attr("href","https://twitter.com/"+msg.screen_name+"/lists/memberships")
              $("#acc_bio").html(msg.description)
              $("#acc_join_date").html(msg.join_date)
              $("#acc_id").html(msg.id)
              $("#acc_link").attr("href","https://twitter.com/"+msg.screen_name)
              $("#acc_link").html("https://twitter.com/"+msg.screen_name)
              $("#acc_location").html(msg.location)

              $("#getTwitsButton").attr('style',"visibility:visible")
              if (msg.countTwits == 0){
                $('#untilTwits').val(false)
                $('#sinceTwits').val(false)
                $("#getTwitsButton").click()
              }
              if (msg.countTwits != 0){
                $("#countTwits").html(msg.countTwits + " Твитов в базе")
                $("#countTwits1").html(msg.countTwits)
                $("#countTwits2").html(msg.countTwits)
                $('#anzlyzeInput').val(msg.name)
                $("#messageBoard").html("")
                
                sizze = Object.keys(msg.TwitsToBoard).length
                if (sizze > 0) {
                  for (var i = 0; i < sizze; i++) {
                    addMessageOnBoard(msg.TwitsToBoard[i]);
                  }
                  $('#untilTwitsToBoard').val(msg.TwitsToBoard[sizze-1]['created_at'])
                }

                ApexCharts.exec('chartAnswers', 'updateOptions', {
                  xaxis: {
                    categories: msg.chartAnswersCategories,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);


                ApexCharts.exec('chartAnswers', 'updateSeries', [{
                  data: msg.chartAnswersCount
                }], true);

                console.log(msg.weekdays_time)

                ApexCharts.exec('chartDayOfWeek', 'updateOptions', {
                  series: msg.weekdays
                }, false, true);
                
                ApexCharts.exec('chartheatmap', 'updateSeries', [
                  {
                    name: 'Вск',
                    data: msg.weekdays_time[0]
                  },
                  {
                      name: 'Сб',
                      data: msg.weekdays_time[6]
                  },
                  {
                      name: 'Пт',
                      data: msg.weekdays_time[5]
                  },
                  {
                      name: 'Чт',
                      data: msg.weekdays_time[4]
                  },
                  {
                      name: 'Ср',
                      data: msg.weekdays_time[3]
                  },
                  {
                      name: 'Вт',
                      data: msg.weekdays_time[2]
                  },
                  {
                      name: 'Пн',
                      data: msg.weekdays_time[1]
                  }
                ], true);

                ApexCharts.exec('chartt', 'updateOptions', {
                  xaxis: {
                    categories: msg.charttDay
                  }
                }, false, true);
                ApexCharts.exec('chartt', 'updateSeries', [{
                  data: msg.charttCount
                }], true);

                ApexCharts.exec('chartHash', 'updateOptions', {
                  xaxis: {
                    categories: msg.chartHashCategories,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);


                ApexCharts.exec('chartHash', 'updateSeries', [{
                  data: msg.chartHashCount
                }], true);

                ApexCharts.exec('chartQuotes', 'updateOptions', {
                  xaxis: {
                    categories: msg.chartCashCategories,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);


                ApexCharts.exec('chartQuotes', 'updateSeries', [{
                  data: msg.chartCashCount
                }], true);

                ApexCharts.exec('chartUrl', 'updateOptions', {
                  xaxis: {
                    categories: msg.chartUrlCategories,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);


                ApexCharts.exec('chartUrl', 'updateSeries', [{
                  data: msg.chartUrlCount
                }], true);


                ApexCharts.exec('chartLang', 'updateOptions', {
                  xaxis: {
                    categories: msg.langs,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);

                ApexCharts.exec('chartLang', 'updateSeries', [{
                  data: msg.langCount
                }], true);


                ApexCharts.exec('chartClient', 'updateOptions', {
                  xaxis: {
                    categories: msg.sources,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);

                ApexCharts.exec('chartClient', 'updateSeries', [{
                  data: msg.sourceCount
                }], true);

                ApexCharts.exec('chartTypeTwit', 'updateOptions', {
                  xaxis: {
                    categories: msg.typeTweet,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);

                ApexCharts.exec('chartTypeTwit', 'updateSeries', [{
                  data: msg.TypeCount
                }], true);
                

                ApexCharts.exec('chartAnswers', 'updateOptions', {
                  xaxis: {
                    categories: msg.quote_screen_names,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);

                ApexCharts.exec('chartAnswers', 'updateSeries', [{
                  data: msg.quote_screen_name_count
                }], true);
                

                ApexCharts.exec('chartRetweet', 'updateOptions', {
                  xaxis: {
                    categories: msg.retweet_screen_names,
                    labels: {
                      show: false
                    }
                  }
                }, false, true);

                ApexCharts.exec('chartRetweet', 'updateSeries', [{
                  data: msg.retweet_screen_name_count
                }], true);


                $('#untilTwits').val(msg.charttDay[0])
                $('#sinceTwits').val(msg.charttDay[msg.charttDay.length - 1])
              }
              // enableScroll()
              
          },
          error: function(msg) {
              alert('bad request')
          },
          beforeSend: function(){
            $("#overlay").fadeIn(300);
            disableScroll()
        },
       complete: function(){
        enableScroll()
        $("#overlay").fadeOut(300);
       }
        });
  }
}