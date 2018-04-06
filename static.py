# Detailed Wikipedia Skill
# Author: Ben Madany


# Skill States
reading = 'reading'
rpause = 'rpause'
waiting = 'waiting'


# Prompts
welcome_message = "Welcome to Detailed Wikipedia. Please tell me what you would like to find information on."
welcome_reprompt = "Please tell me what article you would like information on by saying something like, get info on Stephen Hawking."

help_message = "You can use this skill to find information on any topic on Wikipedia. " \
    "When you know what you want to research, ask me, and I'll help you get specific information about that topic or sub-categories of its Wikipedia page. " \
    "For example, you can ask me about info related to Stephen Hawking, and I'll ask if you want a summary or a list of possible sub-categories from his page, such as publications."
help_reprompt = "I can help you get specific information about that topic or sub-categories of its Wikipedia page. " \
    "For example, you can ask me about info related to Stephen Hawking, and I'll ask if you want a summary or a list of possible sub-categories from his page, such as publications."

error_prompts = ["I'm sorry, I encountered an error and can't complete your request.",
    "Sorry about that, I found an error and can't complete your request."]

page_not_found_prompts = ["I'm sorry, I was unable to find an article matching your request on Wikipedia. Feel free to try again by saying something like, get info on Stephen Hawking."]

wikipedia_exception_prompts = ["I'm sorry, I encountered an error while talking to Wikipedia and was unable to complete your request. Feel free to try again by saying something like, get info on Stephen Hawking."]

found_article_prompts = ["I found an article titled: {}, on Wikipedia. Would you like the summary, or its categories?",
    "I found this Wikipedia article: {}. Would you like its summary or its categories?"]