from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup as BS


load_dotenv()
username = os.getenv('username')
password = os.getenv('password')
session = requests.Session()
# print("Username and password:", username, password)

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
# post for SAMLResponse, RelayState
url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
data = {'j_username': username,
        'j_password': password,
        'dominio': '@unitn.it',
        '_eventId_proceed': ''}

res = session.post(url, data=data, allow_redirects=True)

# extract SAMLResponse from last request
soup = BS(res.text, 'html.parser')
try:
    tokenRelayState = soup.find('input', {'name': 'RelayState'}).get('value')
    tokenSAMLResponse = soup.find(
        'input', {'name': 'SAMLResponse'}).get('value')
except Exception as e:
    print("Got unhandled exception %s" %
          str(e) + ", while extracting from: " + res.url)


# post to idsrv.unitn.it with tokens(Acs)
url = 'https://idsrv.unitn.it/sts/identity/saml2service/Acs'
data = {'RelayState': tokenRelayState, 'SAMLResponse': tokenSAMLResponse}
res = session.post(url, data=data, allow_redirects=True)

# extract next post url, code, id_token, scope, state, session_state
soup = BS(res.text, 'html.parser')
try:
    url = soup.find('form').get('action')
    code = soup.find('input', {'name': 'code'}).get('value')
    id_token = soup.find('input', {'name': 'id_token'}).get('value')
    scope = soup.find('input', {'name': 'scope'}).get('value')
    state = soup.find('input', {'name': 'state'}).get('value')
    session_state = soup.find('input', {'name': 'session_state'}).get('value')
except Exception as e:
    print("Got unhandled exception %s" %
          str(e) + ", while extracting from: " + res.url)

# callback with tokens to webapps.unitn.it/GestioneCorsi/callback (maybe)
data = {'code': code, 'id_token': id_token, 'scope': scope,
        'state': state, 'session_state': session_state}
res = session.post(url, data=data, allow_redirects=True)

# extract authorization Bearer token to get courses
soup = BS(res.text, 'html.parser')
script_with_auth = soup.findAll('script')[9]
auth = str(script_with_auth).split('Bearer ', 1)[1].split('"')[0]


# get attended courses
url = 'https://webapps.unitn.it/api/gestionecorsi/v1/studente/corsi/'
headers = {'Authorization': 'Bearer ' + auth}
res = session.get(url, headers=headers, allow_redirects=True)

# save json
with open('attended_courses.json', 'w') as file:
    file.write(res.text)

# get aviable courses
url = 'https://webapps.unitn.it/api/gestionecorsi/v1/studente/possibilicorsi/'
headers = {'Authorization': 'Bearer ' + auth}
res = session.get(url, headers=headers, allow_redirects=True)

# save json
with open('aviable_courses.json', 'w') as file:
    file.write(res.text)

# # save html
# with open('response_post.html', 'w') as file:
#     file.write(res.text)

# # print history of requests
# for i in res.history:
#     print(i.status_code, i.url)
# print(res.url)
