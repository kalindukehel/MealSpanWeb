#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
import math
import login

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/balance",methods=['GET','POST'])
def form_post():
    if(request.method == 'GET'): #reprompt user if bal page accessed without form data
        back = url_for('home')
        return ("<a href="+ back+'>'+"Click here to log-in again.</a>")
    elif(request.method == 'POST'):
        #sending form data to generate balance page
        username = request.form['username']
        password = request.form['password']
        date = request.form['date']
        exclude = 'exclude' in request.form
        basic,flex,statusCode,mp = login.authenticate(username,password)
        if(statusCode == 1):
            return ("Invalid username/password <a href="+ url_for('home')+'>'+"click here</a> to try again.")
        else:
            spending = login.calculatespending(basic,flex,date,exclude)
            basic_width = 0
            if (float(basic) != 0):
                basic_width = float((basic.replace(',','')))/(int(math.ceil(float(mp[1])))+int(mp[2]))*100
            flex_width = 0
            if (float(flex) != 0):
                flex_width = float((flex.replace(',','')))/(int(mp[1])+int(math.ceil(float(mp[2]))))*100
            return render_template('balance.html',basic = basic, flex=flex,spend=spending, plan = mp[0],total=(mp[1] + mp[2]),username=username, basicwidth = basic_width, flexwidth = flex_width)


if __name__ == '__main__':  #if run with python $ python webapp.py     then it runs with debug mode on
    app.run(debug=True)
