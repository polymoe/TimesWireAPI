from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from elasticsearch import Elasticsearch

# définition de la classe qui nous servira à passer des informations dans le corps de notre requête
class Visualization_criteria(BaseModel):
    """Les critères qui sont transmis pour choisir les graphes
    """
    top: int
    viz: str

### définition de l'API ###
api = FastAPI(
    title="Projet BigApplePI Times Wire FastAPI",
    description="Développée par Mohamed TOUMI - jan 2023",
    version="1.0",
    openapi_tags=[
        {
            'name': 'home',
            'description': 'default functions'
        },
        # {
        #     'name': 'questions',
        #     'description': 'functions that are used to deal with questions'
        # }
    ]
)

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

### définition du champs des valeurs possibles ###
users = {

    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash('wonderland'),
    },

    "bob" : {
        "username" :  "bob",
        "hashed_password" : pwd_context.hash('builder'),
    },

}
viz_type = ["geo", "material_type", "people_vs_geo"]
top_range = [i for i in range(1,21)]

### définition de la fonction qui permettra de fournir un formulaire d'authentification et de vérification d'identifiant pour les utilisateurs autorisés ###
def get_current_user():
    """ pour vérifier si les identifiants figurent bien dans la base des utilisateurs autorisés
    """

    def get_user_(credentials: HTTPBasicCredentials = Depends(security)):
        username = credentials.username
        if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_password'])):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect user or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username
    return get_user_

