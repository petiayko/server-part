from flask import request
from db_init import app, db, User


@app.route('/check_email/', methods=['GET'])
def check_email():
    if request.method == 'GET':
        email = request.args['email']
        return str(db.session.query(User).filter_by(mail=email).count() != 0)


@app.route('/check_login/', methods=['GET'])
def check_login():
    if request.method == 'GET':
        login = request.args['login']
        return str(db.session.query(User).filter_by(login=login).count() != 0)


@app.route('/get_password/', methods=['GET'])
def get_password():
    if request.method == 'GET':
        login = request.args['login']
        usr = db.session.query(User).filter_by(login=login).one()
        return usr.password


@app.route('/get_email/', methods=['GET'])
def get_email():
    if request.method == 'GET':
        login = request.args['login']
        usr = db.session.query(User).filter_by(login=login).one()
        return usr.mail
