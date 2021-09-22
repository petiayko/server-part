from flask import Flask, request

app = Flask(__name__)


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
