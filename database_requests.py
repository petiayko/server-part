import json
from flask import request
import database
from db_init import app, user_db, Users
import jwt


@app.route('/auth/', methods=['GET'])
def auth():
    if request.method == 'GET':
        login = request.args['login']
        password = request.args['password']
        if database.auth(login=login, password=password):
            pass


@app.route('/check_email/', methods=['GET'])
def check_email():
    if request.method == 'GET':
        email = request.args['email']
        return str(user_db.session.query(Users).filter_by(mail=email).count() != 0)


@app.route('/check_login/', methods=['GET'])
def check_login():
    if request.method == 'GET':
        login = request.args['login']
        return str(user_db.session.query(Users).filter_by(login=login).count() != 0)


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
def delete_user():
    if request.method == 'GET':
        database.delete_user(login=request.args['login'])
    return str(True)


@app.route('/change_mail/', methods=['GET'])
def change_mail():
    if request.method == 'GET':
        login = request.args['login']
        email = request.args['email']
        database.change(login=login, field='mail', new_value=email)
    return str(True)


@app.route('/change_password/', methods=['GET'])
def change_password():
    if request.method == 'GET':
        login = request.args['login']
        password = request.args['password']
        database.change(login=login, field='password', new_value=password)
    return str(True)


@app.route('/add_version/', methods=['GET'])
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
def delete_version():
    if request.method == 'GET':
        database.delete_folder(
            login=request.args['login'],
            mac=request.args['mac'],
            folder_path=request.args['folder_path'],
            version=request.args['version']
        )
    return str(True)
