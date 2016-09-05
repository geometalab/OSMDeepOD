import urllib.request
from ntlm3 import HTTPNtlmAuthHandler

'''
def process(user, password, url):
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, user, password)

    # create the NTLM authentication handler
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman, debuglevel=0)

    opener = urllib.request.build_opener(auth_NTLM)
    response = opener.open(url)
    urllib.request.install_opener(opener)
    content = response.read()

    print(content)


process('skurath', '..Ib27Ja.!', 'http://maps.hsr.ch/gdi/rest/services/Basisdaten/swissimage/ImageServer')
'''

import requests
from requests_ntlm import HttpNtlmAuth

session = requests.Session()
session.auth = HttpNtlmAuth('hsr\\skurath', '..Ib27Ja.!', session)
result = session.get('http://maps.hsr.ch/gdi/rest/services/Basisdaten/swissimage/ImageServer')

print(result)
