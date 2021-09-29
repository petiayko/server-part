from db_init import User, db


def add(login, email, password):
    user = User(login=login, mail=email, password=password)
    db.session.add(user)
    db.session.commit()
