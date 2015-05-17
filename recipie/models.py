from mongoengine import *
import pymongo
import os

connect("miseenplace",
        host=os.getenv("MONGO_HOST", '127.0.0.1'),
        port=os.getenv("MONGO_PORT", 27017),
        read_preference=pymongo.ReadPreference.PRIMARY)
default_document = """#!/bin/bash
sudo mkdir -p /opt/[[company]]
sudo chmod [[opt_level]] /opt/[[company]]
cd /opt/[[company]]
git checkout http://[[oauth]]@github.com/[[company]]/[[cookbooks]].git
echo "cookbook_path [\"/opt/[[company]]/[[cookbooks]]\"]" >> /opt/[[company]]/[[client_rb]]
[[chef_install]]
echo "Run your setup by running: chef-solo -j /opt/[[company]]/[[cookbooks]]/[[dev_setup_json]] -c /opt/[[company]]/[[client_rb]]"
"""


def get_defaults(class_to_check):
    rtn_dict = {}
    for k in class_to_check._db_field_map:
        try:
            rtn_dict[k] = getattr(class_to_check, k).default
        except AttributeError:
            rtn_dict[k] = None
        except Exception as e:
            print(e)
            rtn_dict[k] = None
    return rtn_dict


class Company(Document):
    name = StringField(required=True, unique=True)


class MainDoc(Document):
    company = ReferenceField(Company)
    user = LongField(required=True)


class DefaultDoc(Document):
    company = StringField(required=True)  # needs to resolve down to name later
    user = LongField(required=True)  # for filtering really
    oauth = StringField(required=True, unique=False)  # custom per setup, genreated at github.com
    opt_level = LongField(default=777)  # default 777
    cookbooks = StringField(default="cookbooks")  # name of the repo and checklout location: ie cookbooks
    dev_setup_json = StringField(default="dev_setup.json")  # requires extension: ie dev_setup.json
    client_rb = StringField(default="client.rb")  # default to client.rb
    chef_install = StringField(default="curl -L https://www.chef.io/chef/install.sh | sudo bash")  # for chef client
