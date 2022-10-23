// root node
node conversation_root;

// regular node
node conversation_state {
    // for visualizing in 'jac dot' 
    has name;
    // user query obj
    has input;
    // chatbot text response obj
    has response;
    // placeholder function for sending text to webapp
    can post_to_webapp;
    // placeholder function for sending text to backend
    can post_to_back;
}

graph conversation {
    // node 0
    has anchor conversation_root;

    // conversation nodes
    // according to greybox_diagram
    spawn {
        conversation_root = spawn node::conversation_root;

        starting_hello_node_0 = spawn node::conversation_state();

        summarize_requested_node_1 = spawn node::conversation_state();
        quiz_requested_node_2 = spawn node::conversation_state();
        vocab_requested_node_3 = spawn node::conversation_state();
        unrecognized_not_implemented_node_4 = spawn node::conversation_state();

        summarize_query_node_5 = spawn node::conversation_state();
        quiz_query_node_6 = spawn node::conversation_state();
        vocab_list_query_node_7 = spawn node::conversation_state();
        vocab_definition_node_8 = spawn node::conversation_state();

        // [forward connections]
        conversation_root --> starting_hello_node_0;

        // [forward connections] start
        starting_hello_node_0 --> summarize_requested_node_1;
        starting_hello_node_0 --> quiz_requested_node_2;
        starting_hello_node_0 --> vocab_requested_node_3;
        starting_hello_node_0 --> unrecognized_not_implemented_node_4;

        // [forward connections] task request to query 
        summarize_requested_node_1 --> summarize_query_node_5;
        quiz_requested_node_2 --> quiz_query_node_6;
        vocab_requested_node_3 --> vocab_list_query_node_7;
        vocab_requested_node_3 --> vocab_definition_node_8;

        // [backwards connections] to start
        summarize_requested_node_1 --> starting_hello_node_0;
        quiz_requested_node_2 --> starting_hello_node_0;
        vocab_requested_node_3 --> starting_hello_node_0;
        unrecognized_not_implemented_node_4 --> starting_hello_node_0;                              
        summarize_query_node_5 --> starting_hello_node_0;
        quiz_query_node_6 --> starting_hello_node_0;
        vocab_list_query_node_7 --> starting_hello_node_0;
        vocab_definition_node_8 --> starting_hello_node_0;
    }
}

// main(){}
// https://dreampuf.github.io/GraphvizOnline/
walker init {
    root {
        spawn here --> graph::conversation;
    }
}

walker conversation {

}

node conversation_root:conversation_root {
    has name = "conversation_root";
}
node starting_hello_node_0:conversation_state {
    has name = "starting_hello_node_0";
}
node summarize_requested_node_1:conversation_state {
    has name = "summarize_requested_node_1";
}
node quiz_requested_node_2:conversation_state {
    has name = "quiz_requested_node_2";
}
node vocab_requested_node_3:conversation_state {
    has name = "vocab_requested_node_3";
}
node unrecognized_not_implemented_node_4:conversation_state {
    has name = "unrecognized_not_implemented_node_4";
}
node summarize_query_node_5:conversation_state {
    has name = "summarize_query_node_5";
}
node quiz_query_node_6:conversation_state {
    has name = "quiz_query_node_6";
}
node vocab_list_query_node_7:conversation_state {
    has name = "vocab_list_query_node_7";
}
node vocab_definition_node_8:conversation_state {
    has name = "vocab_definition_node_8";
}
