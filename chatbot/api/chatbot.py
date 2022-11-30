import flask 
import chatbot
import re
#import sys

import requests

#state = "start"
#saved_query = ""

TARG_WORDS = {
        'summary':["summarize", "summary", "tldr", "important", 'gist'] ,
        'quiz': ["quiz", "test", "question", "practice"], 
        'passage':["passage", "text", "full", 'look up', 'look something up',"search for"],
        'summary_split':  ["about","on",'of'],
        'quiz_split':["about","on"],
        'passage_split':["about","on", "search for"],
        }


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
        
        topic_words_sum =  ["about","on",'of']
        topic_words_quiz = ["about","on"]
        topic_words_passage = ["about","on", "search for"]


        actions = {"sum_count": 0, "quiz_count": 0, "passage_count": 0}
        
        query = query.lower()

        for word in TARG_WORDS['summary']:
            if (re.search(word, query)):
                actions['sum_count'] = actions['sum_count'] + 1

        for word in TARG_WORDS['quiz']:
            if (re.search(word, query)):
                actions['quiz_count'] = actions['quiz_count'] + 1

        for word in TARG_WORDS['passage']:
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
            # check if we have a query built into the first command 
            for split_word in TARG_WORDS['summary_split']: 
                # check if word is in query 
                if split_word in query:
                    splits = query.split(split_word)
                    mode_part,query_part = splits[0], split_word.join(splits[1:])
                    # verify that target is before the split 
                    if check_query_parts(mode_part,query_part,"summary"): 
                        message,success = do_summary_query(query_part)
                        if success:
                            chatbot.state = "check_fp"
                            return {'text':message}
            # else go ask wheat they do... 
            chatbot.state = "summarize_keyword"
            return {'text': "What do you want me to look for?"}
        elif (todo == "quiz_count"):
            # check if we have a query built into the first command 
            for split_word in TARG_WORDS['quiz_split']: 
                # check if word is in query 
                if split_word in query:
                    splits = query.split(split_word)
                    mode_part,query_part = splits[0], split_word.join(splits[1:])
                    # verify that target is before the split 
                    if check_query_parts(mode_part,query_part,"quiz"): 
                        message,success = do_question_query(query_part)
                        if success:
                            chatbot.state = "answer"
                            return {'text':message}
            # else go ask wheat they do... 
            chatbot.state = "quiz_keyword"
            return {'text': "What topic would you like me to quiz you on?"}
        elif(todo == "passage_count"):
            # check if we have a query built into the first command 
            for split_word in TARG_WORDS['passage_split']: 
                # check if word is in query 
                if split_word in query:
                    splits = query.split(split_word)
                    mode_part,query_part = splits[0], split_word.join(splits[1:])
                    # verify that target is before the split 
                    if check_query_parts(mode_part,query_part,"passage"): 
                        message,success = do_passage_query(query_part)
                        if success:
                            chatbot.state = "chat"
                            return {'text':message}

            # else go ask wheat they do... 
            chatbot.state = "passage" 
            return {'text': "What do you want me to look for?"}

    elif (chatbot.state == "passage"):
        print(query)
        message,success = do_passage_query(query)
        # update state and return 
        chatbot.state="chat"
        return {"text": message}
    
    elif (chatbot.state == "summarize_keyword"):
        print(query)
        # do the lookup 
        message,success = do_summary_query(query)
        # act on the lookup 
        if success: 
            chatbot.state = "check_fp"
            chatbot.saved_query = query
        else: 
            chatbot.state = "chat"
        return {"text":message}

    elif (chatbot.state == "quiz_keyword"):
        print(query)
        message, success = do_question_query(query)
        if success: 
            chatbot.state = "answer"
        else:  
            chatbot.state = "chat"
        return {"text":message}


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
        elif yes_count == no_count == 0: 
            chatbot.state = "chat"
            return respond() 
        else: 
            chatbot.state = "chat" 
            return {'text': "That is ok! I hope I can still help!"}
            

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

    
def check_query_parts(act_part:str,query_part:str,type:str)-> bool : 
    """ 
    Given parts of a query, verify that the start and end are valid 
    """
    wordlist = TARG_WORDS[type]
    # check that at least one word is after the split 
    if(len(query_part.strip()) < 4): return False
    # check that  the target is before the split 
    for word in wordlist: 
        if word in act_part: 
            return True 
    return False 

    #print(query)
def do_summary_query(query): 
    """ 
    given a query, return a ret string and a boolean indicating if the lookup was a success
    """
    r = requests.get("http://localhost:8002/orch/get_summ", json={"Query": query})
    response = r.json()
    if (response['Success']): 
        text = response['Summary']
        doc_name = response['DocName']

        output = "According to " + doc_name + ":     \"" + text + "\"        Would you like the full passage instead of just a summarization?"
        return  output, True
    else:
        return "Sorry, we could not find what you are looking for", False 

def do_passage_query(query):
    r = requests.get("http://localhost:8002/orch/get_passage", json={"Query": query})
    response = r.json()
    if (response['Success']):
        text = response['Text']
        doc_name = response['DocName']

        output = "According to " + doc_name + ":       " + text
        return output, True
    else:
        return "Sorry, we could not find what you are looking for", False 

def do_question_query(query):
    r = requests.get("http://localhost:8002/orch/get_question", json={"Query": query})
    response = r.json()
    print(response)
    if (response['Success']): 
        question = response['Question']
        chatbot.curr_answer = response['Answer']
        chatbot.curr_question_doc = response["DocName"]
        return  question, True 
    else:
        chatbot.saved_query = query
        return "Sorry, we don't have any questions for that", False 


#if __name__ == "__main__":
    #args = sys.argv
    #globals()[args[1]](*args[2:])
        # args[0] = current file
        # args[1] = function name
        # args[2:] = function args : (*unpacked)