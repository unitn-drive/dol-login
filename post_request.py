# get request
import requests
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

session = requests.Session()

# get request per ottenere i cookie

session.get('https://didatticaonline.unitn.it/dol/login/index.php', allow_redirects=True)

# get request per ottenere execution id
result = session.get(
    'https://didatticaonline.unitn.it/dol/auth/shibboleth/index.php', allow_redirects=True)

execution = result.url.split('execution=')[1]

# preparo post request per login

url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution

headers = {
    "Host": "idp.unitn.it",
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, */*;q=0.8",
    "Accept-Language": "en-US, en",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "100",
    "Origin": "https://idp.unitn.it",
    "Connection": "keep-alive",
    "Referer": "https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution="+execution,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "TE": "trailers"
}

data = {'j_username': username,
        'j_password': password,
        'dominio': '@unitn.it',
        '_eventId_proceed': ''
        }

# spedisco la post request per login

session.post(url, headers=headers, data=data, allow_redirects=True)

# prova per vedere se ci sono tutti e 4 i cookie
# print(session.cookies.get_dict())

# prova di accesso a una pagina

url = '	https://didatticaonline.unitn.it/dol/course/index.php?categoryid=682'

yy = session.get(url, allow_redirects=True)
print(yy.status_code)
assert yy.status_code == 200

