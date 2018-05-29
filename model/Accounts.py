from services.AccountServices import *
import mongoengine as mongoengine
from Transactions import Transaction     #, Transaction
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


    # def withdraw(self, aamount):
    #     #withdraw funds from account: must have sufficient balance. Balance cannot be negative
    #     if not self.validateamount(aamount):
    #         response = 'Cannot be transacted for {}. Amount is a negative number. Withdrawal attempt: {}'.format(self.accountnumber, aamount)
    #         return response
    #     if self.balance - aamount < self.minbalance:
    #         response = 'Cannot be transacted for {}. Resulting in below minimum balance. Withdrawal attempt: {}' .format(self.accountnumber, amount)
    #         return response
    #     else:
    #         self.balance -= aamount
    #         #####################################################
    #         trans = Transaction(typetrans="WITHDRAW", amount=aamount, balance=self.balance)
    #         self.transactions.append(trans)  # add transaction to transactions list under Account
    #         self.save_account()
    #         response = "Withrawal successful: {}. Balance is now {}" .format(aamount, self.balance)
    #         return response


    # def deposit(self, aaccountid, aamount):
    #     #deposit funds to account: must be postive amount
    #     acs = AccountServices()
    #     if not acs.account_exists(aaccountid):      #If account does not exist... then cannot make deposit
    #     #if not self.account_exists(aaccountid):
    #         response = 'Cannot perform action. Account does not exist for {} - accountid: {} ' .format(aaccountid)
    #         return response
    #     ##retrieve account
    #     self.__objects.get(aaccountid)
    #     if not self.validateamount(aamount):
    #         response = 'Cannot be transacted for {}. Amount is a negative number. Deposit attempt: {}'.format(self.accountnumber, aamount)
    #         return response
    #     self.balance += aamount
    #    ######### self.save_transaction("Deposit", amount)
    #     trans = Transaction(typetrans="DEPOSIT", amount=aamount, balance=self.balance)
    #     self.transactions.append(trans)     #add transaction to transactions list under Account
    #     self.save_account()
    #     response = "Deposit successful: {}. Balance is now {}".format(aamount, self.balance)
    #     return response


    def validateamount(self, transamount):
        if transamount < 0:
            return False
        else:
            return True


    def getbalance(self):
        print 'Balance request: Balance is: {} ' .format(self.balance)
        return self.balance


    def sendtojson(self):
        return self.to_json()


    def save_account(self):
        try:
            self.save()
            return True
        except:
            print "exception occurred"
            return False