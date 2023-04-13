from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup
from pprint import pprint
load_dotenv()

webapp_url = 'https://webapps.unitn.it'
dol_url = 'https://didatticaonline.unitn.it/dol'
idp_url = 'https://idp.unitn.it'
idsrv_url = 'https://idsrv.unitn.it'

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
session = requests.Session()

# accesso a webapp unitn
# accesso a webapp unitn
res = session.get(
    'https://webapps.unitn.it/GestioneCorsi/IndexAuth', allow_redirects=True)

# extract RelyState from last request
relayState = res.history[-1].url.split('RelayState=')[1]

# extract location from last request
location = res.history[-1].headers.get('Location')

# extract execution number from location
execution = location.split('execution=')[1]

cookies = session.cookies.get_dict()
# post for SAMLResponse, RelayState (don't need headers)
url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
data = {'j_username': username,
        'j_password': password,
        'dominio': '@unitn.it',
        '_eventId_proceed': ''}
res = session.post(url, data=data, allow_redirects=True)

# save html
with open('response_post.html', 'w') as file:
    file.write(res.text)


# # print history of requests
# for i in res.history:
#     print(i.status_code, i.url)
# print(res.url)
