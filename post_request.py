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

data = {'j_username': username,
        'j_password': password,
        'dominio': '@unitn.it',
        }

# spedisco la post request per login

session.post(url, data=data, allow_redirects=True)

# prova di accesso a una pagina

url = '	https://didatticaonline.unitn.it/dol/course/index.php?categoryid=682'

yy = session.get(url, allow_redirects=True)
print(yy.status_code)
assert yy.status_code == 200

