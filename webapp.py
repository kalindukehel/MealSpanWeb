#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
import login

app = Flask(__name__)

#def authenticate(username,password):


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/balance",methods=['GET','POST'])
def form_post():
    if(request.method == 'GET'):
        back = url_for('home')
        return ("<a href="+ back+'>'+"a</a>")
    elif(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        date = request.form['date']
        #authenticate(username,password)
        basic,flex,statuscode = login.authenticate(username,password)
        if(statuscode == 1):
            return render_template('balance.html',basic= '0',flex='0',spend=0)
        else:
            spending = login.calculatespending(basic,flex,date)
            return render_template('balance.html',basic = basic, flex=flex,spend=spending)


if __name__ == '__main__':  #if run with python $ python webapp.py     then it runs with debug mode on
    app.run(debug=True)
