import requests
import os


def get_files(path_file):
    files = []
    for file in os.listdir(path_file):
        if os.path.isfile(path_file + '/' + file):
            files.append(path_file + '/' + file)
        elif os.path.isdir(path_file + '/' + file):
            files += get_files(path_file + '/' + file)
    return files


def get_metadata(files):
    table = []
    for file in files:
        table.append((file, os.stat(file).st_mtime))
    return table


if __name__ == '__main__':
    while True:
        print('Reg - 0\nChange password - 1\nChange email - 2\nGet password - 3\nGet email - 4\nDelete user - 5\nAdd path - 6\nExit - 7')
        command = input('>> ')
        if command == '0':
            req = requests.get(
                f'http://127.0.0.1:5555/add_user/',
                params={
                    'login': input('login: '),
                    'email': input('email: '),
                    'password': input('password: '),
                }
            )
        elif command == '1':
            req = requests.get(
                f'http://127.0.0.1:5555/change_password/',
                params={
                    'login': input('login: '),
                    'password': input('new password: '),
                }
            )
        elif command == '2':
            req = requests.get(
                f'http://127.0.0.1:5555/change_mail/',
                params={
                    'login': input('login: '),
                    'email': input('new email: '),
                }
            )
        elif command == '3':
            req = requests.get(
                f'http://127.0.0.1:5555/get_password/',
                params={
                    'login': input('login: '),
                }
            )
            print(req.content.decode('UTF-8'))
        elif command == '4':
            req = requests.get(
                f'http://127.0.0.1:5555/get_email/',
                params={
                    'login': input('login: '),
                }
            )
            print(req.content.decode('UTF-8'))
        elif command == '5':
            req = requests.get(
                f'http://127.0.0.1:5555/delete_user/',
                params={
                    'login': input('login: '),
                }
            )
        elif command == '6':
            login = input('login: ')
            folder_path = input('file path: ')
            if not os.path.exists(folder_path):
                print('not found')
                continue
            req_folder = requests.get(
                f'http://127.0.0.1:5555/add_path/',
                params={
                    'login': login,
                    'path': folder_path,
                }
            )
            files = get_metadata(get_files(folder_path))
            for pair in files:
                req_file = requests.get(
                    f'http://127.0.0.1:5555/add_file/',
                    params={
                        'login': login,
                        'folder_path': folder_path,
                        'filename': pair[0],
                        'edit_time': pair[1],
                    }
                )
        elif command == '7':
            break
        else:
            continue
