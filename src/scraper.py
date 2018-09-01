import feedparser
from time import sleep

def fetch():
    url = "http://www.dusken.no/feed"
    content = feedparser.parse(url)
    if "entries" in content.keys():
        return content["entries"]
    else:
        return None

def diff_entries(old_entries, new_entries):
    for entry in new_entries:
        if "guid" in entry.keys():
            title = entry["guid"]
            if title not in [e["guid"] for e in old_entries]:
                yield entry

def entries_to_messages(entries):
    for entry in entries:
        if "title" in entry.keys() and "link" in entry.keys():
            yield entry["title"] + "\n" + entry["link"]

def send_message(message):
    pass

def get_new_entries():
    new_entries = fetch()
    for i in range(10):
        sleep(60)
        old_entries = new_entries[:]
        new_entries = fetch()
        if new_entries is not None:
            diff = diff_entries(old_entries, new_entries)
            messages = entries_to_messages(diff)
            for msg in messages:
                yield msg
