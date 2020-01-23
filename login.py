#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup


def authenticate(username,password):
    basic = ''
    flex = ''
    with requests.session() as s:
        page = s.get('http://onlineservices.hospitality.uoguelph.ca/')
        soup = BeautifulSoup(page.text,'html5lib')
        request_id = soup.find('input',{'name':'request_id'})['value']
        OAM_REQ = soup.find('input',{'name':'OAM_REQ'})['value']
        payload = {'username':username,'password':password,'request_id':request_id,'OAM_REQ':OAM_REQ}
        logpage = s.post('https://sso2.identity.uoguelph.ca/oam/server/auth_cred_submit',data=payload)
        print(logpage.url)
        statuscode = 1
        if(logpage.url == 'https://onlineservices.hospitality.uoguelph.ca/student/studenthome.cshtml'):
            statuscode = 0
            balpage = s.get('https://onlineservices.hospitality.uoguelph.ca/secure/onlineinquiry.cshtml')
            balsoup = BeautifulSoup(balpage.text,'html5lib')
            basic = balsoup.find_all('td',{'align':'left'})[3].text
            flex = balsoup.find_all('td',{'align':'left'})[5].text
        else:
            statuscode = 1

    return(basic,flex,statuscode)