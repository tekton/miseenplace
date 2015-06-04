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
sudo apt-get -y install git curl
git clone https://[[oauth]]@github.com/[[company_github]]/[[cookbooks]].git
echo "cookbook_path [\\"/opt/[[company]]/[[cookbooks]]\\"]" >> /opt/[[company]]/[[client_rb]]
echo "environment_path [\\"/opt/[[company]]/[[cookbooks]]/environments\\"]" >> /opt/[[company]]/[[client_rb]]
echo "role_path [\\"/opt/[[company]]/[[cookbooks]]/roles\\"]" >> /opt/[[company]]/[[client_rb]]
echo "local_mode true" >> /opt/[[company]]/[[client_rb]]
[[chef_install]]
echo "You should update the dev.json in \"/opt/[[company]]/[[cookbooks]]/environments\" before continuing..."
echo "Run your setup by running: sudo chef-client -z -c /opt/[[company]]/[[client_rb]] -j /opt/[[company]]/[[cookbooks]]/[[dev_setup_json]]"
"""

json_document = """{
"run_list": [[[recipes]]]
}"""


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


class JsonDoc(Document):
    company = StringField(required=True)  # needs to resolve down to name later
    user = LongField(required=True)  # for filtering really
    root = StringField(default=json_document)
    recipes = ListField()
    attributes = StringField()


class DefaultDoc(Document):
    company = StringField(required=True)  # needs to resolve down to name later
    user = LongField(required=True)  # for filtering really
    oauth = StringField(required=True, unique=False)  # custom per setup, genreated at github.com
    opt_level = LongField(default=777)  # default 777
    cookbooks = StringField(default="cookbooks")  # name of the repo and checklout location: ie cookbooks
    dev_setup_json = StringField(default="jsons/dev_setup.json")  # requires extension: ie dev_setup.json
    client_rb = StringField(default="client.rb")  # default to client.rb
    chef_install = StringField(default="curl -L https://www.chef.io/chef/install.sh | sudo bash")  # for chef client
    company_github = StringField(required=True)
