# Задание №9
# 📌 Создать страницу, на которой будет форма для ввода имени
# и электронной почты
# 📌 При отправке которой будет создан cookie файл с данными
# пользователя
# 📌 Также будет произведено перенаправление на страницу
# приветствия, где будет отображаться имя пользователя.
# 📌 На странице приветствия должна быть кнопка "Выйти"
# 📌 При нажатии на кнопку будет удален cookie файл с данными
# пользователя и произведено перенаправление на страницу
# ввода имени и электронной почты.

from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = b'your_secret_key'  # Замените 'your_secret_key' на ваш уникальный секретный ключ

@app.route('/')
def index():
    return render_template('index_task9.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        email = request.form.get('email')

        # Создаем cookie с данными пользователя
        response = make_response(redirect(url_for('greet')))
        response.set_cookie('user_data', f'{name},{email}')

        return response

@app.route('/greet')
def greet():
    # Получаем данные пользователя из cookie
    user_data_cookie = request.cookies.get('user_data')

    if user_data_cookie:
        # Разделяем данные пользователя на имя и электронную почту
        name, email = user_data_cookie.split(',')
        return render_template('welcome_task9.html', name=name, email=email)
    else:
        # Если cookie не существует, перенаправляем на страницу ввода
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Удаляем cookie с данными пользователя
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_data')
    return response

if __name__ == '__main__':
    app.run(debug=True)

