import re
#import sys
import flask 
import requests

def summarize_confirm():
    answer = input("Would you like me to summarize a passage?")
    answer = answer.lower()

    if (answer == 'no'):
        answer2 = input("Would you like me to quiz you instead?")
        answer2 = answer2.lower()
        if (answer2 == 'no'):
            print("Sorry, that's all I can do for now. More features on the way!")
        if (answer2 == 'yes'):
            quiz_confirm()
            return
    
    answer3 = input("What part would you like me to summarize?")
    return


def quiz_confirm():
    answer = input("Would you like me to quiz you on a topic?")
    answer = answer.lower()
    if (answer == 'no'):
        answer2 = input("Would you like me to summarize something for you instead?")
        answer2 = answer2.lower()
        if (answer2 == 'no'):
            print("Sorry, that's all I can do for now. More features on the way!")
        if (answer2 == 'yes'):
            summarize_confirm()
            return
    
    answer3 = input("What would you like for me to quiz you on?")
    return

#requires where query is string obj
@chatbot.app.route("/chatbot/chat", methods=["POST"])
def respond(state,  query): # params - question, summary, start, unknown 

    if (state == 'start'):
        #start of the program
        return {'text': "Hello, I'm Professor Marvin, your personal study buddy! Would you like me to summarize a passage, or give you test questions?", 'next_state': 'chat'}
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
            return {'text': "What part would you like me to summarize?", 'next_state': 'summarize_keyword'}
        elif (sum_count < quiz_count):
            return {'text': "What would you like me to quiz?", 'next_state': 'quiz_keyword'}
        else:
            return {'text': "I'm sorry, I don't quite understand", 'next_state': 'chat'}
    
    elif (state == "summarize_keyword"):

        r = requests.post("http://localhost:8000/orch/get_summ/", json=query)
        if (r['success']): 
            text = r['Summary']
            return {'text' : text, 'next_state' : 'chat'}
        else:
            return {'text': "Sorry, we could not find what you are looking for",  'next_state': "chat"}
            
    elif (state == "quiz_keyword"):
        r = requests.post("http://localhost:8000/orch/get_question/", json=query)
        if (r['success']): 
            text = r['Outputs']['Question']
            return {'text' : text, 'next_state' : 'question'}
        else:
            return {'text': "Sorry, we could not find what you are looking for",  'next_state': "answer"}
    elif (state == "answer"):
        r = requests.post("http://localhost:8000/orch/get_question/", json=query)
        if (r['success']): 
            text = r['Outputs']['Answer']
            return {'text' : text, 'next_state' : 'question'}
        else:
            return {'text': "Sorry, we could not find what you are looking for",  'next_state': "chat"}
    

    return {'text': "", "next_state": 'start'}

    

    #print(query)

#if __name__ == "__main__":
    #args = sys.argv
    #globals()[args[1]](*args[2:])
        # args[0] = current file
        # args[1] = function name
        # args[2:] = function args : (*unpacked)
