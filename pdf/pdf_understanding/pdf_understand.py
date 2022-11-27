import flask
from flask import request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from pdf.pdf_understanding import pdf_util
import pdf
import sys
import os


@pdf.app.route("/pdf/to_text", methods=["POST"])
def get_text_segs():
    # file = request.files["file"]
    # filename = secure_filename(file.filename)
    # filepath = os.path.join(os.environ["UPLOAD_FOLDER"], filename)
    # file.save(filepath)
    filepath = request.get_json()["url"]
    print(request.get_json(),type(request.get_json()))
    filepath = os.path.join(os.environ["PATH_TO_FRONTEND"],'src/api',filepath)
    print(filepath)
    text_arr = pdf_util.segment_document(filepath)
    context = {"Status": "Success", "text segments": text_arr}
    # cleanup by deleting file
    return flask.jsonify(**context)