### définition de la fonction qui génère les données nécessaires pour créer les visualisations demandées
def gen_viz_data(top_, viz_):  
    """fonction qui retourne les données pour générer la visuatlisation demandée
    """
    # Connexion au cluster
    es =Elasticsearch(hosts ="http://@localhost:9200")
    index = "wire"

    ### if geo ###
    fields_geo = [
            {
            "field": "created_date",
            "format": "date_time"
            },
            {
            "field": "first_published_date",
            "format": "date_time"
            },
            {
            "field": "published_date",
            "format": "date_time"
            },
            {
            "field": "updated_date",
            "format": "date_time"
            }
        ]
    size_geo = 0
    script_fields_geo = {}
    stored_fields_geo = ["*"]
    runtime_mappings_geo = {}
    _source_geo = {
            "excludes": []
        }
    query_geo = {
            "bool": {
            "must": [],
            "filter": [
                {
                    "range": {
                        "created_date": {
                        "format": "strict_date_optional_time",
                        "gte": "2022-12-29T18:00:00.000Z",
                        "lte": "2023-01-04T15:00:05.714Z"
                        }
                    }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
    aggs_geo = {
            "0": {
                "terms": {
                    "field": "geo_facet.keyword",
                    "order": {
                    "_count": "desc"
                    },
                    "size": top_,
                    "shard_size": 1000
                }
            }
        }

    ### if material ###
    fields_material = [
        {
        "field": "created_date",
        "format": "date_time"
        },
        {
        "field": "first_published_date",
        "format": "date_time"
        },
        {
        "field": "published_date",
        "format": "date_time"
        },
        {
        "field": "updated_date",
        "format": "date_time"
        }
    ]
    size_material = 0
    script_fields_material = {}
    stored_fields_material = ["*"]
    runtime_mappings_material = {}
    _source_material = {
            "excludes": []
        }
    query_material = {
        "bool": {
        "must": [],
        "filter": [
            {
            "range": {
                "created_date": {
                "format": "strict_date_optional_time",
                "gte": "2022-12-29T18:00:00.000Z",
                "lte": "2023-01-04T20:27:08.055Z"
                }
            }
            }
        ],
        "should": [],
        "must_not": []
        }
    }
    aggs_material = {
        "0": {
        "terms": {
            "field": "material_type_facet.keyword",
            "order": {
            "_count": "desc"
            },
            "size": top_,
            "shard_size": 1000
        }
        }
    }

    ### if pvg ###
    fields_pvg = [
        {
        "field": "created_date",
        "format": "date_time"
        },
        {
        "field": "first_published_date",
        "format": "date_time"
        },
        {
        "field": "published_date",
        "format": "date_time"
        },
        {
        "field": "updated_date",
        "format": "date_time"
        }
    ]
    size_pvg = 0
    script_fields_pvg = {}
    stored_fields_pvg = ["*"]
    runtime_mappings_pvg = {}
    _source_pvg = {
            "excludes": []
        }
    query_pvg = {
        "bool": {
        "must": [],
        "filter": [
            {
            "range": {
                "created_date": {
                "format": "strict_date_optional_time",
                "gte": "2022-12-29T18:00:00.000Z",
                "lte": "2023-01-04T20:30:39.286Z"
                }
            }
            }
        ],
        "should": [],
        "must_not": []
        }
    }
    aggs_pvg = {
        "0": {
        "terms": {
            "field": "per_facet.keyword",
            "order": {
            "_count": "desc"
            },
            "size": top_,
            "shard_size": 25
        },
        "aggs": {
            "1": {
            "terms": {
                "field": "geo_facet.keyword",
                "order": {
                "_count": "desc"
                },
                "size": 2,
                "shard_size": 25
            }
            }
        }
        }
    }
    
    if viz_ == "geo":
        query=query_geo
        aggs=aggs_geo
        fields=fields_geo
        size=size_geo
        script_fields=script_fields_geo
        stored_fields=stored_fields_geo
        runtime_mappings=runtime_mappings_geo
        _source=_source_geo
    elif viz_ == "material_type":
        query=query_material
        aggs=aggs_material
        fields=fields_material
        size=size_material
        script_fields=script_fields_material
        stored_fields=stored_fields_material
        runtime_mappings=runtime_mappings_material
        _source=_source_material
    elif viz_ == "people_vs_geo":
        query=query_pvg
        aggs=aggs_pvg
        fields=fields_pvg
        size=size_pvg
        script_fields=script_fields_pvg
        stored_fields=stored_fields_pvg
        runtime_mappings=runtime_mappings_pvg
        _source=_source_pvg
        
    resp = es.search(index=index, query=query, aggs=aggs, fields=fields, size=size, script_fields=script_fields, stored_fields=stored_fields, runtime_mappings=runtime_mappings, _source=_source)
    
    return resp['aggregations']['0']['buckets']   

### définition de la fonction qui vérifie que les critères renseignés sont bien dans le champs des possibles ###
def check_criteria(viz_criteria_, top_range_, viz_list_):
    """fonction qui qui vérifie que les critères renseignés sont bien dans le champs des possibles
    """
    raise_exception = False
    if viz_criteria_.top not in top_range_:
        raise_exception = True 
    if viz_criteria_.viz not in viz_list_:
        raise_exception = True
    if raise_exception:
        raise ValueError
    
### point de terminaison pour vérifier que l'API est bien fonctionnelle ###
@api.get('/', name="Vérif API fonctionnelle", tags=['home'])
def get_index(username: str = Depends(get_current_user())):
    """Point de terminaison permettant de vérifier que l'API est fonctionnelle
    """
    return {
        "message" : "tout va bien {} ! l'API est fonctionnelle".format(username)
        }

### point de terminaison pour récupérer les différents champs possibles pour générer les visualisations, et leurs valeurs ###
@api.get('/criteria', name="Valeurs possibles pour champs requêtes", tags=['home'])
def get_criteria(username: str = Depends(get_current_user())):
    """ Point de terminaison pour récupérer les différents champs possibles pour extraire des visualisations, et leurs valeurs
    """
    return dict(
        User=username,
        Top_range=top_range,
        Viz_type=viz_type)

### point de terminaison pour récupérer les visualisations souhaitées ###
responses = {
    498: {"description": "Sample Size Error"},
    499: {"description": "Incorrect Top value or viz type"},
}
@api.post('/viz', name="post les critères et récupère les données pour les visualisations souhaitées", tags=['viz'], responses=responses)
def post_viz_criteria(viz_criteria: Visualization_criteria, username: str = Depends(get_current_user())):
    """Point de terminaison permettant de poster les critères des visualisations et de récupérer ensuite les données correspondantes
    """
    try:
        check_criteria(viz_criteria, top_range, viz_type)
        pass
    except ValueError:
        raise HTTPException(
            status_code=499,
            detail='{}, the question criteria is not in correct range of top or viz type'.format(username)
        )
    try:
        viz_data = gen_viz_data(viz_criteria.top, viz_criteria.viz)
        return viz_data
    except ValueError:
        raise HTTPException(
            status_code=498,
            detail='{}, the sample requested is larger than possible questions'.format(username)
        )    