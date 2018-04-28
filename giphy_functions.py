import giphy_client
import urllib
import os
from giphy_client.rest import ApiException
from pprint import pprint

GIPHY_API_KEY = os.environ['GIF_GIPHY_API_KEY']

def searchGif(q = 'cheeseburgers'):
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    limit = 25 # int | The maximum number of records to return. (optional) (default to 25)
    offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    rating = 'g' # str | Filters results by specified rating. (optional)
    lang = 'en' # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try: 
        # Search Endpoint
        api_response = api_instance.gifs_search_get(GIPHY_API_KEY, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
    except ApiException as e: raise
    
    return True

def getRandomGif(tag = 'burrito'):
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    rating = 'g' # str | Filters results by specified rating. (optional)
    fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try: 
        # Random Endpoint
        api_response = api_instance.gifs_random_get(GIPHY_API_KEY, tag=tag, rating=rating, fmt=fmt)
        return api_response.data
    except ApiException as e: raise

    return False

def getRandomGifs(terms):
    for term in terms:
        gif = getRandomGif(term)
        urllib.urlretrieve(gif.fixed_height_downsampled_url, "source/"+term.replace(" ","_")+".gif")
    return True