import flask
import spacy
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer
from nlp.qg import pipelines

print("Initializing server...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Summarizer loaded")
qagen_model = pipelines.pipeline("question-generation", model="valhalla/t5-base-qg-hl")
print("qagen model loded")
print("NLP server initialized")
# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)

# Read settings from config module (insta485/config.py)
app.config.from_object("nlp.config")

import nlp.api
import nlp.qg
