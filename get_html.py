
# Создаем HTML-шаблон
html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holcim Lista</title>
    <link rel="stylesheet" type="text/css" href="static/styles/styles.css">
</head>

<body style="background: linear-gradient(121deg, #e5fff4 0%, #9ec8ff 100%);">
    <div class="main">
        <div class="title_div">
            <div class="title_text">
                <p><span style="font-size: large; font-weight: bold;">Lista Holcim</span></p>
                <p>{{ Zaktualizowano }}</p>
                <p style="color: rgb(59, 59, 124);">{{ brend }}</p>
                <p style="font-size: large; color: rgb(231, 118, 43);">{{cong}}</p>
                <p style="font-size: large; color: rgb(238, 36, 36); font-weight: bold;">{{war}}</p>
            </div>

            <div class="title_image"><a href="https://www.holcim.pl/" target="_blank" style="filter: drop-shadow(5px -1px 5px #19345d);"><img
                        src="static/image/holcim_logo_color.svg" alt="Holcim"></a></div>
        </div>
    </div>

    <div class="main_list">
        <p>{{ element1[0] }}</p>
        <div class="main_list" style="filter: drop-shadow(7px 8px 10px #9e9a9a); background-color: rgb(189, 255, 193); border-radius: 16px;">
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
        <div class="main_list" style="filter: drop-shadow(7px 8px 10px #9e9a9a); background-color: rgb(255, 247, 188); border-radius: 16px;">
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
        <div class="main_list" style="filter: drop-shadow(7px 8px 10px #9e9a9a); background-color: rgb(255, 188, 188); border-radius: 16px">
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
