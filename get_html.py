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

        @keyframes beton {
            0% {
                animation-timing-function: ease-in;
                opacity: 0;
                transform: translateX(-250px);
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
            padding: 5px;
            justify-content: center;
            filter: drop-shadow(7px 8px 10px #9e9a9a);
            border-radius: 10px;
        }

        .main_list>p {
            margin-top: 5px;
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

        #betonka {
            animation: beton 4s linear 1s 1 alternate forwards;
        }

        #bet {
            text-align: right;
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
                <p id="bet"><svg id="betonka" version="1.0" xmlns="http://www.w3.org/2000/svg"
                width="64.000000pt" height="54.000000pt" viewBox="0 0 64.000000 54.000000"
                preserveAspectRatio="xMidYMid meet">

                <g transform="translate(0.000000,64.000000) scale(0.100000,-0.100000)"
                fill="#000000" stroke="none">
                <path d="M41 510 c-21 -38 -21 -41 -6 -98 13 -53 13 -64 0 -102 -8 -23 -15
                -64 -15 -91 0 -46 2 -49 26 -49 16 0 35 -11 51 -30 33 -40 73 -40 106 0 25 29
                28 30 117 30 89 0 92 -1 117 -30 33 -40 73 -40 106 0 16 19 35 30 51 30 22 0
                26 4 26 30 0 17 -4 30 -10 30 -6 0 -10 26 -10 58 0 56 -22 143 -43 170 -7 9
                -32 12 -81 10 l-71 -3 -3 -117 c-1 -68 -7 -118 -12 -118 -6 0 -10 19 -10 43 0
                24 -5 48 -11 54 -8 8 -8 17 0 31 16 30 15 34 -25 81 -54 63 -98 86 -187 99
                -43 7 -81 12 -86 12 -4 0 -17 -18 -30 -40z m122 5 l48 -6 -37 -67 c-20 -37
                -39 -69 -41 -71 -8 -10 -32 27 -51 80 -22 59 -17 80 16 73 10 -1 39 -6 65 -9z
                m101 -30 c17 -13 16 -17 -25 -89 -39 -68 -44 -74 -63 -64 -12 6 -23 12 -25 14
                -4 4 82 154 88 154 4 0 14 -7 25 -15z m-185 -88 c11 -32 21 -78 21 -102 0 -25
                5 -45 11 -45 5 0 7 -4 4 -10 -3 -5 -22 -10 -41 -10 -39 0 -41 7 -19 71 16 44
                14 63 -12 154 -12 42 15 -1 36 -58z m255 22 l26 -30 -20 -39 c-25 -49 -32 -53
                -80 -45 l-40 7 37 69 c21 38 41 69 45 69 3 0 18 -14 32 -31z m228 -24 c9 -27
                17 -76 17 -107 1 -55 0 -58 -23 -58 -14 0 -28 4 -31 10 -8 13 -62 13 -70 0 -3
                -5 -13 -10 -21 -10 -11 0 -14 21 -14 110 l0 111 63 -3 62 -3 17 -50z m-313
                -111 l56 -12 -92 -1 -93 -1 0 35 0 34 36 -21 c20 -12 61 -27 93 -34z m111 -14
                l0 -40 -84 0 c-47 0 -88 5 -91 10 -4 6 18 10 59 10 63 0 66 1 81 30 21 41 35
                38 35 -10z m-200 -90 c0 -5 -4 -10 -10 -10 -5 0 -10 5 -10 10 0 6 5 10 10 10
                6 0 10 -4 10 -10z m340 0 c0 -5 -4 -10 -10 -10 -5 0 -10 5 -10 10 0 6 5 10 10
                10 6 0 10 -4 10 -10z"/>
                <path d="M440 390 c0 -33 3 -40 19 -40 11 0 23 -4 26 -10 3 -5 22 -10 42 -10
                32 0 35 2 29 25 -17 69 -23 75 -71 75 l-45 0 0 -40z m81 -6 c13 -35 7 -39 -30
                -23 -39 17 -42 49 -6 49 18 0 28 -7 36 -26z"/>
                <path d="M440 300 c0 -5 9 -10 20 -10 11 0 20 5 20 10 0 6 -9 10 -20 10 -11 0
                -20 -4 -20 -10z"/>
                </g>
                </svg></p>
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
