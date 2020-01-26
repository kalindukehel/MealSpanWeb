#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from datetime import date,datetime
import numpy as np

def authenticate(username,password):
    basic = ''
    flex = ''
    with requests.session() as s:
        page = s.get('http://onlineservices.hospitality.uoguelph.ca/')
        soup = BeautifulSoup(page.text,'html.parser')
        request_id = soup.find('input',{'name':'request_id'})['value']
        OAM_REQ = soup.find('input',{'name':'OAM_REQ'})['value']
        payload = {'username':username,'password':password,'request_id':request_id,'OAM_REQ':OAM_REQ}
        logpage = s.post('https://sso2.identity.uoguelph.ca/oam/server/auth_cred_submit',data=payload)
        print(logpage.url)
        statuscode = 1
        if(logpage.url == 'https://onlineservices.hospitality.uoguelph.ca/student/studenthome.cshtml'):
            statuscode = 0
            balpage = s.get('https://onlineservices.hospitality.uoguelph.ca/secure/onlineinquiry.cshtml')
            balsoup = BeautifulSoup(balpage.text,'html.parser')
            basic = balsoup.find_all('td',{'align':'left'})[3].text[1:]
            flex = balsoup.find_all('td',{'align':'left'})[5].text[1:]
        else:
            statuscode = 1

    return(basic,flex,statuscode)

def calculatespending(basic,flex,enddate,exclude):
    total = float(basic.replace(',','')) + (float(flex.replace(',','')))
    enddatesplit = enddate.split('-')
    d2 = date(int(enddatesplit[0]),int(enddatesplit[1]),int(enddatesplit[2]))
    d1 = date.today()
    if (exclude == True):
        diff = np.busday_count(d1,d2)+ 1
    else:
        diff = (d2-d1).days
    return round(total/diff,2)
