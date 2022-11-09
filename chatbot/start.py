from jaseci.actions.live_actions import jaseci_action

def main():
    current_state = 0
    graph_connection = {'root': ['conv_root'], #root root
             'conv_root': [0], #root
             0: [1, 2, 3, 4], #
             1: [1, 5],
             2: [1, 6],
             3: [1, 7, 8],
             4: [1], #error/ unrecognized command node
             5: [1],
             6: [1],
             7: [1],
             8: [1] }

    nodes = {0: ['var0', 'var1', 'var2'],
             1: ['var1', 'var2', 'var3']
            }

    #nodes[current_state][2]  how to access node element
    #current_state = graph_connection[current_state]['x']    how to move along graph
             
    #one of the node vars could be boilerplate filler text explaining the node
    #another variable could be a identifier for jaseci

def send_string(outputting_node): #additional input for specific query e.g. "here's what I found for 'eiffel tower height'" ??
    pass

def receive_string(user_query):
    # run ML on user input to select best node 
    pass







