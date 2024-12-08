
# Создаем HTML-шаблон
html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holcim Lista</title>
    <link rel="stylesheet" href="static/styles/styles.css">
</head>

<body>
    <div class="main">
        <div class="title_div">
            <div class="title_text">
                <p><span style="font-size: large; font-weight: bold;">Lista Holcim</span></p>
                <p>{{ Zaktualizowano }}</p>
                <p><span style="color: rgb(59, 59, 124);">production by "Trans-Serwis" :)</span></p>
            </div>

            <div class="title_image"><a href="https://www.holcim.pl/" target="_blank"><img
                        src="static/image/holcim_logo_color.svg" alt="Holcim"></a></div>
        </div>
    </div>

    <div class="main_list">
        <p>{{ element1[0] }}</p>
        <div class="main_list" style="background-color: rgb(189, 255, 193);">
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
        <div class="main_list" style="background-color: rgb(255, 247, 188);">
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
        <div class="main_list" style="background-color: rgb(255, 188, 188); border: 30px; border-color: black;">
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
