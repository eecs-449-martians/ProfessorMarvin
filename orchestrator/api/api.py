# flask api for orchestrator 

import orchestrator
import flask
from flask import request
from werkzeug.utils import secure_filename
import os
import json 

PDF_API_CALL     = 'curl -X POST -F file=@{}  http://localhost:{}/pdf/to_text > {}'
SUMMARY_API_CALL = "curl -X POST http://127.0.0.1:8000/nlp/summary -H 'Content-Type: application/json' -d {json} > {}"
QUESTION_API_CALL = "curl -X POST http://127.0.0.1:8000/nlp/genqa2 -H 'Content-Type: application/json' -d {json} > {}"


@orchestrator.app.route("/orch/upload_file", methods=["POST"])
def ingest_file(): 
	print(' ingesting file')
	
	# get file path
	file = request.files["file"]
	filename = secure_filename(file.filename)
	filepath = os.path.join(os.environ["UPLOAD_FOLDER"], filename)
	file.save(filepath)

	# call pdf thing 
	targ_path = os.path.join(os.environ["UPLOAD_FOLDER"], f'{filename}_text.json')
	command = PDF_API_CALL.format(filepath,8001,targ_path)
	os.system(command)
	# read output json 
	with open(targ_path,'r') as file: 
		pdf_texts = json.load(file)
	print(pdf_texts)
	if pdf_texts['Status'] != "Success": 
		return flask.jsonify(Success=False)

	passages = pdf_texts['text segments']

	# Run text understanding 
	summ_path = os.path.join(os.environ["UPLOAD_FOLDER"], f'temp_summ.json')
	qagen_path = os.path.join(os.environ["UPLOAD_FOLDER"], f'temp_qagen.json')
	for passage in passages: 
		text_json = flask.jsonify(text=passage)
		# call summary 
		command = SUMMARY_API_CALL.format(text_json,summ_path)
		print(command)
		os.system(command)

		# call QAgen
		command = QUESTION_API_CALL.format(text_json,qagen_path)
		print(command)
		os.system(command)

		# load outputs 
		with open(summ_path, 'r') as file:
			summary_json = json.load(file)
			print(summary_json)
		with open(qagen_path, 'r') as file:
			qagen_json = json.load(file)
			print(qagen_json)

		questions = qagen_json['qas']
		summary = summary_json['summary']
		print(questions,summary)
		orchestrator.documents.add_passage(name=filename,text=passage,summary=summary,questions=questions)
	
	# Inputs: PDF file in requests object 	
	# Outputs: {Success: (True, False)}
	return flask.jsonify(Success=True,curr_state=orchestrator.documents.to_dict()) 

@orchestrator.app.route("/", methods=["GET"])
def get_question(): 
	print('getting question ')
	"""
	Get question
	Inputs: {"Query": text } (describing goal) 
	return format  {dict: 
					success(True, False), 
					Outputs: {Question: text, Answer:text}} """
	query = flask.request.get_json()["Query"]
	question = orchestrator.documents.get_question(query)
	if question is None: 
		return flask.jsonify(Success=False,Question = None )
	return flask.jsonify(Success=True,Question=question)


@orchestrator.app.route("/orch/get_summ/", methods=["GET"])
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
		return flask.jsonify(Success=False,Summary = None )
	return flask.jsonify(Success=True,Summary=summary)



@orchestrator.app.route("/orch/delete_file/", methods=["Post"])
def delte_file():
	"""
	Inputs: {"filename": text } (exact name of file) 
	return format  {dict: 
					  success: (True, False) 
					}
					"""
	return flask.jsonify(Success= orchestrator.documents.delete_doc() ) 


@orchestrator.app.route("/orch/get_passage/", methods=["GET"])
def get_passage(): 
	query = flask.request.get_json()["Query"]
	passage = orchestrator.documents.get_passage(query)
	if passage is None: 
		return flask.jsonify(Success=False,Text = None )
	return flask.jsonify(Success=True,Text=passage)


