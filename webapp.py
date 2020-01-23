#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
import login

app = Flask(__name__)

#def authenticate(username,password):


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/",methods=['POST'])
def form_post():
    username = request.form['username']
    password = request.form['password']
    #authenticate(username,password)
    bal = login.authenticate(username,password)
    return render_template('balance.html',balance=bal)


if __name__ == '__main__':  #if run with python $ python webapp.py     then it runs with debug mode on
    app.run(debug=True)
