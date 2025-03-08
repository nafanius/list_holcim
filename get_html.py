# <link rel="stylesheet" type="text/css" href="static/styles/styles.css">
# Создаем HTML-шаблон
html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holcim Lista</title>
    <style>
        * {
            margin: 0px;
        }

        body {
            background: linear-gradient(144deg, #f0fded 20%, #a5ecfd 100%);

        }

        ul {
            list-style: none;
        }

        li {
            word-wrap: break-word;
            overflow-wrap: break-word;
        }

        @keyframes congrat {
            0% {
                animation-timing-function: ease-in;
                opacity: 0;
                transform: scale(0);
            }

            38% {
                animation-timing-function: ease-out;
                opacity: 1;
                transform: scale(1);
            }

            55% {
                animation-timing-function: ease-in;
                transform: scale(0.7);
            }

            72% {
                animation-timing-function: ease-out;
                transform: scale(1);
            }

            81% {
                animation-timing-function: ease-in;
                transform: scale(0.84);
            }

            89% {
                animation-timing-function: ease-out;
                transform: scale(1);
            }

            95% {
                animation-timing-function: ease-in;
                transform: scale(0.95);
            }

            100% {
                animation-timing-function: ease-out;
                transform: scale(1);
            }
        }

        @keyframes warning {

            0%,
            100% {
                transform: translateX(0%);
                transform-origin: 50% 50%;
            }

            15% {
                transform: translateX(-30px) rotate(-6deg);
            }

            30% {
                transform: translateX(15px) rotate(6deg);
            }

            45% {
                transform: translateX(-15px) rotate(-3.6deg);
            }

            60% {
                transform: translateX(9px) rotate(2.4deg);
            }

            75% {
                transform: translateX(-6px) rotate(-1.2deg);
            }
        }

        @keyframes beton {
            0% {
                animation-timing-function: ease-in;
                opacity: 0;
                transform: translateX(-300px);

            }

            38% {
                animation-timing-function: ease-out;
                opacity: 1;
                transform: translateX(0);
            }

            55% {
                animation-timing-function: ease-in;
                transform: translateX(-68px);
            }

            72% {
                animation-timing-function: ease-out;
                transform: translateX(0);
            }

            81% {
                animation-timing-function: ease-in;
                transform: translateX(-28px);
            }

            90% {
                animation-timing-function: ease-out;
                transform: translateX(0);
            }

            95% {
                animation-timing-function: ease-in;
                transform: translateX(-8px);
            }

            100% {
                animation-timing-function: ease-out;
                transform: translateX(0);
            }
        }

        .main {
            text-align: left;
            align-content: center;
            display: block;
        }

        .title_div {
            display: flex;
            padding: 5px;
            flex-direction: row;
            align-items: left;
            text-align: left;
        }

        .title_text {
            flex: 1;
            display: inline-block;
            text-align: start;
            order: 1;
            margin-top: 3px;
            margin-left: 3px;
            margin-right: 3px;
        }

        .title_image {
            display: inline-block;
            white-space: nowrap;
            max-width: 100%;
            text-align: center;
            height: auto;
            order: 2;
        }

        .main_list {
            display: flex;
            flex-direction: column;;
            text-align: center;
            align-content: center;
            padding: 5px;
            justify-content: center;
            filter: drop-shadow(3px -2px 5px #cac9c9);
            border-radius: 10px;
        }

        .main_list>p {
            margin-top: 5px;
            margin-left: 3px;
            font-size: larger;
            text-align: left;
            font-weight: bold;
        }

        .libold {
            margin-top: 5px;
            font-weight: bold
        }

        .lirozklad {
            list-style: decimal;
            position: relative;
            margin-left: 1.4em;
        }

        .lirozklad::marker {
            position: absolute;
            left: 0;
            color: rgb(75, 1, 1);
            font-size: 0.9em;
        }

        .list {
            display: block;
            margin: 3px;
            margin-bottom: 20px;
            text-align: left;
        }

        .rozklad_curs_tab {
            font-size: 0.8em;
            justify-content: center;
            text-align: center;
        }

        .rozklad_kierowca_tab {
            font-size: 0.8em;
            justify-content: center;
            text-align: center;
        }

        .rozklad_kerowca_brak {
            font-size: 0.7em;
            justify-content: center;
            text-align: center;
        }

        .hidden {
            display: none;
        }

        .content {
            background: local;
            
        }

        .button-like {
            display: inline-block;
            padding: 10px 10px;
            margin: 2px;
            background-color: #003e7c;
            color: white;
            text-align: center;
            cursor: pointer;
            border: none;
            border-radius: 4px;
            text-decoration: none;
        }
        .button-push {
            display: inline-block;
            padding: 10px 10px;
            margin: 2px;
            background-color:rgb(77, 158, 30);
            color: white;
            text-align: center;
            cursor: pointer;
            border: none;
            border-radius: 4px;
            text-decoration: none;
            }

        .full-width-graph {
            display: inline-block;
            width: 100%;
            margin: 0px;
            justify-content: center;
            text-align: center;
           }

        .content-div {
            display: none; /* Изначально скрываем все элементы */
        }


        #brend {
            color: rgb(59, 59, 124);
            font-size: small;
        }

        #cong {
            font-size: large;
            margin: 3px;
            color: rgb(231, 118, 43);
            font-weight: bold;
            animation: congrat 5s linear 1s 1 alternate both;
        }

        #war {
            font-size: large;
            color: rgb(238, 36, 36);
            font-weight: bold;
            animation: warning 3s ease 2s infinite normal forwards;
        }

        #logo {
            display: inline;
            margin-top: 5px;
            filter: drop-shadow(3px -3px 3px #a1a1a1);
        }

        #betonka {
            animation: beton 5s linear 2s 1 alternate forwards;
            padding-bottom: 5px;
            filter: drop-shadow(3px -3px 2px #a1a1a1);

        }

        #bet {
            text-align: right;
            padding-right: 15px;
        }

        #dropdown {
            border: none;
            margin-left: 5px;
            font-weight: normal;
            font-size: large;
            font-weight: bold;
            color: #003e7c;
            background: linear-gradient(90deg, #ffffff 0%, rgba(0, 128, 0, 0.397) 100%);
            border-radius: 3px;
            filter: drop-shadow(3px -3px 2px #a1a1a1);
        }

        #dropdown option {
            font-weight: normal;
            color: green;
        }

        #dropdown:focus {
            border: none;
        }

        #dropdown option:checked,
        #dropdown option[selected] {
            font-weight: bold;
            color: #003e7c;
        }


        @media (max-width: 500px) {
            .title_div {
                flex-direction: column;

            }

            .title_text {
                order: 2;
            }

            .title_image {
                order: 1;
            }
        }
    </style>
    <script>
            function toggleVisibility(divId, buttonId) {
                const div = document.getElementById(divId);
                const button = document.getElementById(buttonId);

                // Переключаем видимость элемента
                if (div.classList.contains('hidden')) {
                    div.classList.remove('hidden');
                    window.dispatchEvent(new Event('resize'));
                } else {
                    div.classList.add('hidden');
                };

                // Изменяем текст кнопки
                if (div.classList.contains('hidden')) {
                    button.classList.remove('button-like');
                    button.classList.add('button-push');
                } else {
                    button.classList.remove('button-push');
                    button.classList.add('button-like');
                }
            }

            document.addEventListener('DOMContentLoaded', (event) => {
                showDivs(); // Показываем первый элемент при загрузке страницы
            });

            function showDivs() {
                const dropdown = document.getElementById('dropdown');
                const selectedValue = dropdown.value;

                // Скрываем все div'ы
                const allDivs = document.querySelectorAll('.content-div');
                allDivs.forEach(div => div.style.display = 'none');

                // Показываем только выбранный div
                const selectedDiv = document.getElementById(selectedValue);
                if (selectedDiv) {
                    selectedDiv.style.display = 'block';
                }
            }
        </script>

