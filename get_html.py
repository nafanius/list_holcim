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

        img {
            display: inline;
            margin: 5px;
            filter: drop-shadow(9px -5px 3px #a1a1a1);

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
                        <img src="static/image/holcim_logo_color.svg" alt="Holcim"></a></div>
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
