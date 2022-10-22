import flask
import spacy
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer
print("Initializing server...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Summarizer loaded")
spacy_model = spacy.load("en_core_web_sm") # can be changed to "en_core_web_md/lg/trf" for better + slower
print("Spacy model loaded")
qg_tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
print("Tokenizer loaded")
qg_model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
print("QG model loaded")

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)

# Read settings from config module (insta485/config.py)
app.config.from_object('nlp.config')

import nlp.api