</head>

<body>
    <div class="main">

    <div id="ww_7367f5689bf4c" v='1.3' loc='id' a='{"t":"ticker","lang":"pl","ids":["wl7640"],"font":"Arial","sl_ics":"one_a","sl_sot":"celsius","cl_bkg":"image","cl_font":"#FFFFFF","cl_cloud":"#FFFFFF","cl_persp":"#81D4FA","cl_sun":"#FFC107","cl_moon":"#FFC107","cl_thund":"#FF5722"}'>More forecasts: 
        <a href="https://oneweather.org/warsaw/30_days/" id="ww_7367f5689bf4c_u" target="_blank">Weather forecast Warsaw 30 days</a>
    </div>

    <script async src="https://app3.weatherwidget.org/js/?id=ww_7367f5689bf4c"></script>

        <div class="title_div">
            <div class="title_text">
                <p><span style="font-size: large; font-weight: bold;">Lista Holcim</span></p>
                <p>{{ data['Zaktualizowano'] }}</p>
                <p id="brend">{{ data['brend'] }}</p>
                <p id="cong">{{ data['cong'] }}</p>
                <p id="war">{{ data['war'] }}</p>
            </div>

            <div class="title_image"><a style="text-decoration: none;" href="https://www.holcim.pl/" target="_blank">
                <svg id="logo" xmlns="http://www.w3.org/2000/svg" width="284" height="67" fill="none"
                    viewBox="0 0 284 67">
                    <g clip-path="url(#clip0)">
                        <path fill="#1D4370"
                            d="M78.39 19.11h9.14v12.25H99.6V19.11h9.13v32.74H99.6V39.41H87.52v12.44h-9.14V19.11h.01zm38.25 16.46v-.09c0-9.4 7.46-17.03 17.63-17.03 10.17 0 17.53 7.53 17.53 16.93v.09c0 9.4-7.46 17.02-17.63 17.02-10.17.01-17.53-7.52-17.53-16.92zm25.84 0v-.09c0-4.72-3.27-8.84-8.3-8.84-4.99 0-8.16 4.02-8.16 8.75v.09c0 4.72 3.27 8.84 8.26 8.84 5.02 0 8.2-4.02 8.2-8.75zm17.65-16.46h9.14V43.9h15.1v7.95h-24.24V19.11zm28.83 16.46v-.09c0-9.54 7.39-17.03 17.38-17.03 6.73 0 11.07 2.81 13.99 6.83l-6.88 5.29c-1.88-2.34-4.05-3.84-7.2-3.84-4.61 0-7.86 3.88-7.86 8.65v.09c0 4.91 3.25 8.75 7.86 8.75 3.44 0 5.46-1.59 7.44-3.98l6.88 4.86c-3.11 4.26-7.3 7.39-14.6 7.39-9.43.01-17.01-7.14-17.01-16.92zm39.81-16.46h9.18v32.74h-9.18V19.11zm18.63 0h9.65l8.38 12.68 8.38-12.68h9.65v32.74h-9.09V32.7l-8.94 12.82h-.19l-8.9-12.72v19.05h-8.95V19.11h.01z" />
                        <path fill="url(#paint0_linear)"
                            d="M43.36 0C34.61 0 27.1 5.6 25.08 14.23c-.42 1.85-.71 4.23-.71 7.5v6.37H38V13.63h10.72v23.51c7.86-2.32 13.64-9.58 13.64-18.22C62.36 8.27 54.02 0 43.36 0zM18.83 65.48c8.76 0 16.43-5.6 18.45-14.23.42-1.85.71-4.23.71-7.5v-6.37H24.36v14.47H13.64V28.34C5.78 30.66 0 37.92 0 46.55c0 11.11 7.72 18.93 18.83 18.93z" />
                    </g>
                    <defs>
                        <linearGradient id="paint0_linear" x1="-1.804" x2="63.995" y1="46.714" y2="18.784"
                            gradientUnits="userSpaceOnUse">
                            <stop offset=".15" stop-color="#94C12E" />
                            <stop offset=".186" stop-color="#8DC137" />
                            <stop offset=".245" stop-color="#7BC04F" />
                            <stop offset=".32" stop-color="#5EBF77" />
                            <stop offset=".407" stop-color="#36BDAE" />
                            <stop offset=".5" stop-color="#04BBF1" />
                            <stop offset=".586" stop-color="#05B7ED" />
                            <stop offset=".674" stop-color="#08ABE0" />
                            <stop offset=".764" stop-color="#0C98CC" />
                            <stop offset=".855" stop-color="#117DAF" />
                            <stop offset=".946" stop-color="#185B8A" />
                            <stop offset="1" stop-color="#1D4370" />
                        </linearGradient>
                        <clipPath id="clip0">
                            <path fill="#fff" d="M0 0H283.46V66.47H0z" />
                        </clipPath>
                    </defs>
                </svg>
                <svg id="betonka" xmlns="http://www.w3.org/2000/svg" version="1.1" width="64px"
                        height="54px"
                        style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
                        xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g>
                            <path style="opacity:0.873" fill="#080604"
                                d="M 4.5,8.5 C 18.9304,6.54517 30.0971,11.5452 38,23.5C 38.2395,25.9769 37.4062,28.1435 35.5,30C 37.0533,33.2166 38.0533,36.7166 38.5,40.5C 39.4977,32.5277 39.831,24.5277 39.5,16.5C 45.2055,16.1712 50.8722,16.5046 56.5,17.5C 57.3323,20.161 58.1656,22.8276 59,25.5C 59.3777,32.5798 60.211,39.5798 61.5,46.5C 59.5,46.5 57.5,46.5 55.5,46.5C 55.0348,50.6294 52.7015,52.6294 48.5,52.5C 44.2985,52.6294 41.9652,50.6294 41.5,46.5C 34.8333,46.5 28.1667,46.5 21.5,46.5C 21.0348,50.6294 18.7015,52.6294 14.5,52.5C 10.2985,52.6294 7.96518,50.6294 7.5,46.5C 5.5,46.5 3.5,46.5 1.5,46.5C 1.14999,40.0448 1.81665,33.7115 3.5,27.5C 2.83333,24.1667 2.16667,20.8333 1.5,17.5C 2.22107,14.3948 3.22107,11.3948 4.5,8.5 Z M 11.5,30.5 C 15.9331,33.6982 20.9331,35.5316 26.5,36C 21.5111,36.4993 16.5111,36.6659 11.5,36.5C 11.5,34.5 11.5,32.5 11.5,30.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#f2b05b"
                                d="M 6.5,10.5 C 11.2943,10.9462 15.961,11.9462 20.5,13.5C 18.0841,18.0006 15.4175,22.3339 12.5,26.5C 11.5224,26.0233 10.6891,25.3567 10,24.5C 7.62795,19.9317 6.46129,15.265 6.5,10.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#eea04c"
                                d="M 22.5,13.5 C 24.903,13.695 26.5696,14.8616 27.5,17C 25.1185,22.2726 22.1185,27.1059 18.5,31.5C 16.5026,31.0142 15.1693,29.8475 14.5,28C 17.0448,23.0751 19.7115,18.2417 22.5,13.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#efad59"
                                d="M 29.5,17.5 C 31.0987,19.6038 32.932,21.6038 35,23.5C 34.4756,26.5814 33.309,29.5814 31.5,32.5C 28.5541,33.6548 25.5541,33.8214 22.5,33C 22.0426,32.586 21.7093,32.086 21.5,31.5C 24.1785,26.806 26.8452,22.1393 29.5,17.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#f7b25c"
                                d="M 41.5,18.5 C 45.8839,18.1744 50.2172,18.5078 54.5,19.5C 57.0722,26.2546 58.0722,33.2546 57.5,40.5C 54.1788,40.5358 51.0121,39.8692 48,38.5C 45.9135,39.4181 43.7468,40.0847 41.5,40.5C 41.5,33.1667 41.5,25.8333 41.5,18.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#100c09"
                                d="M 43.5,20.5 C 46.5184,20.3354 49.5184,20.502 52.5,21C 54.0015,24.0047 55.0015,27.1714 55.5,30.5C 51.277,30.6606 47.277,29.994 43.5,28.5C 43.5,25.8333 43.5,23.1667 43.5,20.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#60a8f5"
                                d="M 45.5,22.5 C 50.4948,21.5823 52.8281,23.5823 52.5,28.5C 50.1667,27.8333 47.8333,27.1667 45.5,26.5C 45.5,25.1667 45.5,23.8333 45.5,22.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#d5d8dc"
                                d="M 3.5,15.5 C 5.45347,18.1411 6.95347,21.1411 8,24.5C 8.68609,29.5722 9.85275,34.4055 11.5,39C 9.06319,40.3747 6.39653,40.8747 3.5,40.5C 3.87391,36.0398 4.87391,31.7065 6.5,27.5C 5.18302,23.5654 4.18302,19.5654 3.5,15.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#1c150b"
                                d="M 43.5,32.5 C 44.9778,32.238 46.3112,32.5713 47.5,33.5C 46.8333,33.8333 46.1667,34.1667 45.5,34.5C 44.2867,34.2528 43.62,33.5862 43.5,32.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#dde0e5"
                                d="M 33.5,32.5 C 35.369,34.6353 36.0356,37.3019 35.5,40.5C 29.0478,40.9155 22.7145,40.4155 16.5,39C 21.1667,38.6667 25.8333,38.3333 30.5,38C 31.6394,36.2196 32.6394,34.3863 33.5,32.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#4e545f"
                                d="M 12.5,40.5 C 17.6646,40.1619 19.8313,42.4953 19,47.5C 16,51.5 13,51.5 10,47.5C 9.16199,44.5193 9.99533,42.1859 12.5,40.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#4e545f"
                                d="M 46.5,40.5 C 51.6646,40.1619 53.8313,42.4953 53,47.5C 50,51.5 47,51.5 44,47.5C 43.162,44.5193 43.9953,42.1859 46.5,40.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#616975"
                                d="M 3.5,42.5 C 4.97782,42.238 6.31116,42.5713 7.5,43.5C 6.83333,43.8333 6.16667,44.1667 5.5,44.5C 4.28665,44.2528 3.61998,43.5862 3.5,42.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#616975"
                                d="M 21.5,42.5 C 28.1998,42.17 34.8665,42.5033 41.5,43.5C 38.1667,43.8333 34.8333,44.1667 31.5,44.5C 27.7614,44.4864 24.428,43.8197 21.5,42.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#59606d"
                                d="M 55.5,42.5 C 56.9778,42.238 58.3112,42.5713 59.5,43.5C 58.8333,43.8333 58.1667,44.1667 57.5,44.5C 56.2867,44.2528 55.62,43.5862 55.5,42.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#0e0e10"
                                d="M 12.5,42.5 C 17.1585,42.0146 18.4919,43.848 16.5,48C 11.7282,48.8104 10.3948,46.9771 12.5,42.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#0e0e10"
                                d="M 46.5,42.5 C 51.1585,42.0146 52.4919,43.848 50.5,48C 45.7282,48.8104 44.3948,46.9771 46.5,42.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#b1b3b7"
                                d="M 13.5,44.5 C 15.337,44.6395 15.6704,45.3061 14.5,46.5C 13.7025,46.0431 13.3691,45.3764 13.5,44.5 Z" />
                        </g>
                        <g>
                            <path style="opacity:1" fill="#b1b3b7"
                                d="M 47.5,44.5 C 49.337,44.6395 49.6704,45.3061 48.5,46.5C 47.7025,46.0431 47.3691,45.3764 47.5,44.5 Z" />
                        </g>
                    </svg>
                </a>
            </div>
        </div>

        <select id="dropdown" onchange="showDivs()">
        <option value="zawod">Zawodzie</option>
        <option value="odola">Odolany</option>
        <option value="zeran">Żerań</option>
        <option value="gora">Góra kalwaria</option>
        </select>

        <p style="padding-left: 5px; padding-top: 5px; font-size: smaller;">zostało <span
                style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;">usunięte</span> <span
                style="color: rgb(0, 139, 7); font-weight: bold;"> nowe</span> - zmiany za ostatnie 4 godziny</p>
        <p style="padding-left: 5px; font-size: smaller;"><span style="font-weight: bold; color:rgb(226, 124, 0);">ładowanie
        </span>w danym momencie.</p>
    </div>

    <div id="zawod" class="main_list  content-div">
        <p>{{ data['zawod']['element1'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #94ffa6 0%, #ffffff 77%);">
            
            <button id="button1" class="button-push" onclick="toggleVisibility('div1', 'button1')">ROZKŁAD</button>
            <div id="div1" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['zawod']['element1'][1] }}</p>
                        {% for item in data['zawod']['element1'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['zawod']['forecast_driver_tab_1'] }}
                    {{ data['zawod']['forecast_driver_brak_1'] }}
                    {{ data['zawod']['grap_driver_1'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['zawod']['forcast_logist_1'] }}
                </div>
            </div>

            <button id="button2" class="button-push" onclick="toggleVisibility('div2', 'button2')">ZAMÓWIENIA</button>
            <div id="div2" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['zawod']['element4'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button3" class="button-push" onclick="toggleVisibility('div3', 'button3')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div3" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['zawod']['count_1'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['zawod']['clean_metrs_1'] }}</p>
                    {{ data['zawod']['rozklad_curs_1'] }}
                    <div class="full-width-graph">
                        {{ data['zawod']['grap_intens_1'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['zawod']['grap_intens_pie_1'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['zawod']['element2'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #fff194 0%, #ffffff 77%);">
            
            <button id="button4" class="button-push" onclick="toggleVisibility('div4', 'button4')">ROZKŁAD</button>
            <div id="div4" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold ">ROZKŁAD:</p>
                        <p>{{ data['zawod']['element2'][1] }}</p>
                        {% for item in data['zawod']['element2'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['zawod']['forecast_driver_tab_2'] }}
                    {{ data['zawod']['forecast_driver_brak_2'] }}
                    {{ data['zawod']['grap_driver_2'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['zawod']['forcast_logist_2'] }}
                </div>
            </div>

            <button id="button5" class="button-push" onclick="toggleVisibility('div5', 'button5')">ZAMÓWIENIA</button>
            <div id="div5" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['zawod']['element5'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button6" class="button-push" onclick="toggleVisibility('div6', 'button6')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div6" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['zawod']['count_2'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['zawod']['clean_metrs_2'] }}</p>
                    {{ data['zawod']['rozklad_curs_2'] }}
                    <div class="full-width-graph">
                        {{ data['zawod']['grap_intens_2'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['zawod']['grap_intens_pie_2'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['zawod']['element3'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #ff9f94 0%, #ffffff 77%);">
            
            <button id="button7" class="button-push" onclick="toggleVisibility('div7', 'button7')">ROZKŁAD</button>
            <div id="div7" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['zawod']['element3'][1] }}</p>
                        {% for item in data['zawod']['element3'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['zawod']['forecast_driver_tab_3'] }}
                    {{ data['zawod']['forecast_driver_brak_3'] }}
                    {{ data['zawod']['grap_driver_3'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['zawod']['forcast_logist_3'] }}

                </div>
            </div>
            
            <button id="button8" class="button-push" onclick="toggleVisibility('div8', 'button8')">ZAMÓWIENIA</button>
            <div id="div8" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['zawod']['element6'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button9" class="button-push" onclick="toggleVisibility('div9', 'button9')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div9" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['zawod']['count_3'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['zawod']['clean_metrs_3'] }}</p>
                    {{ data['zawod']['rozklad_curs_3'] }}
                    <div class="full-width-graph">
                        {{ data['zawod']['grap_intens_3'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['zawod']['grap_intens_pie_3'] }}
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div id="odola" class="main_list content-div" style="display: none;">
        <p>{{ data['odola']['element1'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #94ffa6 0%, #ffffff 77%);">
            
            <button id="button10" class="button-push" onclick="toggleVisibility('div10', 'button10')">ROZKŁAD</button>
            <div id="div10" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['odola']['element1'][1] }}</p>
                        {% for item in data['odola']['element1'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['odola']['forecast_driver_tab_1'] }}
                    {{ data['odola']['forecast_driver_brak_1'] }}
                    {{ data['odola']['grap_driver_1'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['odola']['forcast_logist_1'] }}
                </div>
            </div>

            <button id="button11" class="button-push" onclick="toggleVisibility('div11', 'button11')">ZAMÓWIENIA</button>
            <div id="div11" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['odola']['element4'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button12" class="button-push" onclick="toggleVisibility('div12', 'button12')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div12" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['odola']['count_1'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['odola']['clean_metrs_1'] }}</p>
                    {{ data['odola']['rozklad_curs_1'] }}
                    <div class="full-width-graph">
                        {{ data['odola']['grap_intens_1'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['odola']['grap_intens_pie_1'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['odola']['element2'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #fff194 0%, #ffffff 77%);">
            
            <button id="button13" class="button-push" onclick="toggleVisibility('div13', 'button13')">ROZKŁAD</button>
            <div id="div13" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold ">ROZKŁAD:</p>
                        <p>{{ data['odola']['element2'][1] }}</p>
                        {% for item in data['odola']['element2'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['odola']['forecast_driver_tab_2'] }}
                    {{ data['odola']['forecast_driver_brak_2'] }}
                    {{ data['odola']['grap_driver_2'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['odola']['forcast_logist_2'] }}
                </div>
            </div>

            <button id="button14" class="button-push" onclick="toggleVisibility('div14', 'button14')">ZAMÓWIENIA</button>
            <div id="div14" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['odola']['element5'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button15" class="button-push" onclick="toggleVisibility('div15', 'button15')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div15" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['odola']['count_2'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['odola']['clean_metrs_2'] }}</p>
                    {{ data['odola']['rozklad_curs_2'] }}
                    <div class="full-width-graph">
                        {{ data['odola']['grap_intens_2'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['odola']['grap_intens_pie_2'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['odola']['element3'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #ff9f94 0%, #ffffff 77%);">
            
            <button id="button16" class="button-push" onclick="toggleVisibility('div16', 'button16')">ROZKŁAD</button>
            <div id="div16" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['odola']['element3'][1] }}</p>
                        {% for item in data['odola']['element3'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['odola']['forecast_driver_tab_3'] }}
                    {{ data['odola']['forecast_driver_brak_3'] }}
                    {{ data['odola']['grap_driver_3'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['odola']['forcast_logist_3'] }}
                </div>
            </div>
            
            <button id="button17" class="button-push" onclick="toggleVisibility('div17', 'button17')">ZAMÓWIENIA</button>
            <div id="div17" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['odola']['element6'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button18" class="button-push" onclick="toggleVisibility('div18', 'button18')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div18" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['odola']['count_3'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['odola']['clean_metrs_3'] }}</p>
                    {{ data['odola']['rozklad_curs_3'] }}
                    <div class="full-width-graph">
                        {{ data['odola']['grap_intens_3'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['odola']['grap_intens_pie_3'] }}
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div id="zeran" class="main_list content-div" style="display: none;">
        <p>{{ data['zeran']['element1'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #94ffa6 0%, #ffffff 77%);">
            
            <button id="button19" class="button-push" onclick="toggleVisibility('div19', 'button19')">ROZKŁAD</button>
            <div id="div19" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['zeran']['element1'][1] }}</p>
                        {% for item in data['zeran']['element1'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['zeran']['forecast_driver_tab_1'] }}
                    {{ data['zeran']['forecast_driver_brak_1'] }}
                    {{ data['zeran']['grap_driver_1'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['zeran']['forcast_logist_1'] }}
                </div>
            </div>

            <button id="button20" class="button-push" onclick="toggleVisibility('div20', 'button20')">ZAMÓWIENIA</button>
            <div id="div20" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['zeran']['element4'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button21" class="button-push" onclick="toggleVisibility('div21', 'button21')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div21" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['zeran']['count_1'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['zeran']['clean_metrs_1'] }}</p>
                    {{ data['zeran']['rozklad_curs_1'] }}
                    <div class="full-width-graph">
                        {{ data['zeran']['grap_intens_1'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['zeran']['grap_intens_pie_1'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['zeran']['element2'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #fff194 0%, #ffffff 77%);">
            
            <button id="button22" class="button-push" onclick="toggleVisibility('div22', 'button22')">ROZKŁAD</button>
            <div id="div22" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold ">ROZKŁAD:</p>
                        <p>{{ data['zeran']['element2'][1] }}</p>
                        {% for item in data['zeran']['element2'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['zeran']['forecast_driver_tab_2'] }}
                    {{ data['zeran']['forecast_driver_brak_2'] }}
                    {{ data['zeran']['grap_driver_2'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['zeran']['forcast_logist_2'] }}
                </div>
            </div>

            <button id="button23" class="button-push" onclick="toggleVisibility('div23', 'button23')">ZAMÓWIENIA</button>
            <div id="div23" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['zeran']['element5'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button24" class="button-push" onclick="toggleVisibility('div24', 'button24')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div24" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['zeran']['count_2'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['zeran']['clean_metrs_2'] }}</p>
                    {{ data['zeran']['rozklad_curs_2'] }}
                    <div class="full-width-graph">
                        {{ data['zeran']['grap_intens_2'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['zeran']['grap_intens_pie_2'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['zeran']['element3'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #ff9f94 0%, #ffffff 77%);">
            
            <button id="button25" class="button-push" onclick="toggleVisibility('div25', 'button25')">ROZKŁAD</button>
            <div id="div25" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['zeran']['element3'][1] }}</p>
                        {% for item in data['zeran']['element3'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['zeran']['forecast_driver_tab_3'] }}
                    {{ data['zeran']['forecast_driver_brak_3'] }}
                    {{ data['zeran']['grap_driver_3'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['zeran']['forcast_logist_3'] }}
                </div>
            </div>
            
            <button id="button26" class="button-push" onclick="toggleVisibility('div26', 'button26')">ZAMÓWIENIA</button>
            <div id="div26" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['zeran']['element6'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button27" class="button-push" onclick="toggleVisibility('div27', 'button27')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div27" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['zeran']['count_3'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['zeran']['clean_metrs_3'] }}</p>
                    {{ data['zeran']['rozklad_curs_3'] }}
                    <div class="full-width-graph">
                        {{ data['zeran']['grap_intens_3'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['zeran']['grap_intens_pie_3'] }}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="gora" class="main_list content-div" style="display: none;">
        <p>{{ data['gora']['element1'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #94ffa6 0%, #ffffff 77%);">
            
            <button id="button28" class="button-push" onclick="toggleVisibility('div28', 'button28')">ROZKŁAD</button>
            <div id="div28" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['gora']['element1'][1] }}</p>
                        {% for item in data['gora']['element1'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['gora']['forecast_driver_tab_1'] }}
                    {{ data['gora']['forecast_driver_brak_1'] }}
                    {{ data['gora']['grap_driver_1'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['gora']['forcast_logist_1'] }}
                </div>
            </div>

            <button id="button29" class="button-push" onclick="toggleVisibility('div29', 'button29')">ZAMÓWIENIA</button>
            <div id="div29" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['gora']['element4'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button30" class="button-push" onclick="toggleVisibility('div30', 'button30')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div30" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['gora']['count_1'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['gora']['clean_metrs_1'] }}</p>
                    {{ data['gora']['rozklad_curs_1'] }}
                    <div class="full-width-graph">
                        {{ data['gora']['grap_intens_1'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['gora']['grap_intens_pie_1'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['gora']['element2'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #fff194 0%, #ffffff 77%);">
            
            <button id="button31" class="button-push" onclick="toggleVisibility('div31', 'button31')">ROZKŁAD</button>
            <div id="div31" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold ">ROZKŁAD:</p>
                        <p>{{ data['gora']['element2'][1] }}</p>
                        {% for item in data['gora']['element2'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['gora']['forecast_driver_tab_2'] }}
                    {{ data['gora']['forecast_driver_brak_2'] }}
                    {{ data['gora']['grap_driver_2'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['gora']['forcast_logist_2'] }}
                </div>
            </div>

            <button id="button32" class="button-push" onclick="toggleVisibility('div32', 'button32')">ZAMÓWIENIA</button>
            <div id="div32" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['gora']['element5'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button33" class="button-push" onclick="toggleVisibility('div33', 'button33')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div33" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['gora']['count_2'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['gora']['clean_metrs_2'] }}</p>
                    {{ data['gora']['rozklad_curs_2'] }}
                    <div class="full-width-graph">
                        {{ data['gora']['grap_intens_2'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['gora']['grap_intens_pie_2'] }}
                    </div>
                </div>
            </div>
        </div>

        <p>{{ data['gora']['element3'][0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #ff9f94 0%, #ffffff 77%);">
            
            <button id="button34" class="button-push" onclick="toggleVisibility('div34', 'button34')">ROZKŁAD</button>
            <div id="div34" class="content hidden">
                <div class="list">
                    <ul>
                        <p class="libold">ROZKŁAD:</p>
                        <p>{{ data['gora']['element3'][1] }}</p>
                        {% for item in data['gora']['element3'][2:] %}
                        <li class="lirozklad">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    <p class="libold">Prognoza czasu pierwszego załadunku i liczby kursów:</p>
                    {{ data['gora']['forecast_driver_tab_3'] }}
                    {{ data['gora']['forecast_driver_brak_3'] }}
                    {{ data['gora']['grap_driver_3'] }}
                    <p class="libold">Optymalna liczba kierowców i czas pierwszego załadunku do wykonania pracy(w pomoc logistyka) :)</p>
                    {{ data['gora']['forcast_logist_3'] }}
                </div>
            </div>
            
            <button id="button35" class="button-push" onclick="toggleVisibility('div35', 'button35')">ZAMÓWIENIA</button>
            <div id="div35" class="content hidden">
                <div class="list">
                    <ul>
                        <li class="libold">ZAMÓWIENIA:</li>
                        {% for item in data['gora']['element6'][1:] %}
                        <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button id="button36" class="button-push" onclick="toggleVisibility('div36', 'button36')">HARMONOGRAM ZAŁADUNKÓW</button>
            <div id="div36" class="content hidden">
                <div class="list">
                    <p class="libold">ilosć kursów {{ data['gora']['count_3'] }}</p>
                    <p class="libold">metrów betonu bez wywrotek {{ data['gora']['clean_metrs_3'] }}</p>
                    {{ data['gora']['rozklad_curs_3'] }}
                    <div class="full-width-graph">
                        {{ data['gora']['grap_intens_3'] }}
                    </div>
                    <div class="full-width-graph">
                        {{ data['gora']['grap_intens_pie_3'] }}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer style="margin-top: 3px; text-align: center; font-size: small;">
            <p> ⓒ production by Ilin Maksim <br> fizruk.ilin@gmail.com</p>
    </footer>
</body>

</html>
"""
