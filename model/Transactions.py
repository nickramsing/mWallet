from mongoengine import *
import datetime

## Class for mongoengine - interaction with MongoDB
class Transaction(EmbeddedDocument):
    datetrans = DateTimeField(default=datetime.date.today)
    typetrans = StringField()
    amount = FloatField()
    balance = FloatField()
    timestamp = DateTimeField(default=datetime.datetime.now)


    meta = {
    #    'db_alias': 'core',
        'collection': 'accounts',
        'indexes': [
            'datetrans',
            'typetrans'
        ],
        'ordering': ['datetrans']
    }


#    def save_transaction(self):
#        return "ARgh"

