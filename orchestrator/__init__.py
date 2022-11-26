import flask

print("importing")


print("starting app")
app = flask.Flask(__name__)
app.config.from_object("pdf.config")
print("app started")

from orchestrator.api import *
from orchestrator.storage.stored_state import Documents

documents = Documents



