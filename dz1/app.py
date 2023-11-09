# Задание №9
# 📌 Создать базовый шаблон для интернет-магазина,
# содержащий общие элементы дизайна (шапка, меню,
# подвал), и дочерние шаблоны для страниц категорий
# товаров и отдельных товаров.
# 📌 Например, создать страницы "Одежда", "Обувь" и "Куртка",
# используя базовый шаблон.!

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/about/')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/contact/')
def contact():  # put application's code here
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
