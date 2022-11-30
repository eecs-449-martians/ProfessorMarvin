import flask

print("importing")


print("starting app:orchestrator")
app = flask.Flask(__name__)
app.config.from_object("pdf.config")
print("app started")

from orchestrator.api.orchestrator import *
from orchestrator.storage.stored_state import Documents

documents = Documents()


# def has_no_empty_params(rule):
#     defaults = rule.defaults if rule.defaults is not None else ()
#     arguments = rule.arguments if rule.arguments is not None else ()
#     return len(defaults) >= len(arguments)


# def list_site_map():
#     links = []
#     for rule in app.url_map.iter_rules():
#         # Filter out rules we can't navigate to in a browser
#         # and rules that require parameters
#         if "GET" in rule.methods and has_no_empty_params(rule):
#             url = url_for(rule.endpoint, **(rule.defaults or {}))
#             links.append((url, rule.endpoint))
