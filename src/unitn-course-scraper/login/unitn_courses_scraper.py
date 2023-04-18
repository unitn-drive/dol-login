from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup as BS
import json


def saveHTML(name, res):
    with open(name + '.html', 'w') as file:
        file.write(res.text)


def extract_RelayState_from_HTML(res):
    soup = BS(res.text, 'html.parser')
    try:
        return soup.find('input', {'name': 'RelayState'}).get('value')
    except Exception as e:
        print("Got unhandled exception %s" %
              str(e) + ", while extracting RelayState from: " + res.url)


def extract_SAMLRessponse_from_HTML(res):
    soup = BS(res.text, 'html.parser')
    try:
        return soup.find('input', {'name': 'SAMLResponse'}).get('value')
    except Exception as e:
        print("Got unhandled exception %s" %
              str(e) + ", while extracting SAMLResponse from: " + res.url)

# print("Username and password:", username, password)


def scrape(env: str,
           list_enrolled: bool,
           list_available: bool) -> None:

    load_dotenv(dotenv_path=env)
    username = os.getenv('username')
    password = os.getenv('password')

    if username == "" or password == "" or username == None or password == None:
        raise ValueError('Fill your username and password in .env')

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
    # post for SAMLResponse, RelayState
    url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
    data = {'j_username': username,
            'j_password': password,
            'dominio': '@unitn.it',
            '_eventId_proceed': ''}

    res = session.post(url, data=data, allow_redirects=True)

    saveHTML('DEBUG_POST_REQ', res)

    # extract RelayState and SAMLResponse from last request
    tokenRelayState = extract_RelayState_from_HTML(res)
    tokenSAMLResponse = extract_SAMLRessponse_from_HTML(res)

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
        session_state = soup.find(
            'input', {'name': 'session_state'}).get('value')
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

    # # get aviable courses
    # url = 'https://webapps.unitn.it/api/gestionecorsi/v1/studente/possibilicorsi/'
    # headers = {'Authorization': 'Bearer ' + auth}
    # res = session.get(url, headers=headers, allow_redirects=True)

    # # save json
    # with open('aviable_courses.json', 'w') as file:
    #     file.write(res.text)

    # output list of courses
    json = res.json()

    # removing multi language substring and setting url of each course
    for i in json:
        if '{mlang other}' in i['fullName']:
            i['fullName'] = i['fullName'].split('{mlang other}', 1)[
                1].split('{mlang}', 1)[0]
        i['url'] = i['urlMoodle'].split('target=', 1)[1]

    # visiting first course
    course = json[0]

    # ACTUALLY THE SECOND AUTHENTICATION
    res = session.get(course['urlMoodle'], allow_redirects=True)

    # extract RelayState and SAMLResponse from last request
    tokenRelayState = extract_RelayState_from_HTML(res)
    tokenSAMLResponse = extract_SAMLRessponse_from_HTML(res)

    # post to dol with tokens
    url = 'https://didatticaonline.unitn.it/Shibboleth.sso/SAML2/POST'
    data = {'RelayState': tokenRelayState, 'SAMLResponse': tokenSAMLResponse}
    res = session.post(url, data=data, allow_redirects=True)

    # should be redirected to course page
    print(res.url)


# # print courses names
# for i in json:
#     print(i['fullName'])
#     print()

# # print history of requests
# for i in res.history:
#     print(i.status_code, i.url)
# print(res.url)
if __name__ == "__main__":
    scrape()
