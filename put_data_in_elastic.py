import requests, json, os
from elasticsearch import Elasticsearch, helpers

def put_in_elastic():
    
    # chemin vers le répertoire contenant la data
    dir_path = os.path.dirname(os.path.abspath(__file__))
    directory = dir_path+'/data'

    # Connexion au cluster
    es =Elasticsearch(hosts ="http://@localhost:9200")

    fullpath = directory+'/requested_data.json'
    # Opening JSON file
    f = open(fullpath, "r")

    # Reading from file
    json_records = json.loads(f.read())

    index_name = 'wire'
    ### uncomment next line to clear index ###
    # es.options(ignore_status=[400, 404]).indices.delete(index=index_name)
    es.options(ignore_status=400).indices.create(index=index_name)
    action_list = []

    for row in json_records["results"]:
        record = {
            '_op_type': 'index',
            '_index': index_name,
            '_source': row
        }
        
        # Ajouter row à l'index seulement s'il n'y figure pas déjà
        if row_not_in_index(es, index_name, row["uri"]):
            action_list.append(record)

    # s'il y a des éléments à ajouter à l'index, alors le faire
    if action_list:
        helpers.bulk(es, action_list, index=index_name)

def row_not_in_index(elastic, index, key):
    # requête pour vérifier si la clé "uri" passée en argument figure déjà dans l'index
    query_body = {
        "bool":{
            "must": [
            {
                "terms":{
                "uri.keyword":[key]
                }
            }  
            ]
        }
    }    
    
    resp = elastic.search(index=index, query=query_body)
    if resp['hits']['total']['value'] > 0:
        return False
    else:
        return True

# run this when executed at top level (i.e as scrypt, and not as an import)
if __name__ == "__main__":
    put_in_elastic()