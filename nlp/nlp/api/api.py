import flask
import nlp

@nlp.app.route('/nlp/summary', methods=["POST"])
def get_summary():
    text = flask.request.get_json()["text"]

    # summarizer
    output = nlp.summarizer(text, max_length=130, min_length=30, do_sample=False)[0]

    context = {
        "summary": output
    }
    
    return flask.jsonify(**context)
