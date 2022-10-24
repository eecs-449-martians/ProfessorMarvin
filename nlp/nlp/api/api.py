import enum
import flask
import nlp

@nlp.app.route('/nlp/summary', methods=["POST"])
def get_summary():
    text = flask.request.get_json()["text"]

    # summarizer
    output = nlp.summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]

    context = {
        "summary": output
    }
    
    return flask.jsonify(**context)


@nlp.app.route('/nlp/genqa', methods=["POST"])
def get_generated_qa():
    text = flask.request.get_json()["text"]
    print("====================== starting ===================")
    print(text)

    # Summarize
    summary = nlp.summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
    print("====================== summary ===================")
    print(summary)

    # Parse with SpaCy to extract named entities as answers
    doc = nlp.spacy_model(summary)
    answers = [(e.text, e.end_char) for e in doc.ents]

    print("====================== answer entities ===================")
    print(answers)

    # Match answers to sentences in text for context
    contexts = text.split('.') # separate text into context sentences
    sentence_ends = [i for i, char in enumerate(text) if char == '.'] # find ends of each context sentence
    ans_cntxt = []
    for ans in answers:
        for i, period_idx in enumerate(sentence_ends): 
            # if ans ends before a given period, it's in that sentence. Works because sentence_ends is sorted.
            if ans[1] < period_idx:
                ans_cntxt.append((ans, contexts[i]))
                break
    
    
    # ans_cntxt = [(answer, sentence answer is in), ...]
    print("====================== qg ===================")

    # Run QG model on answers to get questions
    questions = []
    for ac_pair in ans_cntxt:
        input_text = f"answer: {ac_pair[0][0]}  context: {ac_pair[1]} </s>"
        print(input_text)

        features = nlp.qg_tokenizer([input_text], return_tensors='pt')
        output = nlp.qg_model.generate(input_ids=features['input_ids'], 
               attention_mask=features['attention_mask'],
               max_length=64) # max_length is tunable
        
        question = nlp.qg_tokenizer.decode(output[0])
        print(question)
        questions.append(question)

    
    # Called payload to avoid confusion with question contexts above
    payload = {
        "questions": questions,
        "answers": answers
    }

    return flask.jsonify(**payload)



@nlp.app.route('/nlp/genqa2', methods=["POST"])
def get_generated_qa2():
    text = flask.request.get_json()["text"]
    print("====================== starting ===================")
    print(text)

    # Summarize
    summary = nlp.summarizer(text, max_length=260, min_length=200, do_sample=False)[0]["summary_text"]
    print("====================== summary ===================")
    print(summary)

    print("====================== qagen ===================")

    # Run QG model on answers to get questions
    qas = nlp.qagen_model(summary)
    
    # Called payload to avoid confusion with question contexts above
    payload = {
        "qas": qas
    }

    return flask.jsonify(**payload)
