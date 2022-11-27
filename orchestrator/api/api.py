# flask api for orchestrator

import orchestrator
import flask
from flask import request, url_for
from werkzeug.utils import secure_filename
import os
import json

#PDF_API_CALL = "curl -X POST -F file=@'{}'  http://localhost:{}/pdf/to_text > '{}'"
PDF_API_CALL = "curl -X POST http://localhost:{}/pdf/to_text -H 'Content-Type: application/json' -d '{}' > '{}'"
SUMMARY_API_CALL = "curl -X POST http://127.0.0.1:8000/nlp/summary -H 'Content-Type: application/json' -d '{}' > {}"
QUESTION_API_CALL = "curl -X POST http://localhost:8000/nlp/genqa  -H 'Content-Type: application/json' -d '{}' > {}"


@orchestrator.app.route("/orch/upload_file", methods=["POST"])
def ingest_file():
    """ Takes JSON body with 2 values: url and filename for pdf to process"""
    print(" ingesting file")

    # get file path
    filepath = request.get_json()['url']
    filename = request.get_json()['filename']
    # file = request.files["file"]
    # print("Just got a file called", file.filename)
    # filename = secure_filename(file.filename)
    # filepath = os.path.join(os.environ["PDF_FOLDER"], filename)
    #file.save(filepath)

    print(filepath,filename)

    # call pdf thing
    targ_path = os.path.join(os.environ["UPLOAD_FOLDER"], f"{filename}_text.json")
    print("saving plaintext to", str(targ_path))
    url_json = json.dumps({'url': filepath})
    # filepath = url of pdf file to turn to plaintext, targ_path = where to save response json
    command = PDF_API_CALL.format(8001, url_json, targ_path)
    print("Making a call to", command)
    os.system(command)
    # read output json
    with open(targ_path, "r") as file:
        pdf_texts = json.load(file)
    print(pdf_texts)
    if pdf_texts["Status"] != "Success":
        return flask.jsonify(Success=False)

    passages = pdf_texts["text segments"]

    # Run text understanding
    summ_path = os.path.join(os.environ["UPLOAD_FOLDER"], f"temp_summ.json")
    qagen_path = os.path.join(os.environ["UPLOAD_FOLDER"], f"temp_qagen.json")
    for passage in passages:
        print(passage)
        text_json = json.dumps({"text": passage})
        # call summary
        command = SUMMARY_API_CALL.format(text_json, summ_path)
        print(command)
        os.system(command)

        # call QAgen
        command = QUESTION_API_CALL.format(text_json, qagen_path)
        print(command)
        os.system(command)

        # load outputs
        with open(summ_path, "r") as file:
            try:
                summary_json = json.load(file)
                print(summary_json)
            except json.decoder.JSONDecodeError:
                print("error encountered in SUMMARY step")
                continue

        with open(qagen_path, "r") as file:
            try:
                qagen_json = json.load(file)
                print(qagen_json)
            except json.decoder.JSONDecodeError:
                print("error encountered in QAGEN step")
                qagen_json = {"qas": []}

        questions = qagen_json["qas"]
        summary = summary_json["summary"]
        print(questions, summary)
        orchestrator.documents.add_passage(
            name=filename, text=passage, summary=summary, questions=questions
        )

    # Inputs: PDF file in requests object
    # Outputs: {Success: (True, False)}
    return flask.jsonify(
        Success=True, curr_state=orchestrator.documents.passages.to_dict()
    )


@orchestrator.app.route("/orch/get_question", methods=["GET"])
def get_question():
    print("getting question ")
    """
	Get question
	Inputs: {"Query": text } (describing goal) 
	return format  {dict: 
					success(True, False), 
					Outputs: {Question: text, Answer:text}} """
    query = flask.request.get_json()["Query"]
    question = orchestrator.documents.get_question(query)
    if question is None:
        return flask.jsonify(Success=False, Question=None)
    return flask.jsonify(Success=True, Question=question)


@orchestrator.app.route("/orch/get_summ", methods=["GET"])
def get_summary():
    """
    Get summary from group
    Inputs: {"Query": text } (describing goal)
    return format  {dict:
                                success: (True, False),
                                    Summary: Text }
    """
    query = flask.request.get_json()["Query"]
    summary = orchestrator.documents.get_summary(query)
    if summary is None:
        return flask.jsonify(Success=False, Summary=None)
    return flask.jsonify(Success=True, Summary=summary)


@orchestrator.app.route("/orch/delete_file", methods=["Post"])
def delte_file():
    """
    Inputs: {"filename": text } (exact name of file)
    return format  {dict:
                                      success: (True, False)
                                    }
    """
    fname = flask.request.get_json()["filename"]

    return flask.jsonify(Success=orchestrator.documents.delete_doc(fname))


@orchestrator.app.route("/orch/get_passage", methods=["GET"])
def get_passage():
    query = flask.request.get_json()["Query"]
    passage = orchestrator.documents.get_passage(query)
    if passage is None:
        return flask.jsonify(Success=False, Text=None)
    return flask.jsonify(Success=True, Text=passage)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@orchestrator.app.route("/site-map")
def list_site_map():
    links = []
    for rule in orchestrator.app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    return flask.jsonify(map=links)
