# -*- coding: utf-8 -*-
import os
from random import randint
from datetime import datetime
from lib.database import person

store = person.people_save
query = person.people_find
Person = person.Person

uid_base = randint(86344422, 986344422)
PERSON_LENGTH = 5

EXPORT_STORE_FILE = './twitter_persons.test.json'

info = {
    "name": "testname",
    "fullname": "Test Full name",
    "uid": uid_base,
    "description": "This people info for unit test.",
    "sign_at": datetime.now(),
    "protect": False,
    "friends_count": 4,
    "location": "Chicago",
    "followers_count": 6
}

def people_info_save(info):
    store(**info)

def save_many_same_test():
    people_info_save(info)
    people_info_save(info)
    people_info_save(info)
    assert Person.objects().count() is 1
    # It should save as only one, and not raise error.

def save_many_diff_test():
    for i in range(0, PERSON_LENGTH):
        people_info_save(info)
        info["uid"] = info["uid"] + 1
    assert Person.objects().count() == 1 + i

def person_find_test():
    index = uid_base
    people = query(name=info['name'])
    assert people.name == info['name']
    for i in range(0, PERSON_LENGTH):
        people = query(uid=index + i)
        assert people.uid == index+i

def person_read_all_test():
    index = uid_base
    for people in Person.objects().order_by("uid"):
        assert people.uid == index
        index += 1

def get_person_uids_test():
    index = uid_base
    uids = person.get_uids()
    assert len(uids) is PERSON_LENGTH
    for i in range(0, PERSON_LENGTH):
        assert index+i in uids

def export_person_collection_test():
    index = uid_base
    uids = [index + i for i in range(0, PERSON_LENGTH)]
    person.export_persons(EXPORT_STORE_FILE, uids, limit=10)

def person_del_all_test():
    for people in Person.objects():
        people.delete()
    assert Person.objects().count() is 0

def teardown_module():
    Person.drop_collection()
    if os.path.isfile(EXPORT_STORE_FILE):
        os.remove(EXPORT_STORE_FILE)

if __name__ == '__main__':
    save_many_same_test()
    save_many_diff_test()
    person_find_test()
    person_read_all_test()
    get_person_uids_test()
    export_person_collection_test()
    person_del_all_test()
    teardown_module()