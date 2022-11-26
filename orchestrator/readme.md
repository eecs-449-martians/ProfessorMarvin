# Orchestrator module 

This is the orchestrator module that connects all of the PDF understanding and retrieval functionality of Marvin

## To start

This orchestrator module runs in a flask server. To run the flask server, do the following

1. Start the NLP and PDF understanding flask server modules 
1. CD into this directory in a new terminal window 
1. run the following command: `source run_orch_server`

## Endpoints 

This server has a number of endpoints as follows. 


### File Upload 

ingest a PDF document and add all its passages to the saved state of the PDF system 

API call:

```
curl -X POST -F file=@[FILE_PATH] http://localhost:[PORT_NUMBER]/orch/upload_file
````

e.g: ` curl -X POST -F file=@$(pwd)/../pdf/test_docs/Syllabus.pdf http://localhost:8002/orch/upload_file`

### Get Question

Given a query, generate a question about the most appropriate passage 

API call:

```
curl -X GET http://localhost:[PORT_NUMBER]/orch/get_question -H 'Content-Type: application/json' -d '{"Query":"[QUERY_TEXT]"}'
````

e.g: `curl -X GET http://localhost:8002/orch/get_passage -H 'Content-Type: application/json' -d '{"Query":"what is the MDP project"}'`


### Get Summary

Given a query, generate a summary of the most appropriate passage 

API call:

```
curl -X GET http://localhost:[PORT_NUMBER]/orch/get_summ -H 'Content-Type: application/json' -d '{"Query":"[QUERY_TEXT]"}'
````

e.g: `curl -X GET http://localhost:8002/orch/get_summ -H 'Content-Type: application/json' -d '{"Query":"what is the MDP project"}'`


### Get Passage

Given a query, return the most appropriate passage 

API call:

```
curl -X GET http://localhost:[PORT_NUMBER]/orch/get_passage -H 'Content-Type: application/json' -d '{"Query":"[QUERY_TEXT]"}'
````

e.g: `curl -X GET http://localhost:8002/orch/get_passage -H 'Content-Type: application/json' -d '{"Query":"what is the MDP project"}'`


### Delete File 

Delete all entries from a given file

API call:

```
curl -X GET http://localhost:[PORT_NUMBER]/orch/delete_file -H 'Content-Type: application/json' -d '{"filename":"[FILE_NAME.pdf]"}'
````

e.g: `curl -X GET http://localhost:8002/orch/delete_file -H 'Content-Type: application/json' -d '{"filename":"mypdf.pdf"}'`
