import json

from flask import Flask, request, make_response
from flask_apscheduler import APScheduler
from client import send_message, verification_token
from scraper import fetch, get_new_entries, entries_to_messages


app = Flask(__name__)
new_entries = fetch()


class Config(object):
    JOBS = [
        {
            'id': 'example',
            'func': 'app:post_new_entries',
            'trigger': 'cron',
            'second': '0',
        }
    ]

    SCHEDULER_API_ENABLED = True


def post_new_entries():
    global new_entries
    existing_entries = new_entries[:]
    new_entries = fetch()
    for msg in get_new_entries(existing_entries, new_entries):
        send_message(msg)


@app.route('/events', methods=['GET', 'POST'])
def derp():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json" })

    if verification_token != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                %s\n\n" % (slack_event["token"], verification_token.verification)

        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event = slack_event['event']
        if "text" in event.keys() and event['text'].startswith('!last'):
            number = 1
            split = event['text'].split(" ")
            if len(split) > 1:
                number = int(split[1])
            last = list(fetch())[:number]
            for message in entries_to_messages(last):
                send_message(message)
            return make_response("OK", 200, {})

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                             you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(host='0.0.0.0', port=80)
