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
        'old_version': '',
        'new_version': '',
        'files': dict()
    }
    for file in fls:
        table['files'][file] = os.stat(file).st_mtime
    return table


def auth():
    # lg = input('Enter login: ')
    lg = 'peter'
    # pwd = input('Enter password: ')
    pwd = 'reh/5e76g'
    request = requests.get(
        f'http://127.0.0.1:5555/auth/',
        params={
            'login': lg,
            'password': pwd,
        }
    )
    return lg, request.content


if __name__ == '__main__':
    if input('Reg? ') == '1':
        req = requests.get(
            f'http://127.0.0.1:5555/add_user/',
            params={
                'login': input('login: '),
                'email': input('email: '),
                'password': input('password: '),
            }
        )

    login, token = auth()

    while True:
        print('Change password - 1\n'
              'Change email - 2\n'
              # 'Get password - 3\n'
              # 'Get email - 4\n'
              'Delete user - 5\n'
              'Add version - 6\n'
              'Update version - 7\n'
              'Delete version - 8\n'
              'Exit - 9')
        command = input('>> ')
        if command == '1':
            req = requests.get(
                f'http://127.0.0.1:5555/change_password/',
                params={
                    'login': login,
                    'password': input('new password: '),
                }
            )
        elif command == '2':
            head = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
            # headers = {'content-type': 'application/json'}
            req = requests.get(
                f'http://127.0.0.1:5555/change_mail/',
                params={
                    'login': login,
                    'email': input('new email: '),
                },
                headers=head
            )
        # elif command == '3':
        #     req = requests.get(
        #         f'http://127.0.0.1:5555/get_password/',
        #         params={
        #             'login': input('login: '),
        #         }
        #     )
        #     print(req.content.decode('UTF-8'))
        # elif command == '4':
        #     req = requests.get(
        #         f'http://127.0.0.1:5555/get_email/',
        #         params={
        #             'login': input('login: '),
        #         }
        #     )
        #     print(req.content.decode('UTF-8'))
        elif command == '5':
            req = requests.get(
                f'http://127.0.0.1:5555/delete_user/',
                params={
                    'login': login,
                }
            )
        # Add version
        elif command == '6':
            folder_path = input('file path: ')
            if not os.path.exists(folder_path):
                print('not found')
                continue
            data = get_json(get_files(folder_path))
            data['login'] = login
            data['mac'] = get_mac()
            data['path_file'] = folder_path
            data['new_version'] = input('version name: ')

            req_file = requests.get(
                f'http://127.0.0.1:5555/add_version/',
                data=json.dumps(data)
            )
        # Update version
        elif command == '7':
            folder_path = input('file path: ')
            if not os.path.exists(folder_path):
                print('not found')
                continue
            o_ver = input('old version name: ')
            n_ver = input('new version name: ')
            data = get_json(get_files(folder_path))
            data['login'] = login
            data['mac'] = get_mac()
            data['path_file'] = folder_path
            data['old_version'] = o_ver
            data['new_version'] = n_ver

            req_file = requests.get(
                f'http://127.0.0.1:5555/update_version/',
                data=json.dumps(data)
            )
        # Delete version
        elif command == '8':
            folder_path = input('file path: ')
            ver = input('version name: ')
            req_file = requests.get(
                f'http://127.0.0.1:5555/delete_version/',
                params={
                    'login': login,
                    'mac': get_mac(),
                    'folder_path': folder_path,
                    'version': ver,
                }
            )
        elif command == '9':
            break
        else:
            continue
