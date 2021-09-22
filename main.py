from flask import Flask, escape, request
import requests

app = Flask(__name__)
#
#
# @app.route('/user/<name>')
# def hello_world(name):
#     html_text = '''
#     <html>
#         <body>
#             <h1>Header</h1>
#             <p>Hello, %s</p>
#         </body>
#     </html>
#     '''
#     return html_text % escape(name)


@app.route('/sum/', methods=['GET'])
def sum():
    if request.method == 'GET':
        a = int(request.args['a'])
        b = int(request.args['b'])
        return f'{a} + {b} = {a + b}'
    return f'Был получен {request.method} запрос.'


@app.route('/dif/', methods=['GET'])
def dif():
    if request.method == 'GET':
        a = int(request.args['a'])
        b = int(request.args['b'])
        return f'{a} - {b} = {a - b}'
    return f'Был получен {request.method} запрос.'


@app.route('/mult/', methods=['GET'])
def mult():
    if request.method == 'GET':
        a = int(request.args['a'])
        b = int(request.args['b'])
        return f'{a} * {b} = {a * b}'
    return f'Был получен {request.method} запрос.'


@app.route('/div/', methods=['GET'])
def div():
    if request.method == 'GET':
        a = int(request.args['a'])
        b = int(request.args['b'])
        return f'{a} / {b} = {a / b}'
    return f'Был получен {request.method} запрос.'


@app.route('/pow/', methods=['GET'])
def pow():
    if request.method == 'GET':
        a = int(request.args['a'])
        b = int(request.args['b'])
        return f'{a} ** {b} = {a ** b}'
    return f'Был получен {request.method} запрос.'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
    req = requests.get('http://127.0.0.1:5555/reauest-test/', params={'a': 5, 'b': 3})
