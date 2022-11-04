import flask 
from flask import request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from pdf.pdf_understanding import pdf_util 
import pdf 
import sys 
import os


@pdf.app.route('/pdf/to_text',methods = ['POST'])
def get_text_segs():
	file = request.files['file'] 
	filename=secure_filename(file.filename)
	filepath = os.path.join(os.environ['UPLOAD_FOLDER'],filename)
	file.save(filepath)
	
	
	text_arr = pdf_util.segment_document(filepath)
	context = {
		"text_arr" : text_arr 
	}
	# cleanup by deleting file 
	os.remove(filepath)
	return flask.jsonify(**context)
