import requests

if __name__ == '__main__':
    a = int(input('>> '))
    b = int(input('>> '))
    op = input('>> ')
    req = requests.get(f'http://127.0.0.1:5555/{op}/', params={'a': a, 'b': b})
    print(req.content.decode('UTF-8'))
