from requests import Session
from login.login import extract_RelayState_from_HTML, extract_SAMLResponse_from_HTML

sampleCourse = 'https://webapps.unitn.it/geco/#/public/redirectcorso/2022|91290|1|N0|75022'

def subscribe(session: Session, course: str):
    # test
    course = sampleCourse
    # end test

    # ACTUALLY THE SECOND AUTHENTICATION
    res = session.get(sampleCourse, allow_redirects=True)
    
    # extract RelayState and SAMLResponse from last reques
    tokenRelayState = extract_RelayState_from_HTML(res)
    tokenSAMLResponse = extract_SAMLResponse_from_HTML(res)

    # post to dol with tokens
    url = 'https://didatticaonline.unitn.it/Shibboleth.sso/SAML2/POST'
    data = {'RelayState': tokenRelayState, 'SAMLResponse': tokenSAMLResponse}
    res = session.post(url, data=data, allow_redirects=True)

    # should be redirected to course page
    print(res.url)


