#import data.request_data
from data.request_data import *
from put_data_in_elastic import *
import data.API_KEY as API_KEY_module

# run this when executed at top level (i.e as scrypt, and not as an import)
if __name__ == "__main__":
    
    #### 1 - IMPORTER LES DONNEES ####

    # source can be : "all", "nyt", "inyt". Default = "all"
    source = "all"
    # section can be : all, admin, arts, automobiles, books, briefing, business, climate, corrections, crosswords & games, education, en español, fashion, food, guides, health, home & garden, home page, job market, lens, magazine, movies, multimedia/photos, new york, obituaries, opinion, parenting, podcasts, reader center, real estate, science, smarter living, sports, style, sunday review, t brand, t magazine, technology, the learning network, the upshot, the weekly, theater, times insider, today’s paper, travel, u.s., universal, video, well, world, your money
    # default = "all"
    section = "all"
    # limit is multiple of 20, between 20 and 500. Default = 20 
    limit = "500"
    # offset is multiple of 20, between 20 and 500. Default = 0
    offset = "0"
    #get API KEY which is defined in a specific module
    API_KEY = API_KEY_module.MY_API_KEY
        
    execute(source, section, limit, offset, API_KEY)
    
    
    #### 2 - METTRE LES DONNES DANS ELASTICSEARCH ####
    
    put_in_elastic()

