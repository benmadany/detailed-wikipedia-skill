# Detailed Wikipedia Skill
# Author: Ben Madany


from bs4 import BeautifulSoup
try:
    import requests
except:
    from botocore.vendored import requests
import sys
import re


# Wikipedia API endpoint, starting language code determines which Wiki to use
API_URL = "http://en.wikipedia.org/w/api.php"
# User Agent that must be specified in headers of requests sent to Wikipedia API
USER_AGENT = "Detailed Wikipedia Skill (https://github.com/benmadany/detailed-wikipedia-skill)"


# Generic Exception for errors returned by Wikipedia API
class GenericWikipediaException(Exception):

    def __init__(self, error):
        self.error = error

    def __unicode__(self):
        return "The following error occured: {0}".format(self.error)

    def __str__(self):
        if sys.version_info > (3,0):
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf8')


# Exception raised when no search suggestions are available
class PageNotFoundException(Exception):

    def __init__(self, article):
        self.article = article

    def __unicode__(self):
        return "Could not find a page suggestion for the input: {0}".format(self.article)

    def __str__(self):
        if sys.version_info > (3,0):
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf8')


# Logging wrapper
def log_msg(msg, error=0):
    print("Error:\n------------\n" if error else "Info:\n------------\n" + msg + "\n------------")


# Utility method to strip extra newlines from text, remove references and links (text surrounded by '[]' or lines beginning with '^'), and remove parentheticals that contain removed references
def clean_text(text):
    #log_msg("Before cleaning:\n" + text)
    text = re.sub('(^\^.*$)|(\([^\)]*\[[^\]]*\][^\)]*\)+)|(\[[^\]]*\]\([^\)]*\))|(\[[^\]]*\])', '', text, flags=re.MULTILINE)
    text = re.sub('(\n{2,})', '\n', text)
    #log_msg("After cleaning:\n" + text)
    return text


# Creates dict containing common parameters for the Wikipedia API requests that will be made
def default_params():
    params = {'format':'json', 'redirects':1}
    return params


# Creates dict containing common headers for any Wikipedia API requests
def default_headers():
    global USER_AGENT
    headers = {'User-Agent': USER_AGENT}
    return headers


# Request prefix search of a specific article, returns the title of the first result (Wikipedia's suggestion)
def prefix_search(pssearch):
    params = default_params()
    params['action'] = 'query'
    params['list'] = 'prefixsearch'
    params['pssearch'] = pssearch

    results_json = send_request(params)

    if 'error' in results_json:
        raise GenericWikipediaException(results_json['error']['info'])
    if not results_json['query']['prefixsearch']:
        raise PageNotFoundException(pssearch)

    top_result = results_json['query']['prefixsearch'][0]['title']

    return top_result


# Request parse action with the 'sections' property specified, returns a list of tuples containing all the sub-headings, their indexes, and their depth of an article
def parse_sections(page):
    params = default_params()
    params['action'] = 'parse'
    params['page'] = page
    params['prop'] = 'sections'

    results_json = send_request(params)

    if 'error' in results_json:
        raise GenericWikipediaException(results_json['error']['info'])

    sections = ((section['line'], section['index'], section['toclevel']) for section in results_json['parse']['sections'])

    return list(sections)


# Request content of a page summary or a section, returns parsed and cleaned text from Wikipedia
def get_content(page, section=None, count=0):
    params = default_params()
    if section is not None:
        params['action'] = 'parse'
        params['page'] = page
        params['section'] = section
        params['prop'] = 'text'
    else:
        params['action'] = 'query'
        params['titles'] = page
        params['prop'] = 'extracts'
        params['exintro'] = 1

    results_json = send_request(params)

    if 'error' in results_json:
        raise GenericWikipediaException(results_json['error']['info'])

    content = ""
    if section is not None:
        content = remove_html_and_captions(results_json['parse']['text']['*'])
    else:
        content = remove_html_and_captions(results_json['query']['pages'][list(results_json['query']['pages'])[0]]['extract'])

    return clean_text(content)


# Sends http request to Wikipedia API returning a dictionary of the retrieved content in json format
def send_request(params):
    headers = default_headers()

    global API_URL
    log_msg("Sending request to: " + API_URL + "\nParameters: " + str(params) + "\nHeaders: " + str(headers))
    results = requests.get(API_URL, params=params, headers=headers)
    results_json = results.json()
    log_msg("Received: " + str(results) + "\n" + str(results_json))
    return results_json


# Uses BeautifulSoup to remove html tags and divs that contain captions or navigation hatnotes since they shouldn't be read
def remove_html_and_captions(html):
    soup = BeautifulSoup(html, 'lxml')
    for div in soup.find_all('div', class_=re.compile('(.*caption.*)|(hatnote navigation-not-searchable)|(toc)')):
        div.decompose()
    return soup.text
