import mongoengine as mongoengine
from Transactions import TransactionsDB     #, Transaction
import datetime


## Class for mongoengine - interaction with MongoDB
class AccountDB(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    accountid = mongoengine.StringField(required=True)
    balance = mongoengine.FloatField()
    minbalance = mongoengine.FloatField()
    lastupdate = mongoengine.DateTimeField(default=datetime.datetime.now)
    #connection to account transactions
    transactions = mongoengine.EmbeddedDocumentField(TransactionsDB)

    meta = {
    #    'db_alias': 'core',
        'collection': 'accounts',
        'indexes': [
            'name',
            'accountid'
        ],
        'ordering': ['accountid']
    }

#===================
## operational class
class Account:
    name = ""
    accountid = ""
    balance = 0
    minbalance = 0
    transactions = {}

    def __init__(self):         #, aname, aaccountid):
        self.name = ""
        self.accountid = ""
        self.balance = 0
        self.minbalance = 0
        self.transactions = {}


    def registeraccount(self, accountid, personname):
        # #populate object with data to be saved
        self.accountid = accountid
        self.name = personname
        # ##### NEED TO DETERMINE IF EXISTS ALREADY!!!!
        if self.find_account(accountid):    #If DOES ALREADY EXIST, then stop and inform
            response = 'Cannot register account. Account already exists for {} - accountid: . .'.format(personname, accountid)
            return response
        #Does not exist, then save account
        else:
            success = self.save_account()  # store an account
            if success == True:  # new account saved successfully
                 response = 'New account {} created for {}. Initial balance: {}'.format(self.accountid, self.name, self.balance)
            else:  # not saved successfully
                 response = 'Problems creating account for {}. Please try again - or contact representative.'.format(self.name)
            print response
        return response

    def withdraw(self, amount):
        #withdraw funds from account: must have sufficient balance. Balance cannot be negative
        if not self.validateamount(amount):
            response = 'Cannot be transacted for {}. Amount is a negative number. Withdrawal attempt: {}'.format(self.accountnumber, amount)
            return response
        if self.balance - amount < self.minbalance:
            response = 'Cannot be transacted for {}. Resulting in below minimum balance. Withdrawal attempt: {}' .format(self.accountnumber, amount)
            return response
        else:
            self.balance -= amount
            #####################################################
            self.save_transaction("Withdrawl", amount)
            response = "Withrawal successful: {}. Balance is now {}" .format(amount, self.balance)
            return response


    def deposit(self, amount):
        #deposit funds to account: must be postive amount
        if not self.validateamount(amount):
            response = 'Cannot be transacted for {}. Amount is a negative number. Deposit attempt: {}'.format(self.accountnumber, amount)
            return response
        self.balance += amount
        self.save_transaction("Deposit", amount)
        response = "Deposit successful: {}. Balance is now {}".format(amount, self.balance)
        return response

    def validateamount(self, transamount):
        if transamount < 0:
            return False
        else:
            return True


    def getbalance(self):
        print 'Balance request: Balance is: {} ' .format(self.balance)
        return self.balance

    # def add_transaction(self, aadate, atype, aamount, abalance, aAccount):
    #     code = str(aadate) + "-" + str(atype)+ "-" + str(aamount)
    #     self.transactions[code] = Transaction(aadate, atype, aamount, abalance, self)
    #     return

#### DB FUNCTIONS: for Account

    def save_account(self):
        accountdb = AccountDB()  # mongoengine DB access
        accountdb.name = self.name
        accountdb.accountid = self.accountid
        accountdb.balance = self.balance
        accountdb.minbalance = self.minbalance
        accountdb.save()
        return True

    def save_transaction(self, transtype, transamount):
        print "save_transaction - parameters passed in: {}".format(transtype, transamount)
        try:
            transaction = TransactionsDB()
            #Note: trransdate and timestamp at set at initialization
            transaction.typetrans = transtype
            transaction.amount = transamount
            transaction.balance = self.balance
            ## THIS IS THE PROBLEM - resets the balance of the existing amount
            # problem is created because of having TWO Account objects
            #accountdb = self.find_account(self.accountid)
            accountdb = AccountDB()
            accountdb.name =self.name
            accountdb.accountid =self.accountid
            accountdb.balance = self.balance
            accountdb.minbalance = self.minbalance
            accountdb.transactions.append(transaction)      #appends transaction to account
            accountdb.save()                                #saves full account
            return True
        except:
            return False

    #def find_account(self, accountid: str) -> AccountDB:
    def find_account(self, accountid):
        print "find_account - accountid parameter passed in: {}" .format(accountid)
        accountdb = AccountDB.objects(accountid=accountid).first()
        if not accountdb:
            return False    #an account object DNE
        else:
            self.name = accountdb.name
            self.accountid = accountdb.accountid
            self.balance = accountdb.balance
            self.minbalance = accountdb.minbalance
            return True     #an account object exists - is not populated