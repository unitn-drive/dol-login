from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup
from pprint import pprint
load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

session = requests.Session()

# accesso a webapp unitn
webapp_login = session.get(
    'https://webapps.unitn.it/GestioneCorsi/IndexAuth', allow_redirects=True)

# get request per ottenere execution id
result = session.get(
    'https://didatticaonline.unitn.it/dol/auth/shibboleth/index.php', allow_redirects=True)

execution = result.url.split('execution=')[1]

# post request per login
url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
data = {'j_username': username,
        'j_password': password,
        'dominio': '@unitn.it',
        }
r = session.post(url, data=data, allow_redirects=False)

# save html
with open('list_file.html', 'w') as file:
    file.write(r.text)


# second post request to idsrv.unitn.it (Acs)
url = 'idsrv.unitn.it/sts/identity/saml2service/Acs'
# add to data SAMLResponse, RelayState

# ritorno alla pagina gestione corsi


# accesso a didattica online unitn tramite idp

# get request per ottenere i cookie
session.get('https://didatticaonline.unitn.it/dol/login/index.php',
            allow_redirects=True)

# get request per ottenere execution id
result = session.get(
    'https://didatticaonline.unitn.it/dol/auth/shibboleth/index.php', allow_redirects=True)

execution = result.url.split('execution=')[1]

# post request per login
url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
data = {'j_username': username,
        'j_password': password,
        'dominio': '@unitn.it',
        }
session.post(url, data=data, allow_redirects=False)

# link lista corsi DISI
# url = 'https://didatticaonline.unitn.it/dol/course/index.php?categoryid=682'


# prova di accesso a una pagina

url = 'https://didatticaonline.unitn.it/dol/enrol/index.php?id=36549'

yy = session.get(url, allow_redirects=True)

# print(yy.text)
assert yy.status_code == 200

# tentativo di accesso a pagina  'https://webapps.unitn.it/gestionecorsi/' con post request
url = 'https://webapps.unitn.it/gestionecorsi/'
gestione_corsi = session.post(url, data=data, allow_redirects=True)
