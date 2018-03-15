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
    except wiki.GenericWikipediaException as wiki_error:
        print("Wikipedia Exception: " + wiki_error)
    except:
        print(format_exc())
    return None


def request_article(article):
    try:
        print("Retrieving summary for: " + article)
        summary = wiki.get_content(article)
        print("Retrieving article categories:")
        categories = wiki.parse_sections(article)
        for category in categories:
            subheading, index, depth = category
            print(subheading + " at " + str(index) + " with depth " + str(depth))
        return (summary, categories)
    except wiki.GenericWikipediaException as wiki_error:
        print("Wikipedia Exception: " + wiki_error)
    except:
        print(format_exc())
    return None


def request_section(article, section):
    try:
        print("Retrieving content for: " + article)
        content = wiki.get_content(article, section=section)
        print("Retrieved content:\n" + content)
        return content
    except wiki.GenericWikipediaException as wiki_error:
        print("Wikipedia Exception: " + wiki_error)
    except:
        print(format_exc())
    return None