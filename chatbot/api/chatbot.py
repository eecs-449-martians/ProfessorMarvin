import flask 
import chatbot
import re
#import sys

import requests

state = "start"
saved_query = ""

#requires where query is string obj
@chatbot.app.route("/chatbot/chat", methods=["POST"])
def respond(query): # params - question, summary, start, unknown 

    if (state == 'start'):
        #start of the program
        state = 'chat'
        return {'text': "Hello, I'm Professor Marvin, your personal study buddy! Would you like me to summarize a passage, or give you test questions?"}
        
    elif (state == 'chat'): 
        #find out what user wants
        
        sum_words = ("summarize", "summary", "tldr", "important") # "passage", "text"
        quiz_words = ("quiz", "test", "question", "practice") # "exam"
        #vocab_list = ("vocab", "list", "words", "terms")
        #vocab_specific_definition = ("define", "definition", "word", "mean", "term")

        sum_count, quiz_count = 0
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
            #r = requests.post("http://localhost:8000/orch/get_summ/", json=rq_body)
            state = "summarize_keyword"
            return {'text': "What part would you like me to summarize?"}
        elif (sum_count < quiz_count):
            state = "quiz_keyword"
            return {'text': "What would you like me to quiz?"}
        else:
            state = "chat" 
            return {'text': "I'm sorry, I don't quite understand"}
    
    elif (state == "summarize_keyword"):

        r = requests.post("http://localhost:8000/orch/get_summ/", json=query)
        if (r['success']): 
            text = r['Summary']
            state = "chat"
            return {'text' : text}
        else:
            state = "chat"
            return {'text': "Sorry, we could not find what you are looking for"}
            
    elif (state == "quiz_keyword"):
        r = requests.post("http://localhost:8000/orch/get_question/", json=query)
        if (r['success']): 
            text = r['Outputs']['Question']
            state = "answer"
            return {'text' : text}
        else:
            state = "chat"
            saved_query = query
            return {'text': "Sorry, we could not find what you are looking for"}
    elif (state == "answer"):
        r = requests.post("http://localhost:8000/orch/get_question/", json=saved_query)
        if (r['success']): 
            text = r['Outputs']['Answer']
            state = "chat"
            return {'text' : text}
        else:
            state = "chat"
            return {'text': "Sorry, we could not find what you are looking for"}
    
    state = "start"
    return {'text': ""}

    

    #print(query)

#if __name__ == "__main__":
    #args = sys.argv
    #globals()[args[1]](*args[2:])
        # args[0] = current file
        # args[1] = function name
        # args[2:] = function args : (*unpacked)