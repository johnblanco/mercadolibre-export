import json
import requests


def main():
    secrets = json.loads(open('secrets.json', 'r').read())

    client_id = secrets['client_id']
    client_secret = secrets['client_secret']
    code = secrets['code']

    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': 'https://google.com',
    }

    res = requests.post('https://api.mercadolibre.com/oauth/token', data=data).json()
    access_token = res['access_token']

    secrets['access_token'] = access_token
    open('secrets.json', 'w').write(json.dumps(secrets))


if __name__ == "__main__":
    main()
