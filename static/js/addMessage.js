addMessageOnBoard = function (human) {
    // const human = {
    //     screen_name: 'KremlinRussia',
    //     name: 'Web Президент',
    //     date: '13-10-2001',
    //     time: '12:00',
    //     tweet:"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quisque egestas diam in arcu cursus euismod quis viverra nibh. Eu scelerisque felis...",
    //     link:"http://google.com/",
    //     urls:''
    // }

    // And then create our markup:
    const markup = `
    <div class="p-4 w-full lg:w-1/2 xl:w-1/3">
        <div
            class="flex flex-col shadow rounded text-gray-800 p-2
            relative border-l-4 bg-gray-100 border-teal-600">
            <span
                class="shadow-inner absolute inline-flex justify-center
                items-baseline text-sm mt-2 mr-2 px-2 rounded top-0
                right-0 text-white bg-teal-600">Tweet</span>
            <div class="flex flex-row">
                <div class="flex flex-col flex-1 ml-2">
                    <div class="flex flex-row flex-wrap items-baseline
                        mr-20"><a
                            href="https://twitter.com/${human['screen_name']}"
                            rel="noopener noreferrer" target="_blank"><span
                                class="text-lg font-bold mr-2 hover:text-brand">${human['name']}</span></a><span
                            class="font-semibold"><a class="hover:text-brand"
                                href="https://twitter.com/${human["screen_name"]}"
                                rel="noopener noreferrer" target="_blank">@${human["screen_name"]}</a>
                            · <a
                                href="${human["link"]}"
                                rel="noopener noreferrer" target="_blank"><time
                                    class="hover:text-brand"
                                    datetime="">${human["time"]} ${human["date"]}</time></a></span></div>
                    <p style="font-style: italic;">${human["tweet"]}</p>
                </div>
            </div><button class="ml-auto text-brand
                hover:text-brand-dark mt-2"
                type="button" onclick="window.open('${human["link"]}')">Развернуть</button>
        </div>
    </div>
    `;

    $("#messageBoard").html($("#messageBoard").html() + markup);
}