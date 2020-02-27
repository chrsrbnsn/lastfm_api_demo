import requests
import requests_cache
import json
import time
from IPython.core.display import clear_output

API_KEY = 'fhfhfs88777555fjkfkfkks77559993' #dummy key
USER_AGENT = 'Python_Tester'

# creates local cache to reduce redundant communication with the API
requests_cache.install_cache()

# hold data returned from API
responses = []

page = 1
max_pages = 9999 # place holder, will be set to exact max pages during API call

def mylastfm_get(payload):
    # setup the headers (user agent required)
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # personal lastfm API key and desired format
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def json_print(obj):
    # format json output
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

while page <= max_pages:
    # include parameters for limiting and paganation
    payload = {
        'method': 'chart.gettopartists',
        'limit': 500,
        'page': page
    }

    # for awareness
    print(f"Retrieving page {page}/{max_pages}")

    clear_output(wait=True)

    response = mylastfm_get(payload)

    if response.status_code != 200:
        print(response.text)
        break

    # set paganation variables to true counts
    page = int(response.json()['artists']['@attr']['page'])
    max_pages = int(response.json()['artists']['@attr']['totalPages'])

    responses.append(response)

    # utilizing the cache, if not cached pause .35 seconds to limit API calls
    if not getattr(response, 'from_cache', False):
        time.sleep(0.35)

    # increment the while loop (page)
    page += 1
