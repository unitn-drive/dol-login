# get request
import requests
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

session = requests.Session()
result = session.get(
    'https://didatticaonline.unitn.it/dol/auth/shibboleth/index.php', allow_redirects=True)

# print(session.url)
location = (session.headers.get('Location'))
jsessionid = (session.cookies.get('JSESSIONID'))
execution = result.url.split('execution=')[1]


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
    "Cookie": "JSESSIONID = "+jsessionid,
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
        'dominio': '@unitn.it'
        }

# get set-cookie field from response (shib_idp_session)
x = session.post(url, headers=headers, data=data, allow_redirects=False)
cookies = session.cookies.get_dict()
print(cookies)


# second post request to didatticaonline
url = 'https://didatticaonline.unitn.it/Shibboleth.sso/SAML2/POST'
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, */*;q=0.8",
    "Accept-Language": "en-US, en",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "18762",
    "Content-Type":	"application/x-www-form-urlencoded",
    "Cookie": "ApplicationGatewayAffinityCORS =" + cookies["ApplicationGatewayAffinityCORS"] + "; ApplicationGatewayAffinity =" + cookies["ApplicationGatewayAffinity"] + "; MoodleSessiondol =" + cookies['MoodleSessiondol'],
    "Host": "didatticaonline.unitn.it",
    "Origin": "https://idp.unitn.it",
    "Referer": "https://idp.unitn.it",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    "Sec-GPC": "1",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0"
}
