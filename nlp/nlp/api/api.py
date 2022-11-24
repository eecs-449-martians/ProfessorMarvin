import enum
import flask
import nlp


@nlp.app.route("/nlp/summary", methods=["POST"])
def get_summary():
    text = flask.request.get_json()["text"]

    # summarizer
    output = nlp.summarizer(text, max_length=130, min_length=30, do_sample=False)[0][
        "summary_text"
    ]

    context = {"summary": output}

    return flask.jsonify(**context)


@nlp.app.route("/nlp/genqa", methods=["POST"])
def get_generated_qa2():
    text = flask.request.get_json()["text"]
    print("====================== starting ===================")
    print(text)

    # Summarize
    summary = nlp.summarizer(text, max_length=130, min_length=30, do_sample=False)[0][
        "summary_text"
    ]
    print("====================== summary ===================")
    print(summary)

    print("====================== qagen ===================")

    # Run QG model on answers to get questions
    qas = nlp.qagen_model(summary)

    # Called payload to avoid confusion with question contexts above
    payload = {"qas": qas}

    return flask.jsonify(**payload)
