from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup as BS
import json


# get username and password input
def input(env: str):
    load_dotenv(dotenv_path=env)
    username = os.getenv('username')
    password = os.getenv('password')

    if username == "" or password == "" or username == None or password == None:
        raise ValueError('Fill your username and password in .env')

    return username, password

# clean json courses list


def clean_json_list(json_list):
    # removing multi language substring and setting url of each course
    for i in json_list:
        if 'target=' not in i['urlMoodle']:
            json_list.remove(i)
        else:
            if '{mlang other}' in i['fullName']:
                i['fullName'] = i['fullName'].split('{mlang other}', 1)[
                    1].split('{mlang}', 1)[0]
            i['url'] = i['urlMoodle'].split('target=', 1)[1]

    return json_list

# function to save HTML text to a file


def saveHTML(name, res):
    with open(name + '.html', 'w') as file:
        file.write(res.text)

# function to save json text to a file


def saveJSON(name, data):
    with open(name + '.json', 'w') as file:
        json.dump(data, file, indent=4)

# extract relay state token from html


def extract_RelayState_from_HTML(res):
    soup = BS(res.text, 'html.parser')
    try:
        return soup.find('input', {'name': 'RelayState'}).get('value')
    except Exception as e:
        print("Got unhandled exception %s" %
              str(e) + ", while extracting RelayState from: " + res.url)

# extract SAML response token from html


def extract_SAMLResponse_from_HTML(res):
    soup = BS(res.text, 'html.parser')
    try:
        return soup.find('input', {'name': 'SAMLResponse'}).get('value')
    except Exception as e:
        print("Got unhandled exception %s" %
              str(e) + ", while extracting SAMLResponse from: " + res.url)

# function to login that return (session, Bearer_auth, tokenRelayState, tokenSAMLResponse, data)


def login(username, password):
    session = requests.Session()

    # accesso a webapp unitn
    res = session.get(
        'https://webapps.unitn.it/GestioneCorsi/IndexAuth', allow_redirects=True)

    # extract RelyState from last request
    # relayState = res.history[-1].url.split('RelayState=')[1]

    # extract location from last request
    location = res.history[-1].headers.get('Location')

    # extract execution number from location
    execution = location.split('execution=')[1]

    # post for SAMLResponse, RelayState
    url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
    data = {'j_username': username,
            'j_password': password,
            'dominio': '@unitn.it',
            '_eventId_proceed': ''}

    res = session.post(url, data=data, allow_redirects=True)

    # saveHTML('DEBUG_POST_REQ', res)

    # extract RelayState and SAMLResponse from last request
    tokenRelayState = extract_RelayState_from_HTML(res)
    tokenSAMLResponse = extract_SAMLResponse_from_HTML(res)

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
    Bearer_auth = 'Bearer ' + auth
    return (session, Bearer_auth, tokenRelayState, tokenSAMLResponse, data)

# function to get json list of attended courses


def get_attended_courses(session, auth):
    url = 'https://webapps.unitn.it/api/gestionecorsi/v1/studente/corsi/'
    headers = {'Authorization': auth}
    res = session.get(url, headers=headers, allow_redirects=True)

    # output list of courses
    json_list = res.json()
    return clean_json_list(json_list)


# function to get json list of available courses


def get_available_courses(session, auth):
    url = 'https://webapps.unitn.it/api/gestionecorsi/v1/studente/possibilicorsi/'
    headers = {'Authorization': auth}
    res = session.get(url, headers=headers, allow_redirects=True)
    # output list of courses
    json_list = res.json()
    return json_list


# get course content
def get_course_content(session, auth, url):
    res = session.get(
        url, headers={'Authorization': auth}, allow_redirects=True)
    return True


# def scrape(env: str,
#            list_enrolled: bool,
#            list_available: bool) -> None:


#     #get_attended_courses(session, auth)
#     json = get_available_courses(session, auth)

#     # print_courses_list(list)

#     # visiting first course
#     course = json[0]

#     # ACTUALLY THE SECOND AUTHENTICATION
#     res = session.get(course['urlMoodle'], allow_redirects=True)

#     # extract RelayState and SAMLResponse from last request
#     tokenRelayState = extract_RelayState_from_HTML(res)
#     tokenSAMLResponse = extract_SAMLResponse_from_HTML(res)

#     # post to dol with tokens
#     url = 'https://didatticaonline.unitn.it/Shibboleth.sso/SAML2/POST'
#     data = {'RelayState': tokenRelayState, 'SAMLResponse': tokenSAMLResponse}
#     res = session.post(url, data=data, allow_redirects=True)

#     # should be redirected to course page
#     print(res.url)


# # print courses names
# for i in json:
#     print(i['fullName'])
#     print()

# # print history of requests
# for i in res.history:
#     print(i.status_code, i.url)
# print(res.url)
