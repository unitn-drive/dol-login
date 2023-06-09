from requests import Session, Response
from bs4 import BeautifulSoup as BS
from re import compile
from utils.utils import saveHTML
from login.login import login_dol

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
    return res.text.split('enrolid=', 1)[1].split('"')[0]


def extract_sesskey_from_HTML(res: Response):
    return res.text.split('sesskey":"', 1)[1].split('"')[0]


def unsubscribe(session: Session, courseUrl: str) -> None:
    res = session.get(courseUrl, allow_redirects=True)

    # extract enrolid and sesskey from HTML

    # try catch to handle the case where the user is not enrolled
    # and we cannot find the enrolid
    # warning, potential infinite loop
    enrolid = None
    try:
        enrolid = extract_enrolid_from_HTML(res)
    except Exception as e:
        login_dol(session)
        unsubscribe(session, courseUrl)

    sesskey = extract_sesskey_from_HTML(res)
    url = 'https://didatticaonline.unitn.it/dol/enrol/manual/unenrolself.php'
    data = {
        'enrolid': enrolid,
        'confirm': '1',
        'sesskey': sesskey,
    }
    res = session.post(url, data=data, allow_redirects=True)
