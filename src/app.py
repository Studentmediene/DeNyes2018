from flask import Flask
from flask_apscheduler import APScheduler
from client import send_message
from scraper import fetch, get_new_entries
from time import sleep


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

if __name__ == '__main__':
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()

