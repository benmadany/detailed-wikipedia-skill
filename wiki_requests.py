# Detailed Wikipedia Skill
# Author: Ben Madany

import requests


API_URL = "http://en.wikipedia.org/w/api.php"
USER_AGENT = "Detailed Wikipedia Skill (https://github.com/benmadany/detailed-wikipedia-skill)"


class WikipediaException(msg):
    # TODO


def log_msg(msg, error=0):
    print(msg)


def default_params():
    params = {"format":"json"}
    return params


def default_headers():
    global USER_AGENT
    headers = {"User Agent": USER_AGENT}
    return headers


# Request prefix search of a specific article, returns a tuple containing the title and pageid of the first result (Wikipedia's suggestion)
def prefix_search(pssearch):
    params = default_params()
    params["action"] = "query"
    params["list"] = "prefixsearch"
    params["pssearch"] = pssearch

    results_json = send_request(params)

    if 'error' in results_json
        if results_json['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
            raise HTTPTimeoutError(pssearch)
        else:
            raise WikipediaException(results_json['error']['info'])

    top_result_id = results_json['query']['prefixsearch'][0]['title'], results_json['query']['prefixsearch'][0]['pageid']

    return top_result_id


def parse_sections(pageid):
    params = default_params()
    params["action"] = "parse"
    params["pageid"] = pageid
    params["prop"] = "sections"

    send_request(params)


def parse_content(pageid, section=None, count=0):
    params = {}


def send_request(params):
    headers = default_headers()

    global API_URL
    results = requests.get(API_URL, params=params, headers=headers)
    return results.json()
