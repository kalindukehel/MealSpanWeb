#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup


def authenticate(username,password):
    with requests.session() as s:
        page = s.get('http://onlineservices.hospitality.uoguelph.ca/')
        soup = BeautifulSoup(page.text,'html5lib')
        request_id = soup.find('input',{'name':'request_id'})['value']
        OAM_REQ = soup.find('input',{'name':'OAM_REQ'})['value']
        payload = {'username':username,'password':password,'request_id':request_id,'OAM_REQ':OAM_REQ}
        logpage = s.post('https://sso2.identity.uoguelph.ca/oam/server/auth_cred_submit',data=payload)
        print(logpage.text)
    if(logpage.url == 'https://onlineservices.hospitality.uoguelph.ca/student/studenthome.cshtml'):
        return('Valid')
    else:
        return('False')
    return('a')
