from flask import request
import database
from db_init import app, user_db, Users


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
        database.add(
            login=request.args['login'],
            email=request.args['email'],
            password=request.args['password']
        )
    return str(True)


@app.route('/delete_user/', methods=['GET'])
def delete_user():
    if request.method == 'GET':
        database.delete(login=request.args['login'])
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


@app.route('/add_path/', methods=['GET'])
def add_path():
    if request.method == 'GET':
        login = request.args['login']
        path = request.args['path']
        database.add_folder(login, path)
    return str(True)


@app.route('/add_file/', methods=['GET'])
def add_file():
    if request.method == 'GET':
        login = request.args['login']
        folder_path = request.args['folder_path']
        filename = request.args['filename']
        edit_time = request.args['edit_time']
        database.add_file(login, folder_path, filename, float(edit_time))
    return str(True)
