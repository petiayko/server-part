import requests
import os
import json
from sys import platform
import uuid


def get_mac():
    mac_adr = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_adr[i:i + 2] for i in range(0, 11, 2))
    return platform + '_' + mac


def get_files(path_file):
    fls = []
    for file in os.listdir(path_file):
        if os.path.isfile(path_file + '/' + file):
            fls.append(path_file + '/' + file)
        elif os.path.isdir(path_file + '/' + file):
            fls += get_files(path_file + '/' + file)
    return fls


def get_json(fls):
    table = {
        'login': '',
        'mac': '',
        'path_file': '',
        'version': '',
        'files': dict()
    }
    for file in fls:
        table['files'][file] = os.stat(file).st_mtime
    return table


if __name__ == '__main__':
    while True:
        print('Reg - 0\n'
              'Change password - 1\n'
              'Change email - 2\n'
              'Get password - 3\n'
              'Get email - 4\n'
              'Delete user - 5\n'
              'Add version - 6\n'
              'Update version - 7\n'
              'Exit - 8')
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

        # Add version
        elif command == '6':
            login = input('login: ')
            folder_path = input('file path: ')
            if not os.path.exists(folder_path):
                print('not found')
                continue
            data = get_json(get_files(folder_path))
            data['login'] = login
            data['mac'] = get_mac()
            data['path_file'] = folder_path
            data['version'] = input('version name: ')

            req_file = requests.get(
                f'http://127.0.0.1:5555/add_version/',
                data=json.dumps(data)
            )

        # Update version
        elif command == '7':
            login = input('login: ')
            folder_path = input('file path: ')
            if not os.path.exists(folder_path):
                print('not found')
                continue
            ver = input('old version name: ')
            data = get_json(get_files(folder_path))
            data['login'] = login
            data['mac'] = get_mac()
            data['path_file'] = folder_path
            data['version'] = ver

            req_file = requests.get(
                f'http://127.0.0.1:5555/update_folder/',
                data=json.dumps(data)
            )

        elif command == '8':
            break
        else:
            continue
