import flask
from flask import request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from pdf.pdf_understanding import pdf_util
import pdf
import sys
import os


@pdf.app.route("/pdf/to_text/", methods=["POST"])
def get_text_segs():
    # file = request.files["file"]
    # filename = secure_filename(file.filename)
    # filepath = os.path.join(os.environ["UPLOAD_FOLDER"], filename)
    # file.save(filepath)
    filepath = request.args.get("url")
    filepath = filepath.replace("%2F", "/" )
    #print(filepath)
    text_arr = pdf_util.segment_document(filepath)
    context = {"Status": "Success", "text segments": text_arr}
    # cleanup by deleting file
    #os.remove(filepath)
    
    print(text_arr)
    return flask.jsonify(**context)

# @pdf.app.route("/pdf/to_nlp/", methods=["POST"])
# def pdf_to_nlp():
#     file = request.files["file"]
#     filename = secure_filename(file.filename)
#     filepath = os.path.join(os.environ["UPLOAD_FOLDER"], filename)
#     file.save(filepath)

    
#     text = request.('http://localhost:8001/pdf/to_text?file=' + filename)

#     return pdf
