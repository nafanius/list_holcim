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

        @keyframes myAnim {
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
            margin: 3px;
        }

        .title_image {
            max-width: 100%;
            height: auto;
            order: 2;
            margin: 3px;
        }

        .main_list {
            display: block;
            flex-direction: row;
            text-align: center;
            align-content: center;
            margin: 5px;
            padding: 5px;
            justify-content: center;
            filter: drop-shadow(7px 8px 10px #9e9a9a);
            border-radius: 10px;
        }

        .main_list>p {
            margin-top: 10px;
            margin-left: 3px;
            font-size: larger;
            text-align: left;
            font-weight: bold;
        }

        .libold{
            font-weight: bold
        }

        .list{
            display: block;
            margin: 3px;
            margin-bottom: 20px;
            text-align: left;
        }

        #brend {
            color: rgb(59, 59, 124)
        }

        #cong {
            font-size: large;
            margin: 3px;
            color: rgb(231, 118, 43);
            font-weight: bold;
            animation: myAnim 4s linear 1s 1 alternate both;
        }

        #war {
            font-size: large;
            color: rgb(238, 36, 36);
            font-weight: bold;
        }

        #logo {
            display: inline;
            margin: 5px;
            filter: drop-shadow(9px -5px 3px #a1a1a1);
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

    </head>

<body>
    <div class="main">
        <div class="title_div">
            <div class="title_text">
                <p><span style="font-size: large; font-weight: bold;">Lista Holcim</span></p>
                <p>{{ Zaktualizowano }}</p>
                <p id="brend">{{ brend }}</p>
                <p id="cong">{{ cong }}</p>
                <p id="war">{{ war }}</p>
            </div>

            <div class="title_image"><a href="https://www.holcim.pl/" target="_blank">
                <svg id="logo" xmlns="http://www.w3.org/2000/svg" width="284" height="67" fill="none" viewBox="0 0 284 67">
                    <g clip-path="url(#clip0)">
                        <path fill="#1D4370" d="M78.39 19.11h9.14v12.25H99.6V19.11h9.13v32.74H99.6V39.41H87.52v12.44h-9.14V19.11h.01zm38.25 16.46v-.09c0-9.4 7.46-17.03 17.63-17.03 10.17 0 17.53 7.53 17.53 16.93v.09c0 9.4-7.46 17.02-17.63 17.02-10.17.01-17.53-7.52-17.53-16.92zm25.84 0v-.09c0-4.72-3.27-8.84-8.3-8.84-4.99 0-8.16 4.02-8.16 8.75v.09c0 4.72 3.27 8.84 8.26 8.84 5.02 0 8.2-4.02 8.2-8.75zm17.65-16.46h9.14V43.9h15.1v7.95h-24.24V19.11zm28.83 16.46v-.09c0-9.54 7.39-17.03 17.38-17.03 6.73 0 11.07 2.81 13.99 6.83l-6.88 5.29c-1.88-2.34-4.05-3.84-7.2-3.84-4.61 0-7.86 3.88-7.86 8.65v.09c0 4.91 3.25 8.75 7.86 8.75 3.44 0 5.46-1.59 7.44-3.98l6.88 4.86c-3.11 4.26-7.3 7.39-14.6 7.39-9.43.01-17.01-7.14-17.01-16.92zm39.81-16.46h9.18v32.74h-9.18V19.11zm18.63 0h9.65l8.38 12.68 8.38-12.68h9.65v32.74h-9.09V32.7l-8.94 12.82h-.19l-8.9-12.72v19.05h-8.95V19.11h.01z"/>
                        <path fill="url(#paint0_linear)" d="M43.36 0C34.61 0 27.1 5.6 25.08 14.23c-.42 1.85-.71 4.23-.71 7.5v6.37H38V13.63h10.72v23.51c7.86-2.32 13.64-9.58 13.64-18.22C62.36 8.27 54.02 0 43.36 0zM18.83 65.48c8.76 0 16.43-5.6 18.45-14.23.42-1.85.71-4.23.71-7.5v-6.37H24.36v14.47H13.64V28.34C5.78 30.66 0 37.92 0 46.55c0 11.11 7.72 18.93 18.83 18.93z"/>
                    </g>
                    <defs>
                        <linearGradient id="paint0_linear" x1="-1.804" x2="63.995" y1="46.714" y2="18.784" gradientUnits="userSpaceOnUse">
                            <stop offset=".15" stop-color="#94C12E"/>
                            <stop offset=".186" stop-color="#8DC137"/>
                            <stop offset=".245" stop-color="#7BC04F"/>
                            <stop offset=".32" stop-color="#5EBF77"/>
                            <stop offset=".407" stop-color="#36BDAE"/>
                            <stop offset=".5" stop-color="#04BBF1"/>
                            <stop offset=".586" stop-color="#05B7ED"/>
                            <stop offset=".674" stop-color="#08ABE0"/>
                            <stop offset=".764" stop-color="#0C98CC"/>
                            <stop offset=".855" stop-color="#117DAF"/>
                            <stop offset=".946" stop-color="#185B8A"/>
                            <stop offset="1" stop-color="#1D4370"/>
                        </linearGradient>
                        <clipPath id="clip0">
                            <path fill="#fff" d="M0 0H283.46V66.47H0z"/>
                        </clipPath>
                    </defs>
                </svg></a>
            </div>
        </div>
    </div>

    <div class="main_list">
        <p>{{ element1[0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #94ffa6 0%, #ffffff 77%);">
            <div class="list">
                <ul>
                    <li class="libold">ROZKŁAD:</li>
                    {% for item in element1[1:] %}
                    <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </div>
            <div class="list">
                <ul>
                    <li class="libold">HARMONOGRAM ZAŁADUNKÓW:</li>
                    {% for item in element4[1:] %}
                    <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <p>{{ element2[0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #fff194 0%, #ffffff 77%);">
            <div class="list">
                <ul>
                    <li class="libold">ROZKŁAD:</li>
                    {% for item in element2[1:] %}
                    <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </div>
            <div class="list">
                <ul>
                    <li class="libold">HARMONOGRAM ZAŁADUNKÓW:</li>
                    {% for item in element5[1:] %}
                    <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <p>{{ element3[0] }}</p>
        <div class="main_list" style="background: linear-gradient(93deg, #ff9f94 0%, #ffffff 77%);">
            <div class="list">
                <ul>
                    <li class="libold">ROZKŁAD:</li>
                    {% for item in element3[1:] %}
                    <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </div>
            <div class="list">
                <ul>
                    <li class="libold">HARMONOGRAM ZAŁADUNKÓW:</li>
                    {% for item in element6[1:] %}
                    <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>

    </div>
</body>

</html>
"""
