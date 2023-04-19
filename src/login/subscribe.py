from requests import Session

# tranform course url to the one we need to subscribe
def get_subscription_url(moodleUrl: str) -> str:
    return moodleUrl.replace('/geco/#/public/redirectcorso/', '/api/gestionecorsi/v1/studente/accedicorso/')

def subscribe(session: Session, Bearer_auth: str,  courseUrl: str) -> str:
    courseUrl = get_subscription_url(courseUrl)

    headers = {'Authorization': Bearer_auth}
    res = session.get(courseUrl, headers=headers, allow_redirects=True)
    # returns the url trimming the quotes
    return res.text[1:-1]


