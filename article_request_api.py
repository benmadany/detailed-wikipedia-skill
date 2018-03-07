# Detailed Wikipedia Skill
# Author: Ben Madany

import wikipedia as wiki
from traceback import format_exc


def request_article(article):
    try:
        top_result = wiki.search(article, 1)[0]
        print("Retrieving suggested article: " + str(top_result))
        summary = wiki.summary(top_result)
        print("Retrieved summary")
        page = wiki.page(top_result)
        print("Retrieved page data")
        # TODO: modify wiki request api to retrieve section headings
        for category in page.categories:
            print(category)
    except wiki.DisambiguationError as err:
        print(err)
        return False
    except wiki.PageError as err:
        print(err)
        return False
    except:
        print(format_exc())
        return False
    return True

def request_section(article, section):
    try:
        top_result = wiki.search(article, 1)[0]
        print ("Retrieving suggested article: " + str(top_result))
        page = wiki.page(top_result)
        print("Retrieved page data")
        # TODO: modify wiki request api to retrieve section summaries
    except:
        print(format_exc())
        return False
    return True
