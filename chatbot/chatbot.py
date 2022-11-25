import re
import sys
import flask 

@chatbot.app.route("/chatbot/chat", methods=["GET", "POST"])
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

@chatbot.app.route("/chatbot/chat", methods=["GET", "POST"])
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
@chatbot.app.route("/chatbot/chat", methods=["GET", "POST"])
def start():
    sum_words = ("summarize", "summary", "tldr", "important")
    quiz_words = ("quiz", "test", "question", "practice")

    print("Hello, I'm Professor Marvin, your personal study buddy!") 

    while(True):
        sum_count, quiz_count = 0
        query = input("Would you like me to summarize a passage, or give you test questions?")
        query = query.lower()

        for word in sum_words:
            if (re.search(word, query)):
                sum_count = sum_count + 1

        for word in quiz_words:
            if (re.search(word, query)):
                quiz_count = sum_count + 1


        if (sum_count > quiz_count):
            summarize_confirm()
        elif (sum_count < quiz_count):
            quiz_confirm()
        else:
            print("I'm sorry, I don't quite understand")

    #print(query)

if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
