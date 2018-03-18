# Detailed Wikipedia Skill
# Author: Ben Madany


import wiki_requests as wiki
from traceback import format_exc


def request_suggestion(topic):
    try:
        print("Retrieving suggestion for topic: " + topic)
        title = wiki.prefix_search(topic)
        print("Suggested article: " + str(title))
        return title 
    except Exception as e:
        print(format_exc)
        raise e


def request_article(article):
    try:
        print("Retrieving summary for: " + article)
        summary = wiki.get_content(article)
        print("Retrieving article categories:")
        categories = wiki.parse_sections(article)
        categories = [category for category in categories if category[0].lower() != 'image gallery' and category[0].lower() != 'see also' and category[0].lower() != 'references' and category[0].lower() != 'external links']
        results = (summary, categories)
        print(results)
        return results
    except Exception as e:
        print(format_exc)
        raise e


def request_section(article, section):
    try:
        print("Retrieving content for: " + article)
        content = wiki.get_content(article, section=section)
        print("Retrieved content:\n" + content)
        return content
    except Exception as e:
        print(format_exc)
        raise e