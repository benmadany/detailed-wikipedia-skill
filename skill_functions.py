# Detailed Wikipedia Skill
# Author: Ben Madany


import wiki_requests as wiki
from traceback import format_exc


# Uses the prefixsearch Wikipedia API query to retrieve the top suggestion for a given search query (topic)
def request_suggestion(topic):
    print("Retrieving suggestion for topic: " + topic)
    title = wiki.prefix_search(topic)
    print("Suggested article: " + str(title))
    return title 


# Uses a combination of text extracts and parsing to collect a Wikipedia page's summary and table of contents, then returns a tuple with the summary and filtered toc
def request_article(article):
    print("Retrieving summary for: " + article)
    summary = wiki.get_content(article)
    print("Retrieving article categories:")
    categories = wiki.parse_sections(article)
    categories = [category for category in categories
    if category[0].lower() != 'image gallery' and category[0].lower() != 'see also' and category[0].lower() != 'references' and category[0].lower() != 'external links' and category[0].lower() != 'further reading']
    results = (summary, categories)
    print(str(results))
    return results


# Uses parsing (or text extracts if no section is given) to collect the raw text of a section of a Wikipedia page, filters out html tags and other notation to present only human readable text
def request_section(article, section):
    print("Retrieving content for: " + article)
    content = wiki.get_content(article, section=section)
    print("Retrieved content:\n" + str(content))
    return content  
