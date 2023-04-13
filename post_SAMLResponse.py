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

# # print history of requests
# for i in res.history:
#     print(i.url)

# extract RelyState from last request
relayState = res.history[-1].url.split('RelayState=')[1]

# extract location from last request
location = res.history[-1].headers.get('Location')

# extract execution number from location
execution = location.split('execution=')[1]

# last get (redirect) request
res = session.get(idp_url + location, allow_redirects=True)

cookies = session.cookies.get_dict()
# post for SAMLResponse, RelayState
url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
data = {'j_username': username,
        'j_password': password,
        'dominio': '@unitn.it'}
headers = {"Host": "idp.unitn.it",
           "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, */*;q=0.8",
           "Accept-Language": "en-US, en",
           "Accept-Encoding": "gzip, deflate, br",
           "Content-Type": "application/x-www-form-urlencoded",
           "Content-Length": "100",
           "Cookie": "JSESSIONID=" + cookies['JSESSIONID'] + "; cookie-agreed-version=1.0.1",
           "Origin": "https://idp.unitn.it",
           "Connection": "keep-alive",
           "Referer": "https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution="+execution,
           "Upgrade-Insecure-Requests": "1",
           "Sec-Fetch-Dest": "document",
           "Sec-Fetch-Mode": "navigate",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-User": "?1",
           "Sec-GPC": "1",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0",
           "TE": "trailers"
           }

res = session.post(url, data=data, headers=headers, allow_redirects=False)
print(res.text)
