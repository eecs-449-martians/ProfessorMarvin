import flask 
import chatbot
import re
#import sys

import requests

#state = "start"
saved_query = ""

#requires where query is string obj
@chatbot.app.route("/chatbot/chat", methods=["POST"])
def respond(): # params - question, summary, start, unknown 
    print('got request')
    query = flask.request.get_json()["text"]
    print('hey')
    
    if (chatbot.state == 'start'):
        #start of the program
        chatbot.state = 'chat'
        return {'text': "Hello, I'm Professor Marvin, your personal study buddy! Would you like me to summarize a passage, or give you test questions?"}
    
    elif (chatbot.state == 'chat'): 
        #find out what user wants
        
        sum_words = ("summarize", "summary", "tldr", "important") # "passage", "text"
        quiz_words = ("quiz", "test", "question", "practice") # "exam"
        #vocab_list = ("vocab", "list", "words", "terms")
        #vocab_specific_definition = ("define", "definition", "word", "mean", "term")

        sum_count = 0
        quiz_count = 0
        #vocab_list_count, vocab_define_count = 0
        
        query = query.lower()

        for word in sum_words:
            if (re.search(word, query)):
                sum_count = sum_count + 1

        for word in quiz_words:
            if (re.search(word, query)):
                quiz_count = quiz_count + 1

        #for word in vocab_list:
        #    if (re.search(word, query)):
        #        vocab_list_count += 1

        #for word in vocab_specific_definition:
        #    if (re.search(word, query)):
        #        vocab_define_count += 1

        if (sum_count > quiz_count):
            # call get_summ from orc
            #r = requests.post("http://localhost:8002/orch/get_summ/", json=rq_body)
            chatbot.state = "summarize_keyword"
            return {'text': "What part would you like me to summarize?"}
        elif (sum_count < quiz_count):
            chatbot.state = "quiz_keyword"
            return {'text': "What would you like me to quiz?"}
        else:
            chatbot.state = "chat" 
            return {'text': "I'm sorry, I don't quite understand"}
    
    elif (chatbot.state == "summarize_keyword"):
        r = requests.get("http://localhost:8002/orch/get_summ", json={"Query": query})
        response = r.json()
        if (response['Success']): 
            text = response['Summary']
            chatbot.state = "chat"
            return {'text' : text}
        else:
            chatbot.state = "chat"
            return {'text': "Sorry, we could not find what you are looking for"}
            
    elif (chatbot.state == "quiz_keyword"):
        r = requests.post("http://localhost:8002/orch/get_question", json={"Query": query})
        response = r.json()
        if (response['Success']): 
            text = response['Outputs']['Question']
            chatbot.state = "answer"
            return {'text' : text}
        else:
            chatbot.state = "chat"
            saved_query = query
            return {'text': "Sorry, we could not find what you are looking for"}
    elif (chatbot.state == "answer"):
        r = requests.post("http://localhost:8002/orch/get_question", json={"Query": saved_query})
        response = r.json()
        if (response['Success']): 
            text = response['Outputs']['Answer']
            chatbot.state = "chat"
            return {'text' : text}
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