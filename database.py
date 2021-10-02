from sqlalchemy import and_
from db_init import Users, user_db, Folders, Files
from sqlalchemy import func


def auth(login, password):
    return user_db.session.query(Users).filter(and_(
        Users.login == login,
        Users.password == password,
    )).count() == 1


def add_user(login, email, password):
    user = Users(login=login, mail=email, password=password)
    user_db.session.add(user)
    user_db.session.commit()


def delete_user(login):
    user_db.session.query(Users).filter_by(login=login).delete()
    user_db.session.query(Folders).filter_by(login=login).delete()
    user_db.session.query(Files).filter_by(login=login).delete()
    user_db.session.commit()


def change(login, field, new_value):
    usr = Users.query.filter_by(login=login).first()
    if field == 'mail':
        usr.mail = new_value
    elif field == 'password':
        usr.password = new_value
    user_db.session.commit()


def add_folder(login, mac, folder_path, version):
    count = user_db.session.query(Folders).filter_by(login=login).count()
    row_id = 0
    if user_db.session.query(Folders).count() != 0:
        row_id = user_db.session.query(Folders, func.max(Folders.id)).one()[1] + 1
    fld = Folders(
        id=row_id,
        login=login,
        mac=mac,
        folder_path=folder_path,
        folder_version=version,
        folder_id=count
    )
    user_db.session.add(fld)
    user_db.session.commit()


def add_files(login, mac, folder_path, filename, edited_at, version):
    row_id = 0
    if user_db.session.query(Files).count() != 0:
        row_id = user_db.session.query(Files, func.max(Files.id)).one()[1] + 1
    fls = Files(
        id=row_id,
        login=login,
        mac=mac,
        folder_path=folder_path,
        filename=filename,
        edited_at=edited_at,
        version=version
    )
    user_db.session.add(fls)
    user_db.session.commit()


def delete_folder(login, mac, folder_path, version):
    user_db.session.query(Folders).filter(and_(
        Folders.login == login,
        Folders.mac == mac,
        Folders.folder_path == folder_path,
        Folders.folder_version == version
    )).delete()
    user_db.session.query(Files).filter(and_(
        Files.login == login,
        Files.mac == mac,
        Files.folder_path == folder_path,
        Files.version == version
    )).delete()
    user_db.session.commit()
