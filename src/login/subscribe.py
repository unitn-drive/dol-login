from requests import Session, Response
from bs4 import BeautifulSoup as BS
from re import compile
from utils.utils import saveHTML

# tranform course url to the one we need to subscribe


def get_subscription_url(moodleUrl: str) -> str:
    return moodleUrl.replace('/geco/#/public/redirectcorso/', '/api/gestionecorsi/v1/studente/accedicorso/')


def subscribe(session: Session, Bearer_auth: str,  courseUrl: str) -> str:
    courseUrl = get_subscription_url(courseUrl)

    headers = {'Authorization': Bearer_auth}
    res = session.get(courseUrl, headers=headers, allow_redirects=True)
    # returns the url trimming the quotes
    return res.text[1:-1]


def extract_enrolid_from_HTML(res: Response):
    # return res.text.split('enrolid=', 1)[1]
    soup = BS(res.text, 'html.parser')
    try:
        reg = compile(r'Disiscrivimi')
        elements = [e for e in soup.find_all('a') if reg.match(e.text)]
        return elements
    except Exception as e:
        print("Got unhandled exception %s" %
              str(e) + ", while extracting enrolid from: " + res.url)


def unsubscribe(session: Session, Bearer_auth: str, courseUrl: str) -> None:
    res = session.get(courseUrl, allow_redirects=True)

    url = 'https://didatticaonline.unitn.it/dol/loginUniTN.php'
    res = session.get(url, allow_redirects=True)


    # extract location from last request
    location = res.history[-1].headers.get('Location')

    # extract execution number from location
    execution = location.split('execution=')[1]



    url = 'https://idp.unitn.it/idp/profile/SAML2/Redirect/SSO?execution='+execution
    assert res.status_code == 200
    enrolid = extract_enrolid_from_HTML(res)
    print(enrolid)