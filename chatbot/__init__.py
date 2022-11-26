from flask import Flask

print("Chatbot starting")
Flask(__name__)
app.config.from_object("chatbot.config")
print("Chatbot started")

from chatbot import *
