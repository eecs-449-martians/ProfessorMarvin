import flask 
import chatbot
import re
#import sys

import requests

#state = "start"
#saved_query = ""

#requires where query is string obj
@chatbot.app.route("/chatbot/chat", methods=["POST"])
def respond(): # params - question, summary, start, unknown 
    print('got request')
    query = flask.request.get_json()["text"]

    # punchline feature 
    print(re.sub(r"[^a-zA-Z0-9 ]", "", query).lower())
    if re.sub(r"[^a-zA-Z0-9 ]", "", query).strip().lower() == "marvin youre the best":
        return {'text': "I know."}
    if "i love you" in re.sub(r"[^a-zA-Z0-9 ]", "", query).lower():
        return {'text': "Thats nice."}




    if (chatbot.state == 'start'):
        #start of the program
        chatbot.state = 'chat'
        return {'text': "Hello, I'm Professor Marvin, your personal study buddy! Would you like me to summarize a passage, or find you some information?"}
    
    elif (chatbot.state == 'chat'): 
        #find out what user wants
        
        sum_words = ("summarize", "summary", "tldr", "important", 'gist') # "passage", "text"
        quiz_words = ("quiz", "test", "question", "practice") # "exam"
        passage_words = ("passage", "text", "full", 'look up', 'look something up')

        actions = {"sum_count": 0, "quiz_count": 0, "passage_count": 0}
        
        query = query.lower()

        for word in sum_words:
            if (re.search(word, query)):
                actions['sum_count'] = actions['sum_count'] + 1

        for word in quiz_words:
            if (re.search(word, query)):
                actions['quiz_count'] = actions['quiz_count'] + 1

        for word in passage_words:
            if (re.search(word, query)):
                actions['passage_count'] = actions['passage_count'] + 1

        todo = max(actions, key=actions.get)

        all_zero = True
        for key in actions:
            if actions[key] != 0:
                all_zero = False

        if (all_zero):
            chatbot.state = "chat"
            return {'text': "Sorry, I don't quite understand"}
        elif (todo == "sum_count"):
            # call get_summ from orc
            #r = requests.get("http://localhost:8002/orch/get_summ/", json=rq_body)
            chatbot.state = "summarize_keyword"
            return {'text': "What do you want me to look for?"}
        elif (todo == "quiz_count"):
            chatbot.state = "quiz_keyword"
            return {'text': "What topic would you like me to quiz you on?"}
        elif(todo == "passage_count"):
            chatbot.state = "passage" 
            return {'text': "What do you want me to look for?"}

    elif (chatbot.state == "passage"):
        r = requests.get("http://localhost:8002/orch/get_passage", json={"Query": query})
        response = r.json()
        if (response['Success']):
            text = response['Text']
            chatbot.state = "chat"
            doc_name = response['DocName']

            output = "According to " + doc_name + ":       " + text
            return {'text': output}
        else:
            chatbot.state = "chat"
            return {'text': "Sorry, we could not find what you are looking for"}
    
    elif (chatbot.state == "summarize_keyword"):
        r = requests.get("http://localhost:8002/orch/get_summ", json={"Query": query})
        response = r.json()
        if (response['Success']): 
            text = response['Summary']
            doc_name = response['DocName']
            chatbot.state = "check_fp"
            chatbot.saved_query = query

            output = "According to " + doc_name + ":     \"" + text + "\"        Would you like the full passage instead of just a summarization?"
            return {'text' : output}
        else:
            chatbot.state = "chat"
            return {'text': "Sorry, we could not find what you are looking for"}

    elif (chatbot.state == "check_fp"):
        yes_words = ("yes", "yup", "sure", "alright", "yep", "yeah", "sure",) 
        no_words = ("no", "nah")

        yes_count = 0
        no_count = 0
        
        query = query.lower()

        for word in yes_words:
            if (re.search(word, query)):
                yes_count = yes_count + 1

        for word in no_words:
            if (re.search(word, query)):
                no_count = no_count + 1

        if (yes_count > no_count):
            r = requests.get("http://localhost:8002/orch/get_passage", json={"Query": chatbot.saved_query})
            response = r.json()
            if (response['Success']):
                text = response['Text']
                chatbot.state = "chat"
                return {'text': text}
            else:
                chatbot.state = "chat"
                return {'text': "Sorry, we could not find what you are looking for"}
        else:
            chatbot.state = "chat" 
            return {'text': "That is ok! I hope I can still help!"}
            
    elif (chatbot.state == "quiz_keyword"):
        r = requests.get("http://localhost:8002/orch/get_question", json={"Query": query})
        response = r.json()
        if (response['Success']): 
            question = response['Question']
            chatbot.curr_answer = response['Answer']
            chatbot.curr_question_doc = response["DocName"]
            chatbot.state = "answer"
            return {'text' : question}
        else:
            chatbot.state = "chat"
            chatbot.saved_query = query
            return {'text': "Sorry, we could not find what you are looking for"}

    elif (chatbot.state == "answer"):
        # r = requests.get("http://localhost:8002/orch/get_question", json={"Query": chatbot.saved_query})
        # response = r.json()

        if (chatbot.curr_answer is not None and chatbot.curr_question_doc is not None  ): 
            chatbot.state = "chat"
            output = "According to " + chatbot.curr_question_doc + ", the answer is: " + chatbot.curr_answer
            chatbot.curr_question_doc, chatbot.curr_answer = None, None 
            return {'text' : output}
        else:
            chatbot.state = "chat"
            return {'text': "Sorry, we could not find what you are looking for"}
    
    chatbot.state = "start"
    return flask.jsonify(text = "")

    

    #print(query)

#if __name__ == "__main__":
    #args = sys.argv
    #globals()[args[1]](*args[2:])
        # args[0] = current file
        # args[1] = function name
        # args[2:] = function args : (*unpacked)