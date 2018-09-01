from flask import Flask
from flask_apscheduler import APScheduler


app = Flask(__name__)


class Config(object):
    JOBS = [
        {
            'id': 'example',
            'func': 'app:example',
            'trigger': 'cron',
            'second': '*',
        }
    ]

    SCHEDULER_API_ENABLED = True


def example():
    app.logger.error('Hello')


if __name__ == '__main__':
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()
