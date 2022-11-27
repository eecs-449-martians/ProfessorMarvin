# PDF processing server for Marvin project 

This is the PDF processing server for the marvin project. It consists of all the required components for the PDF processing submodule for this project. That is it provides an API for ingesting PDF documents, extracting all text in them, and segmenting out passages. 

## Running the flask server 

To run the flask server, start by installing all dependencies found in `requirements.txt`. 

*Important:* then go to `run_pdf_server`, and change the value assigned to `PATH_TO_FRONTEND` to the absolute path to the main directory of the MarvinFrontend server this project is being used with. 



Then, navigate to this directory: 
``` 
cd pdf  
```
Finally run the script for starting this server. 
``` 
bash run_pdf_server  [Optional: Port_number] 
```


## Querying the API  

You can query the API by sending a file via POST request to `http://localhost:[PORT_NUMBER]/pdf/to_text`. 
For example, I like doing so with a `curl` command: 

```
curl -X POST -F file=@/path/to/your/file/test_file.pdf "http://localhost:[PORT_NUMBER]/pdf/to_text"
```

The API will return a JSON file with two fields: `status`, which returns the request status, and `text segments`,  which contains an array of segmetnted text passages. 
	