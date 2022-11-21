# howto: run file from command line as 
# $ python3 keyword.py regexfunction "[query]"
# where [query] is a line of text that includes one or none of 
# the following keywords: summarize, quiz, vocab, define

# keyword.py will return the original string with appended prefixes for keyword match
# for example, 
# $ python3 keyword.py regexfunction "can you summarize and vocab me passage 5"
# will print and return 
# "summarize|vocab|can you summarize and vocab me passage 5"

# given command works for same-directory, specify file path as appropriate

import re
import sys

#requires where query is string obj
def regexfunction(query):
    returnObj = ""
    notFound = True
    prefixStrings = ("summarize","quiz","vocab","define")
    
    for word in prefixStrings:
        if (re.search(word, query)):
            returnObj += word
            returnObj += "|"
            notFound = False

    if (notFound):
        returnObj = "notFound|" + returnObj

    returnObj += query
    print(returnObj)
    return(returnObj)
    #print(query)

if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])