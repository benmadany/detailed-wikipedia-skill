# Detailed Wikipedia Skill
# Author: Ben Madany


from __future__ import print_function
from traceback import format_exc
from random import choice
import skill_functions
import static


# --------------- Response JSON constructors ----------------------

def build_speechlet_response(title, output, reprompt_output, should_end_session, plaintext=True):
    return {
        'outputSpeech': {
            'type': 'PlainText' if plaintext else 'SSML',
            'text' if plaintext else 'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText' if plaintext else 'SSML',
                'text' if plaintext else 'ssml': reprompt_output
            }
        },
        'shouldEndSession': should_end_session        
    }


def build_elicit_response(slot_to_elicit, updated_intent, speechlet_response):
    speechlet_response['directives'] = [{
            'type': 'Dialog.Elicit',
            'slotToElicit': slot_to_elicit,
            'updatedIntent': updated_intent
        }]
    return speechlet_response


def build_delegate_response(updated_intent=None):
    return {'directives': [
        {'type': 'Dialog.Delegate'}
    ]}


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Utility functions ------------------


def select(prompts):
    return choice(prompts)
    

def generate_reading_output(session):
    current_reading = session['attributes']['current_reading']
    current_index = session['attributes']['current_index']
    text = "<p>" + current_reading[current_index]  + "</p>"
    max_index = len(current_reading) - 1
    if current_index == max_index:
        prompt = "<p>\nIs there anything else you would like to search for?</p>" # TODO: select from set of prompts
        session['attributes']['state'] = static.waiting
    else:
        prompt = "<p>\nWould you like me to read more?</p>"
        session['attributes']['state'] = static.reading
        session['attributes']['current_index'] = current_index + 1
    speech_output = "<speak>" + text + prompt + "</speak>"
    reprompt_output = "<speak>" + prompt + "</speak>"
    return speech_output, reprompt_output


# --------------- Error handlers ------------------


def handle_error(error, msg=None):
    print(format_exc())
    card_title = "Error Encountered"
    speech_output = msg if msg else select(static.error_prompts)
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


# --------------- Intent and other skill functions ------------------


def get_welcome_response(help):
    should_end_session = False
    if not help:
        card_title = "Welcome"
        speech_output = static.welcome_message
        reprompt_output = static.welcome_reprompt
    else:
        card_title = "Help"
        speech_output = static.help_message
        reprompt_output = static.help_reprompt
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_output, should_end_session))


def handle_session_end_request():
    card_title = "Goodbye"
    speech_output = "Thanks for using Detailed Wikipedia. " \
                    "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def article_intent(intent, session):
    card_title = "Article Request"
    should_end_session = False

    if 'Article' in intent['slots']:
        article = intent['slots']['Article']['value']
        session['attributes']['requested_article'] = article
        try:
            suggested_article = skill_functions.request_suggestion(article)
            session['attributes']['article'] = suggested_article
            session['attributes']['state'] = 'STATE.START'
            speech_output = select(static.found_article_prompts).format(suggested_article)
            reprompt_output = select(static.found_article_prompts).format(suggested_article)
        except skill_functions.wiki.PageNotFoundException:
            speech_output = select(static.page_not_found_prompts)
            reprompt_output = select(static.page_not_found_prompts)
        except skill_functions.wiki.GenericWikipediaException:
            speech_output = select(static.wikipedia_exception_prompts)
            reprompt_output = select(static.wikipedia_exception_prompts)
    else:
        # If this slot is required will this ever be reached now that dialog delegation is used?
        # TODO: Raise custom exception
        raise Exception("Unreachable")
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_output, should_end_session))


def summary_intent(intent, session):
    card_title = "Summary"
    should_end_session = False

    if 'Article' in intent['slots'] and 'value' in intent['slots']['Article']:
        article = intent['slots']['Article']['value']
        session['attributes']['requested_article'] = article
        suggested_article = skill_functions.request_suggestion(article)
        session['attributes']['article'] = suggested_article
        summary, categories = skill_functions.request_article(suggested_article)
    else:
        summary, categories = skill_functions.request_article(session['attributes']['article'])
    session['attributes']['summary'] = summary
    session['attributes']['categories'] = categories
    current_index = 0
    session['attributes']['current_index'] = current_index
    session['attributes']['current_reading'] = summary

    speech_output, reprompt_output = generate_reading_output(session)
    
    response = build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_output, should_end_session, False))
    print("summary_intent response=" + str(response))
    return response


def category_intent(intent, session):
    card_title = "Categories"
    should_end_session = False

    if 'Article' in intent['slots'] and 'value' in intent['slots']['Article']:
        article = intent['slots']['Article']['value']
        session['attributes']['requested_article'] = article
        suggested_article = skill_functions.request_suggestion(article)
        session['attributes']['article'] = suggested_article
        summary, categories = skill_functions.request_article(suggested_article)
    else:
        summary, categories = skill_functions.request_article(session['attributes']['article'])
    session['attributes']['summary'] = summary
    session['attributes']['categories'] = categories
    
    # TODO: Implement Category slot on CategoryIntent for describing category by name or position ex: first, 3, History, etc. then send elicit slot directive
    top_level_categories = [category[0] for category in categories if category[2] == 1]
    speech_output = "<speak><p>Categories:\n" + ', '.join(top_level_categories[:-1]) + ", and " + top_level_categories[-1] + "</p><p>\nWhich category would you like me to read?</p></speak>"
    reprompt_output = "<speak>Which category would you like me to read?</speak>"

    session['attributes']['state'] = 'STATE.CATEGORIES'

    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_output, should_end_session, False))


def yes_intent(intent, session):
    card_title = "Affirmative"
    should_end_session = False
    # TODO: Improve logging
    speech_output, reprompt_output = generate_reading_output(session)
    
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_output, should_end_session, False))



def no_intent(intent, session):
    card_title = "No"
    should_end_session = False

    if session['attributes']['state'] == 'STATE.SUMMARY':
        speech_output = "Sure."
        reprompt_output = None

    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_output, should_end_session, False))


# --------------- Event handlers ------------------

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
    # TODO: Improve logging

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == 'RequestArticleIntent':
        dialog_state = intent_request['dialogState']
        print("on_intent dialogState=" + dialog_state)
        if dialog_state != 'COMPLETED':
            return build_response({}, build_delegate_response())
        else:
            return article_intent(intent, session)
    elif intent_name == 'RequestSummaryIntent':
        return summary_intent(intent, session)
    elif intent_name == 'RequestCategoriesIntent':
        return category_intent(intent, session)
    elif intent_name == 'AMAZON.YesIntent':
        return yes_intent(intent, session)
    elif intent_name == 'AMAZON.NoIntent':
        return no_intent(intent, session)
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
