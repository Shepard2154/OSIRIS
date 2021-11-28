addCAuserOnBoard = function (person) {
    bord_color = "border-teal-600"
    if (parseInt(person['following']) > parseInt(person['followers'])) {
      bord_color = "border-purple-600"
    }

    const markup = `
                  <div id="${person['username']}" class="lg:w-full causer" style="padding: .8rem;"> <!--width: 25%; -->
                    <div name="border_color" class="flex flex-col shadow rounded text-gray-800 p-2
                      relative border-l-4 bg-gray-100 ${bord_color}">
                      <div class="relative" style="padding: .5rem;">
                        <div class="flex flex-row"><img id="acc_image" alt="@${person['username']}'s Profile
                            Picture" class="rounded-lg mr-4 h-12 w-h-12" src="${person['profile_image_url']}" title="@${person['username']}'s Profile Picture">
                          <div class="flex flex-col overflow-hidden max-w-2xs
                            lg:max-w-full xl:max-w-2xs"><a id="acc_twitter_link" href="https://twitter.com/${person['username']}" rel="noopener
                              noreferrer" target="_blank" title="@${person['username']}'s Twitter Profile"><span class="break-all leading-none font-semibold text-xl
                                hover:text-brand whitespace-no-wrap" id="acc_name">${person['name']}</span></a>
                                <a id="acc_username_2" rel="noopener
                              noreferrer" target="_blank">
                              <h2 id="acc_username" class="font-medium text-lg
                                text-gray-500
                                hover:text-brand acc_username">@${person['screen_name']}</h2>
                            </a></div>
                            <div class="flex flex-col mr-3 mb-2" aria-describedby="tooltip:8" data-reach-tooltip-trigger=""><a class="text-brand font-semibold 
                              hover:text-brand-dark" rel="noopener noreferrer" target="_blank"></a><span class="text-gray-500
                              "></span></div>
                            <div class="flex flex-col mr-3 mb-2" aria-describedby="tooltip:8" data-reach-tooltip-trigger=""><a id="acc_tweet_count" class="text-brand font-semibold 
                              hover:text-brand-dark" rel="noopener noreferrer" target="_blank">${person['tweets']}</a><span class="text-gray-500
                              ">Твиты</span></div>
                          <div class="flex flex-col mr-3 mb-2" aria-describedby="tooltip:9" data-reach-tooltip-trigger=""><a id="acc_following_count" class="text-brand font-semibold 
                              hover:text-brand-dark" name="acc_following_count" rel="noopener noreferrer" target="_blank">${person['following']}</a><span class="text-gray-500
                              ">Подписки</span></div>
                          <div class="flex flex-col mr-3 mb-2" aria-describedby="tooltip:10" data-reach-tooltip-trigger=""><a id="acc_followers_count" class="text-brand font-semibold 
                              hover:text-brand-dark" name="acc_followers_count" rel="noopener noreferrer" target="_blank">${person['followers']}</a><span class="text-gray-500
                              ">Подписчики</span></div>
                          <div class="flex flex-col mr-3 mb-2" aria-describedby="tooltip:11" data-reach-tooltip-trigger=""><a id="acc_likes_count" class="text-brand font-semibold 
                              hover:text-brand-dark" rel="noopener noreferrer" target="_blank">${person['likes']}</a><span class="text-gray-500
                              ">Лайки</span></div>
                          <div class="flex flex-col mr-3 mb-2" aria-describedby="tooltip:12" data-reach-tooltip-trigger=""><a id="acc_media_count" class="text-brand font-semibold 
                              hover:text-brand-dark" rel="noopener noreferrer" target="_blank">${person['media']}</a><span class="text-gray-500
                              ">Списки</span></div>
                          <p id="acc_bio" class="break-words leading-tight" style="padding: 15px;">${person['description']}</p>
                              <button onclick="false" onmouseover="this.style.backgroundColor='#AB0606';" onmouseout="this.style.backgroundColor='lightcoral';" style="border-radius:100px; padding-top:4px; padding-bottom:4px; padding-left:10px; padding-right:10px; font-family:revert; margin-left:10px; align-content: space-around;
                               background-color: lightcoral;" class="shadow-inner absolute inline-flex justify-center
                          items-baseline text-sm mr-2 px-2 rounded top-0
                          right-0 text-white ml-4 bg-teal-600">X</button>
                        </div>
                      </div>
                    </div>
                  </div>
    `;

    $("#caBoard").html($("#caBoard").html() + markup);
}