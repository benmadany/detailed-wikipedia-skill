# Detailed Wikipedia Skill
# Author: Ben Madany


import wiki_requests as wiki
from traceback import format_exc


def request_suggestion(topic):
    print("Retrieving suggestion for topic: " + topic)
    title = wiki.prefix_search(topic)
    print("Suggested article: " + str(title))
    return title 


def request_article(article):
    print("Retrieving summary for: " + article)
    summary = wiki.get_content(article)
    print("Retrieving article categories:")
    categories = wiki.parse_sections(article)
    categories = [category for category in categories if category[0].lower() != 'image gallery' and category[0].lower() != 'see also' and category[0].lower() != 'references' and category[0].lower() != 'external links']
    results = (summary.split('\n'), categories)
    print(results)
    return results


def request_section(article, section):
    print("Retrieving content for: " + article)
    content = wiki.get_content(article, section=section)
    print("Retrieved content:\n" + content)
    return content.split('\n')


def split_text(text):
    max_lines = 13
    line_split = text.split('\n')
    results = []
    current = []
    i = 0
    list_set = False
    while i < len(line_split):
        chunk = line_split[i]
        current.append(chunk)
        if chunk.endswith('.'):
            if list_set:
                del current[-1]
                results.append('\n'.join(current))
                list_set = False
                continue
            lines = chunk.count('. ')
            if lines > max_lines:
                if len(current) >= 1:
                    del current[-1]
                results.append('\n'.join(current))
                continue
        else:
            if not list_set:
                del current[-1]
                results.append('\n'.join(current))
                continue
            else:
                list_set = True
        i = i + 1
            
