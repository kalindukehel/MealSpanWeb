#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from datetime import date,datetime
import numpy as np
import re

def authenticate(username,password):
    basic = ''
    flex = ''
    with requests.session() as s:
        #using requests to log into hospitality website
        page = s.get('http://onlineservices.hospitality.uoguelph.ca/')
        soup = BeautifulSoup(page.text,'html.parser')
        request_id = soup.find('input',{'name':'request_id'})['value']
        OAM_REQ = soup.find('input',{'name':'OAM_REQ'})['value']
        payload = {'username':username,'password':password,'request_id':request_id,'OAM_REQ':OAM_REQ}
        logPage = s.post('https://sso.identity.uoguelph.ca/oam/server/auth_cred_submit',data=payload)
        statuscode = 1
        mp = ['',0,0]
        mpTypes = [('Minimum',728,665),('Light',840,805),('Full',915,910),('Plus',1025,980),('Varsity',1099,1015),('Over',0,0)]
        #if prompted to choose between student and staff
        if(logPage.url == 'https://onlineservices.hospitality.uoguelph.ca/secure/choosestatus.cshtml?url=/secure/forceuserlogin.cshtml?'):
            studentPayload = {'status': 'student','login_submit': 'Sign In'}
            logPage = s.post('https://onlineservices.hospitality.uoguelph.ca/secure/forceuserlogin.cshtml?url=/secure/forceuserlogin.cshtml?',data=studentPayload)
        if('onlineservices.hospitality.uoguelph.ca/student/studenthome' in logPage.url):
            statuscode = 0
            balPage = s.get('https://onlineservices.hospitality.uoguelph.ca/secure/onlineinquiry.cshtml')
            balSoup = BeautifulSoup(balPage.text,'html.parser')
            #scraping basic and flex balance from parsed webpage
            try:
                basic = balSoup.find_all('td',{'align':'left'})[3].text[1:]
            except IndexError:
                basic = '0'
            try:
                flex = balSoup.find_all('td',{'align':'left'})[5].text[1:]
            except IndexError:
                flex = '0'

            #checking if the plan is carry over
            try:
                mp[0] = balSoup.find_all('a',href=re.compile("./detailview"))[0].text.split(" ")[1]
                mealplan_name = balSoup.find_all('a',href=re.compile("./detailview"))[0].text
                residence_meal_plan = False
                for i in range(5):
                    if(mpTypes[i][0] == mp[0]):
                        mp[1],mp[2] = mpTypes[i][1],mpTypes[i][2]
                        residence_meal_plan = True
                if(not residence_meal_plan):
                    mp[1],mp[2] = float(basic.replace(',','')),float(flex.replace(',',''))
                    mp[0] = mealplan_name
            except IndexError:
                mp[0] = ''
            s.get('https://onlineservices.hospitality.uoguelph.ca/logout.cshtml')
        else:
            statuscode = 1

    return(basic,flex,statuscode,mp)

def calculatespending(basic,flex,endDate,exclude):
    #calculating recommended spending by dividing days by total money
    total = float(basic.replace(',','')) + (float(flex.replace(',','')))
    endDateSplit = endDate.split('-')
    secondDate = date(int(endDateSplit[0]),int(endDateSplit[1]),int(endDateSplit[2]))
    firstDate = date.today()
    if (exclude == True):
        diff = np.busday_count(firstDate,secondDate)+ 1
    else:
        diff = (secondDate-firstDate).days
    return round(total/diff,2)
