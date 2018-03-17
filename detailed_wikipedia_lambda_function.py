# Detailed Wikipedia Skill
# Author: Ben Madany


from __future__ import print_function
import skill_functions


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response(help):
    should_end_session = False
    if not help:
        card_title = "Welcome"
        speech_output = "Welcome to Detailed Wikipedia. Please tell me what you would like to find information on."
        reprompt_text = "Please tell me what article you would like information on by saying something like, get info on Stephen Hawking."
    else:
        card_title = "Help"
        speech_output = "You can use this skill to find information on any topic on Wikipedia. " \
        "When you know what you want to research, ask me, and I'll help you get specific information about that topic or sub-categories of its Wikipedia page. " \
        "For example, you can ask me about info related to Stephen Hawking, and I'll ask if you want a summary or a list of possible sub-categories from his page, such as publications."
        reprompt_text = "I can help you get specific information about that topic or sub-categories of its Wikipedia page. " \
        "For example, you can ask me about info related to Stephen Hawking, and I'll ask if you want a summary or a list of possible sub-categories from his page, such as publications."
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Goodbye"
    speech_output = "Thank you for doing research with Detailed Wikipedia. " \
                    "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def handle_error(error, msg=None):
    print(error)
    card_title = "Error Encountered"
    speech_output = msg if msg else "I'm sorry, I encountered an error and can't complete your request."
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


def start_research(intent, session):
    card_title = "Article Request"
    should_end_session = False

    if 'Article' in intent['slots']:
        article = intent['slots']['Article']['value']
        session['attributes']['requested_article'] = article
        try:
            suggested_article = skill_functions.request_suggestion(article)
            session['attributes']['article'] = suggested_article
            speech_output = "I found an article titled: " + suggested_article + " on Wikipedia. Would you like its summary, or its categories?"
            reprompt_text = "I found an article titled: " + suggested_article + " on Wikipedia. Would you like its summary, or its categories?"
        except skill_functions.wiki.PageNotFoundException:
            speech_output = "I'm sorry, I was unable to find an article matching your request on Wikipedia. Feel free to try again by saying something like, get info on Stephen Hawking."
            reprompt_text = "I'm sorry, I was unable to find an article matching your request on Wikipedia. Feel free to try again by saying something like, get info on Stephen Hawking."
        except skill_functions.wiki.GenericWikipediaException:
            speech_output = "I'm sorry, I encountered an error while talking to Wikipedia and was unable to complete your request. Feel free to try again by saying something like, get info on Stephen Hawking."
            reprompt_text = "I'm sorry, I encountered an error while talking to Wikipedia and was unable to complete your request. Feel free to try again by saying something like, get info on Stephen Hawking."
    else:
        # TODO: If this slot is required will this ever be reached?
        speech_output = "Impossible"
        reprompt_text = None
        should_end_session = True
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'] + " sessionAttributes=" + str(session['attributes']))


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'] + " sessionAttributes=" + str(session['attributes']))
    # Dispatch to your skill's launch
    return get_welcome_response(False)


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'] + " sessionAttributes=" + str(session['attributes']))

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == 'RequestArticleIntent':
        return start_research(intent, session)
    elif intent_name == 'AMAZON.HelpIntent':
        return get_welcome_response(True)
    elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    # User ends session or (external) error occurs, return no response
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'] + " sessionAttributes=" + str(session['attributes']))
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    try:
        if 'attributes' not in event['session']:
            event['session']['attributes'] = {}

        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']},
                            event['session'])

        if event['request']['type'] == 'LaunchRequest':
            return on_launch(event['request'], event['session'])
        elif event['request']['type'] == 'IntentRequest':
            return on_intent(event['request'], event['session'])
        elif event['request']['type'] == 'SessionEndedRequest':
            return on_session_ended(event['request'], event['session'])
    except Exception as e:
        # Catch-all, should (ideally) never be reached because of more specific error handling
        return handle_error(e)
