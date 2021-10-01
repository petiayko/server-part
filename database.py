from sqlalchemy import and_
from db_init import Users, user_db, Folders, Files


def add(login, email, password):
    user = Users(login=login, mail=email, password=password)
    user_db.session.add(user)
    user_db.session.commit()


def delete(login):
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
    # count_version = user_db.session.query(Folders).filter(and_(
    #     Folders.login == login,
    #     Folders.mac == mac,
    #     Folders.folder_path == folder_path
    # )).count()
    count_all = user_db.session.query(Folders).count()
    fld = Folders(
        id=count_all,
        login=login,
        mac=mac,
        folder_path=folder_path,
        folder_version=version,
        folder_id=count
    )
    user_db.session.add(fld)
    user_db.session.commit()


def add_file(login, mac, folder_path, filename, edited_at, version):
    # ver = user_db.session.query(Files).filter(and_(
    #     Files.login == login,
    #     Files.mac == mac,
    #     Files.folder_path == folder_path,
    #     Files.filename == filename,
    #     Files.edited_at != edited_at
    # )).count()
    count_all = user_db.session.query(Files).count()
    fls = Files(
        id=count_all,
        login=login,
        mac=mac,
        folder_path=folder_path,
        filename=filename,
        edited_at=edited_at,
        version=version
    )
    user_db.session.add(fls)
    user_db.session.commit()
