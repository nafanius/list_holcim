from jinja2 import Template

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
                <p>Zaktualizowano na .....</p>
                <p><span style="color: rgb(59, 59, 124);">prodaction by "Trans-Serwis" :)</span></p>
            </div>

            <div class="title_image"><a href="https://www.holcim.pl/" target="_blank"><img
                        src="static/image/holcim_logo_color.svg" alt="Holcim"></a></div>
        </div>
    </div>

    <div></div>
    <div class="main_list">
        <p>дата день недели</p>
        <div class="main_list" style="background-color: rgb(164, 255, 169);">
            <div class="list">
                <ul>
                    <li>sasasas asas asasasas asasasasass asa sasasas1 sasa sas as asasassa sasas </li>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                </ul>
            </div>
            <div class="list">
                <ul>
                    <li>2 aas as s sa a sas as as as aa a as as asa as asasas asa asas asasasasa s</li>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                </ul>
            </div>
        </div>

        <p>дата день недели</p>
        <div class="main_list" style="background-color: rgb(252, 241, 153);">
            <div class="list">
                <ul>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                </ul>
            </div>
            <div class="list">
                <ul>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                </ul>
            </div>
        </div>

        <p>дата день недели</p>
        <div class="main_list" style="background-color: rgb(255, 157, 157); border: 30px; border-color: black;">
            <div class="list">
                <ul>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                    <li>1</li>
                </ul>
            </div>
            <div class="list">
                <ul>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                    <li>2</li>
                </ul>
            </div>
        </div>

    </div>
</body>

</html>
"""
lista ={}

template = Template(html_template)
rendered_html = template.render(products=lista)