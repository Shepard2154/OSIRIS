addGeofenceTwit = function (person) {

  bg_color = "bg-teal-600"
  place = person['place']

  visible = 'view'

  if (place == "") {
    visible = 'hidden'
  }

  if (person['retweet'] == true) {
    bg_color = "bg-purple-600"
    type = "Retweet"

  }
  sze = Object.keys(person['hashtags']).length
  hashtags = "<span></span>"
  if (sze > 0) {
    for (var i = 0; i < sze; i++) {
      hashtags = hashtags + `<span style="text-align: center; /*! display: inline-table; */ padding: 3px; width: max-content; visibility:view;margin: 2px;" class="shadow-inner inline-flex justify-center
      items-baseline text-sm mr-2 rounded text-white bg-teal-600">${person['hashtags'][i]}</span>`;
    }
  }

  const markup = `
    <div id="sdf" class="p-2 lg:w-full">
      <div class="flex flex-row shadow rounded text-gray-800 p-2
        relative border-l-4 bg-gray-100 border-teal-600">
        <span style="text-align: center; display: inline-table; padding: 7px; width: min-content; visibility:${visible}" class="shadow-inner inline-flex  
          justify-center
          items-baseline text-sm mr-2 rounded text-white ${bg_color}">${place}</span>
        <div class="flex flex-row">
          <div class="flex flex-col flex-1 ml-2">
            <div class="flex flex-row flex-wrap items-baseline"><a
                href="https://twitter.com/${person['username']}"
                rel="noopener noreferrer" target="_blank"><span
                  class="text-lg font-bold mr-2
                  hover:text-brand">${person['name']}</span></a><span
                class="font-semibold"><a
                  class="hover:text-brand"
                  href="https://twitter.com/${person['username']}"
                  rel="noopener noreferrer" target="_blank">@${person['username']}</a>
                · <a
                  href="${person['link']}"
                  rel="noopener noreferrer" target="_blank"><time
                    class="hover:text-brand" datetime="">${person['date']}</time></a></span></div>
            <p style="font-style: italic;">${person['text']}</p>
            <div aria-describedby="tooltip:10" data-reach-tooltip-trigger="" class="flex flex-row mr-3"><span class="text-gray-500
              ">Лайки:</span><a id="" class=" mr-3 text-brand font-semibold 
              hover:text-brand-dark" name="" rel="noopener noreferrer" target="_blank">${person['nlikes']}</a><span class="text-gray-500
              ">Ретвиты:</span><a id="" class=" mr-3 text-brand font-semibold 
              hover:text-brand-dark" name="" rel="noopener noreferrer" target="_blank">${person['nretweets']}</a><span class="text-gray-500
              ">Цитата:</span><a id="" class=" mr-3 text-brand font-semibold 
              hover:text-brand-dark" name="" rel="noopener noreferrer" target="_blank">${person['nreplies']}</a></div>
            <div aria-describedby="tooltip:10" data-reach-tooltip-trigger="" class="flex flex-row mr-3">${hashtags}</div>
          </div>
        </div>
      </div>
    </div>
    `;

  $("#geofenceBoard").html($("#geofenceBoard").html() + markup);
}