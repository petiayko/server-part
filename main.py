from database_requests import app
from db_init import user_db, Folders, Users

if __name__ == '__main__':
    # user_db.create_all()
    app.run(host='127.0.0.1', port=5555, debug=True)
