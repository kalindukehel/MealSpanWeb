#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route("/")

def home():
    return "<h1>hello world</h1>"
