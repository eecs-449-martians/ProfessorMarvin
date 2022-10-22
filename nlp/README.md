# This is the folder for the nlp module

## Setup
- Run ```pip install -r requirements.txt``` in a python virtual environment to install required packages
- Run ```python -m spacy download en_core_web_sm``` to download spacy model

## Running the server
- Run ```./run_nlp``` to start the server
- Run ```./test_summary``` to send a test request to the summarization API


### TODO:
Load up models in flask init
Query models in routing API calls

Find summarization model - https://huggingface.co/facebook/bart-large-cnn
Find answer/question pair generation model(s)
    - https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/
    - https://huggingface.co/mrm8488/t5-base-finetuned-question-generation-ap
Find vocab extraction model
    - https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/
Figure out how to do vocab definitions - 