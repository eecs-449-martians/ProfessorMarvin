import flask
from flask import Flask

print("Chatbot starting")
app = flask.Flask(__name__)
app.config.from_object("chatbot.config")
print("Chatbot started")

from chatbot.api import *
