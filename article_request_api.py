# Detailed Wikipedia Skill
# Author: Ben Madany

import wiki_requests as wiki
from traceback import format_exc


def request_article(article):
    try:
        title = wiki.prefix_search(article)
        print("Retrieving suggested article: " + str(title))
        categories = wiki.parse_sections(title)
        print("Retrieving article categories:")
        for category in categories:
            subheading, index = category
            print(subheading + " at " + str(index))
    except wiki.GenericWikipediaException as err:
        print(err)
        return False
    except:
        print(format_exc())
        return False
    return True

def request_section(article, section=None):
    try:
        title = wiki.prefix_search(article)
        print ("Retrieving suggested article: " + str(title))
        content = wiki.get_content(title, section=section)
        print("Retrieved content:\n" + content)
    except wiki.GenericWikipediaException as err:
        print(err)
        return False
    except:
        print(format_exc())
        return False
    return True
