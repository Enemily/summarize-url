# URL Summary Generator
A Flask application to summarize URL passages using the watsonx Technology Preview and LangChain + IBM GenAI libraries

## Set up virtual environment
1. cd into the project directory
2. run `python3 -m venv venv`
3. run `source venv/bin/activate`
4. run 'python3 -m pip3 install -r requirements.txt`

## Create `.env` file
1. Add your watsonx.ai API key to the `.env` file in this project directory. The `.env` file should look like
```
GENAI_KEY=<your-genai-key>
GENAI_API=https://workbench-api.res.ibm.com/v1/
```

## Run app
1. run `python3 app.py`


## Set up NGINX (Optional)
1. Find location of NGINX config file: run `nginx -t`
2. Open NGINX config file (of location `vim /opt/homebrew/etc/nginx/nginx.conf` for M1 chip)
3. Add
```
  location /generate_pdf_and_summarize {
    proxy_pass http://localhost:8080/generate_pdf_and_summarize;
  }
```
to the server block that is listening on port 8080. Like so:
```
    server {
        listen       8080;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }
        location /generate_pdf_and_summarize {
            proxy_pass http://localhost:8080/generate_pdf_and_summarize;
        }

        #error_page  404              /404.html;
        ...
    }
```
4. Start the NGINX web server: run `nginx`
5. To stop the NGINX web server: run `nginx -s stop`

## Demo video
https://github.com/Enemily/summarize-url/assets/92351379/4162087d-052c-4372-9be3-5e363f94c675

