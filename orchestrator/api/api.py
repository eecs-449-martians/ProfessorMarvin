# flask api for orchestrator 

import flask 
from flask import requests 



@orchestrator.app.route("/orch/upload_file/", methods=["POST"])
def ingest_file(): 
	# link frontend and pdf handling 
	# get back info from pdf handling 
	# passes through pdf understanding 
	# saves to storage 
	# Inputs: PDF file in requests object 
	# Outputs: {Success: (True, False)}
	...

@orchestrator.app.route("/orch/get_question/", methods=["GET"])
def get_question(): 
	# Query storage for questions
	# Inputs: {"Query": text } (describing goal) 
	# return format  {dict: 
	# 				  success(True, False), 
	# 				  Outputs: {Question: text, Answer:text}}

@orchestrator.app.route("/orch/get_summ/", methods=["GET"])
def get_summary(): 
	# Inputs: {"Query": text } (describing goal) 
	# return format  {dict: 
	# 				  success: (True, False), 
	# 				  Summary: Text }
	...

@orchestrator.app.route("/orch/delete_file/", methods=["Post"])
def delte_file():
	# Inputs: {"filename": text } (exact name of file) 
	# return format  {dict: 
	# 				  success: (True, False), 


# @pdf.app.route("/orch/get_passage/", methods=["GET"])
# def get_passage(): 
# 	... 


