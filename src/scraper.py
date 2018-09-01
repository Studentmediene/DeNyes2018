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
        if "id" in entry.keys():
            guid = entry["id"]
            if guid not in [e["id"] for e in old_entries]:
                yield entry

def entries_to_messages(entries):
    for entry in entries:
        if "title" in entry.keys() and "link" in entry.keys():
            yield entry["title"] + ":\n" + entry["link"]

def get_new_entries(existing_entries, new_entries):
    if new_entries is not None:
        diff = diff_entries(existing_entries, new_entries)
        return entries_to_messages(diff)
