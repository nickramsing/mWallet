from services.AccountServices import *
import mongoengine as mongoengine
from model.Transactions import Transaction     #, Transaction
import datetime


## Class for mongoengine - interaction with MongoDB
class Account(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    accountid = mongoengine.StringField(required=True)
    balance = mongoengine.FloatField()
    minbalance = mongoengine.FloatField()
    lastupdate = mongoengine.DateTimeField(default=datetime.datetime.now)
    #connection to account transactions
    #transactions = mongoengine.EmbeddedDocumentField(Transaction)
    transactions = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Transaction))

    meta = {
    #    'db_alias': 'core',
        'collection': 'accounts',
        'indexes': [
            'name',
            'accountid'
        ],
        'ordering': ['accountid']
    }



    def validateamount(self, transamount):
        if transamount < 0:
            return False
        else:
            return True


    def getbalance(self):
        print( 'Balance request: Balance is: {} ' .format(self.balance))
        return self.balance


    def sendtojson(self):
        return self.to_json()


    def save_account(self):
        try:
            self.save()
            return True
        except:
            print( "exception occurred")
            return False