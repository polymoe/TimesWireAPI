import requests
import os

def execute(source, section, limit, offset, API_KEY):
    requestUrl = "https://api.nytimes.com/svc/news/v3/content/"+source+"/"+section+".json?limit="+limit+"&offset="+offset+"&api-key="+API_KEY
    requestHeaders = {
        "Accept": "application/json"
    }

    response = requests.get(requestUrl, headers=requestHeaders)
    dir_path = os.path.dirname(os.path.abspath(__file__))

    with open(dir_path+'/requested_data.json', 'wb') as outf:
        outf.write(response.content)

