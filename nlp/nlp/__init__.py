import flask
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)

# Read settings from config module (insta485/config.py)
app.config.from_object('nlp.config')

import nlp.api