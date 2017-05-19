# -*- coding: utf-8 -*-
import logging
import queue
import logsetting
from twitter.tweeapi import Twitter
from twitter.tweeapi import multi_tweecrawl
from conffor import conffor
import database as db

relate_store = db.relation.people_save
relate_query = db.relation.people_find
detail_store = db.person.people_save

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
db.set_connect(**config["mongo"])
seed_name = config['seed_name']
tokens = config["twitter"]

def store_relation(twitter, uid=None):
    twitter.store_user_relation(relate_store)

def store_people_details(twitter, uid=None):
    twitter.store_user_details(detail_store)

def get_seed_people(seed_name):
    people = relate_query(name=seed_name)
    if not people:
        Twitter(**tokens[0])\
            .get_user(name=seed_name)\
            .store_user_relation(relate_store)
        people = relate_query(name=seed_name)
    return people

def get_unfound_queue(friends, founds):
    unfound_set = set(friends) - set(founds)
    unfounds = queue.Queue()
    for uid in unfound_set:
        unfounds.put(uid)
    return unfounds

def start_crawling_relation(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, callback=store_relation)

def start_crawling_people_details(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, callback=store_people_details)

def crawl_detail_from_hub():
    from analyse_topology import hub_users_file, read_hub_persons
    hub_persons = read_hub_persons(hub_users_file)
    hub_uids = {int(person[0]) for person in hub_persons}
    founds = db.person.get_uids()
    unfounds = get_unfound_queue(hub_uids, founds)
    start_crawling_people_details(tokens, unfounds)

if __name__ == "__main__":
    # people = get_seed_people(seed_name)
    # founds = set(db.relation.get_uids())
    # unfounds = get_unfound_queue(people.friends, founds)
    # start_crawling_relation(tokens, unfounds)
    # db.relation.export_relation('twitter_relations.json')
    crawl_detail_from_hub()
    db.person.export_persons('hub_persons.json')
