import json
from flask import request, jsonify
import database
from db_init import app, user_db, Users
import jwt
import datetime
from functools import wraps


def token_required(req):
    @wraps(req)
    def decorated(*args, **kwargs):
        #
        # if 'Authorization' in request.headers:
        #     token = request.headers['Authorization']
        #     print(token)
        # else:
        #     return app.make_response(('Token is wrong', 403))
        token = request.headers['Authorization']
        token = token[token.find('": "')+4:token.find('"\\')]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            print(e)
            return app.make_response(('Token is wrong', 403))
        return req(*args, **kwargs)
    return decorated


@app.route('/auth/', methods=['GET'])
def auth():
    if request.method == 'GET':
        login = request.args['login']
        password = request.args['password']
        if database.auth(login=login, password=password):
            token = jwt.encode({'user': login,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                                }, app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})
        return 'denied'


# @app.route('/check_email/', methods=['GET'])
# def check_email():
#     if request.method == 'GET':
#         email = request.args['email']
#         return str(user_db.session.query(Users).filter_by(mail=email).count() != 0)


# @app.route('/check_login/', methods=['GET'])
# def check_login():
#     if request.method == 'GET':
#         login = request.args['login']
#         return str(user_db.session.query(Users).filter_by(login=login).count() != 0)

@app.route('/test/')
@token_required
def test():
    return 'True'


@app.route('/get_password/', methods=['GET'])
def get_password():
    if request.method == 'GET':
        login = request.args['login']
        usr = user_db.session.query(Users).filter_by(login=login).one()
        return usr.password


@app.route('/get_email/', methods=['GET'])
def get_email():
    if request.method == 'GET':
        login = request.args['login']
        usr = user_db.session.query(Users).filter_by(login=login).one()
        return usr.mail


@app.route('/add_user/', methods=['GET'])
def add_user():
    if request.method == 'GET':
        database.add_user(
            login=request.args['login'],
            email=request.args['email'],
            password=request.args['password']
        )
    return str(True)


@app.route('/delete_user/', methods=['GET'])
@token_required
def delete_user():
    if request.method == 'GET':
        database.delete_user(login=request.args['login'])
    return str(True)


@app.route('/change_mail/', methods=['GET'])
@token_required
def change_mail():
    if request.method == 'GET':
        login = request.args['login']
        email = request.args['email']
        database.change(login=login, field='mail', new_value=email)
    return str(True)


@app.route('/change_password/', methods=['GET'])
@token_required
def change_password():
    if request.method == 'GET':
        login = request.args['login']
        password = request.args['password']
        database.change(login=login, field='password', new_value=password)
    return str(True)


@app.route('/add_version/', methods=['GET'])
@token_required
def add_version():
    if request.method == 'GET':
        files = json.loads(request.data.decode('UTF-8'))
        login = files['login']
        mac = files['mac']
        path_file = files['path_file']
        ver = files['new_version']
        database.add_folder(
            login=login,
            mac=mac,
            folder_path=path_file,
            version=ver
        )
        for file in files['files']:
            database.add_files(
                login=login,
                mac=mac,
                folder_path=path_file,
                filename=file,
                edited_at=float(files['files'][file]),
                version=ver
            )
    return str(True)


@app.route('/update_version/', methods=['GET'])
@token_required
def update_version():
    if request.method == 'GET':
        files = json.loads(request.data.decode('UTF-8'))
        login = files['login']
        mac = files['mac']
        path_file = files['path_file']
        o_ver = files['old_version']
        n_ver = files['new_version']
        database.delete_folder(
            login=login,
            mac=mac,
            folder_path=path_file,
            version=o_ver
        )
        database.add_folder(
            login=login,
            mac=mac,
            folder_path=path_file,
            version=n_ver
        )
        for file in files['files']:
            database.add_files(
                login=login,
                mac=mac,
                folder_path=path_file,
                filename=file,
                edited_at=float(files['files'][file]),
                version=n_ver
            )
    return str(True)


@app.route('/delete_version/', methods=['GET'])
@token_required
def delete_version():
    if request.method == 'GET':
        database.delete_folder(
            login=request.args['login'],
            mac=request.args['mac'],
            folder_path=request.args['folder_path'],
            version=request.args['version']
        )
    return str(True)
