import os
import json
from bs4 import BeautifulSoup as bs
from some_names import names

SOME_USERS_FILE = "some_users.html"


def load_thread(verbose=False):
    thread_dict = json.load(open("conv.json"))
    thread = thread_dict["_embedded"]["threads"]

    if verbose:
        print(f"Number of messages in thread: {len(thread)}")
    return thread


def process_html(html, replace=None):
    replace = replace or {}
    resp = bs(html, features="html.parser").get_text(" ")
    for key, value in replace.items():
        resp = resp.replace(key, value)

    return resp


def show_message(msg):
    body = process_html(msg.get("body", "!!NO BODY!!"))
    by = msg.get("createdBy", {"first": "!!NO", "last": "AUTHOR!!"})
    when = msg.get("createdAt", "!!NO DATETIME!!")

    print(f"**From: {by['first']} {by['last']} ({when})**")

    if body != "!!NO BODY!!":
        print(body)


def show_thread(thread=None):
    if not thread: 
        thread = load_thread()

    for msg in reversed(thread):
        print("------------------------------")
        show_message(msg)


def get_thread(thread=None, replace=None):
    if not thread: 
        thread = load_thread()

    text = "\n".join([process_html(msg.get("body", "###"), replace=replace) for msg in reversed(thread)])
    return text


def load_users():
    if not os.path.isfile(SOME_USERS_FILE):
        return [{"first_name": name} for name in names]

    soup = bs(open(SOME_USERS_FILE).read(), features="html.parser")
    trs = soup.find_all("tr")

    records = []
    for tr in trs:
        records.append(dict([(td.get("class")[0].split("-")[-1], td.text)
                              for td in tr.find_all("td")
                              if td.text and td.get("class") != ["field-user_type"]]))
    return records



