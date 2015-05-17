from mongoengine import *
import pymongo

connect("test", host='127.0.0.1', port=27017, read_preference=pymongo.ReadPreference.PRIMARY)


class Company(Document):
    name = StringField(required=True, unique=True)


class MainDoc(Document):
    company = ReferenceField(Company)
    user = LongField(required=True)
