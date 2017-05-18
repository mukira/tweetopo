# -*- coding: utf-8 -*-
import logging
import queue
import time
from threading import Thread
from twitter.tweeapi import Twitter
import logsetting
from conffor import conffor
import database as db

store = db.person.people_save
query = db.person.people_find

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
db.set_connect(**config["mongo"])
founds = set(db.person.get_uids())
seed_name = config['seed_name']
tokens = config["twitter"]

def store_user(twitter, uid=None, name=None):
    twitter.get_user(user_id=uid, screen_name=name).store_user(store)

def get_seed_people(seed_name):
    people = query(name=seed_name)
    if not people:
        store_user(Twitter(**tokens[0]), name=seed_name)
        people = query(name=seed_name)
    return people

def get_unfound_queue(friends, founds):
    unfound_set = set(friends) - set(founds)
    unfounds = queue.Queue()
    for uid in unfound_set:
        unfounds.put(uid)
    return unfounds

def query_from_queue(index, twitter, unfounds):
    time.sleep(index)
    logging.info('Thead-%d : tasks started!' %index)
    while not unfounds.empty():
        uid = unfounds.get_nowait()
        store_user(twitter, uid=uid)
    logging.info('Thead-%d : task complete!' %index)

def start_travers_crawling(tokens, unfounds, block=True):
    tasks = []
    for index, token in enumerate(tokens):
        twitter = Twitter(**token)
        task = Thread(target=query_from_queue, args=(index+1, twitter, unfounds))
        tasks.append(task)
        task.start()
    logging.info('Tasks all started!')
    if block:
        for task in tasks:
            task.join()
        logging.info('Tasks all complete!')

def export_person_list(filename, seed_name=None):
    db.person.export_relation(filename, seed_name=seed_name)

if __name__ == "__main__":
    people = get_seed_people(seed_name)
    unfounds = get_unfound_queue(people.friends, founds)
    start_travers_crawling(tokens, unfounds)
    export_person_list('twitter_relations.json')
