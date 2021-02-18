from flask import Flask, url_for
import datetime

app = Flask(__name__)


@app.route('/')
def p():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    return '''Человечество вырастает из детства.<br>
    Человечеству мала одна планета.<br>
    Мы сделаем обитаемыми безжизненные пока планеты.<br>
    И начнем с Марса!<br>
    Присоединяйся!'''


@app.route('/image_mars')
def image_mars():
    return f'''<h1>Жди нас, Марс!<h1><rb>
                <img src="{url_for('static', filename='images/MARS.png')}" 
                alt="здесь должна была быть картинка, но не нашлась">
                <rb><h4>Вот она какая, красная планета.<h4>'''


@app.route('/promotion_image')
def promotion_image():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1><rb>
                    <img src="{url_for('static', filename='images/MARS.png')}" 
                    alt="здесь должна была быть картинка, но не нашлась"> <br>
                    <h6 class="fs">Человечество вырастает из детства.</h6>
                    <h2 class="fs">Человечеству мала одна планета.</h2>
                    <h3 class="fs">Мы сделаем обитаемыми безжизненные пока планеты.</h3>
                    <h4 class="fs">И начнем с марса.</h4>
                    <h5 class="fs">Присоединяйся!</h5>
                  </body>
                </html>"""



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
