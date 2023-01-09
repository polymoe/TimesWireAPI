# BigApplePI/Times Wire API
* Mohamed TOUMI
* Data engineer Bootcamp - project
* 2023 jan

## Project objectives
* The aim of this part of the project is to build a data architecture that makes exploitation of information provided by 'Times Wire API' of the New York Times
* The retrieved information is stored in elasticsearch database
* Then, there is a two-levels data consumption process.
* The first one is based on a kibana dashboard
* The second one aims at replicating the kibana dashboard with a home made application that requests a home made API (using FastAPI) in order to mimic the kibana visualizations

## How to run the application
* install the dependencies that are mentioned in requirements.txt
* run `docker-compose up -d`
* once the elasticsearch and kibana containers are launched, the kibana dashboard is acessible on port 5601 of localhost
* run uvicorn `timeswire_main_api:api --reload`
* run `streamlit run streamlit_dashboard.py`
* click on `Update data`button in the Streamlit app in order to launch the data ingestion pipeline
