from model.Accounts import Account
from model.Transactions import Transaction
import mongoengine as mongoengine
import logging

## ACCOUNT Business operations:
#   Register client
#   Deposit
#   Withdraw
#   TBD: Transfer
#   Supporting functions: does account exist?
#### changes
# included logging in does account exist: def account_does_exist(aaccountid)


def account_register(aaccountid, personname):
        #Does account already exist?
            # If yes, then cannot register account
            # If no, then register account
        # ##### NEED TO DETERMINE IF EXISTS ALREADY!!!!
        if account_does_exist(aaccountid):
            response = 'Cannot register account. Account already exists for {} - accountid: {} '.format(personname, aaccountid)
            return response
        #Does not exist, then save account: populate object with data to be saved and try to save
        else:       #create account with balances set at zero
            newaccount = Account()
            newaccount.accountid = aaccountid
            newaccount.name = personname
            newaccount.balance = 0
            newaccount.minbalance = 0
            try:
                newaccount.save()  # store an account
                response = 'New account {} created for {}. Initial balance: {}'.format(newaccount.accountid, newaccount.name, newaccount.balance)
            except Exception as e:
                print( "LOG: Could not register and save new account".format(aaccountid))
                print( "Exception type: {} message: {}".format(type(e), e.message))
                response = 'Problems creating account for {}. Please try again - or contact representative.'.format(newaccount.name)
            print( response)
            return response


def account_deposit(aaccountid, aamount):
    #Deposit funds to account: (1) account must exist (2) must be positive amount
    #Outcome:  (1) balance is increased by deposit (2) transaction is stored
    if not account_does_exist(aaccountid):  # If account does not exist... then cannot make deposit
        response = 'Cannot perform action. Account does not exist for {} - accountid: {} '.format(aaccountid)
        return response
    ##retrieve account: obtain account; increase balance; add transaction; save account record
    ac = account_find_record(aaccountid)
    if not account_validateamount(aamount):
        response = 'Cannot be transacted for {}. Amount is a negative number. Deposit attempt: {}'.format(aaccountid, aamount)
        return response
    ac.balance += aamount
    ######### create transaction and associate with account
    trans = Transaction(typetrans="DEPOSIT", amount=aamount, balance=ac.balance)
    ac.transactions.append(trans)  # add transaction to transactions list under Account
    ## put following in Save function
    try:
        ac.save()  # store an account
        response = 'New account {} created for {}. Initial balance: {}'.format(ac.accountid, ac.name, ac.balance)
    except Exception as e:
        print( "LOG: Could not register and save new account".format(aaccountid))
        print( "Exception type: {} message: {}".format(type(e), e.message))
        response = 'Problems creating account for {}. Please try again - or contact representative.'.format(ac.name)
    response = "Deposit successful: {}. Balance is now {}".format(aamount, ac.balance)
    return response


def account_withdraw(aaccountid, aamount):
    #Withdraw funds to account: (1) account must exist (2) must be positive amount (3) must have sufficient balance. Balance cannot be negative
    #Outcome:  (1) balance is decreased by withdrawl(2) transaction is stored
    if not account_does_exist(aaccountid):  # If account does not exist... then cannot make deposit
        response = 'Cannot perform action. Account does not exist for {} - accountid: {} '.format(aaccountid)
        return response
    ##retrieve account: obtain account; increase balance; add transaction; save account record
    ac = account_find_record(aaccountid)
    if not account_validateamount(aamount):
        response = 'Cannot be transacted for {}. Amount is a negative number. Withdrawal attempt: {}'.format(aaccountid, aamount)
        return response
    if ac.balance - aamount < ac.minbalance:
        response = 'Cannot be transacted for {}. Resulting in below minimum balance. Withdrawal attempt: {}'.format(ac.accountid, aamount)
        return response
    ac.balance -= aamount
    #####################################################
    ######### create transaction and associate with account
    trans = Transaction(typetrans="WITHDRAW", amount=aamount, balance=ac.balance)
    ac.transactions.append(trans)  # add transaction to transactions list under Account
    ## put following in Save function
    try:
        ac.save()  # store an account
        response = 'New account {} created for {}. Initial balance: {}'.format(ac.accountid, ac.name, ac.balance)
    except Exception as e:
        print( "LOG: Could not register and save new account".format(aaccountid))
        print( "Exception type: {} message: {}".format(type(e), e.message))
        response = 'Problems creating account for {}. Please try again - or contact representative.'.format(ac.name)
    response = "Withrawal successful: {}. Balance is now {}".format(aamount, ac.balance)
    return response


def account_getbalance(aaccountid):
    #report balance of account, if it exists and can be found
    #does account exist?
    if not account_does_exist(aaccountid):  # If account does not exist... then cannot make deposit
        response = 'Cannot perform action. Account does not exist for {} - accountid: {} '.format(aaccountid)
        return response
    ##retrieve account: obtain balance and respond
    ac = account_find_record(aaccountid)
    response = 'Balance for account {} is {}' .format(aaccountid, ac.balance)
    return response


def account_find_record(aacountid):
    #returns an Account object based on searching for accountid: get returns ONE account
    #insert try except to capture problems
    account_retrieved = Account.objects.get(accountid=aacountid)
    return account_retrieved

def account_does_exist(aaccountid):
    logger = logging.getLogger(__name__)
    logger.info('=== checking: does account exist? ====')
    try:
        result = Account.objects.get(accountid=aaccountid)
        return True  # a single account does exist
    except mongoengine.MultipleObjectsReturned:
        print( "LOG: multiple objects returned for account {}".format(aaccountid))
        logger.info("LOG: multiple objects returned for account {}".format(aaccountid))
        return True  # multiple records - should not be the case
    except mongoengine.DoesNotExist:
        logger.info("LOG: does not exist - account {}".format(aaccountid))
        return False  # account does not exist
    except Exception as e:
        print( "LOG: AccountServices:account_does_exist: a different exception returned than expected for account {}".format(aaccountid))
        print( "Exception type: {} message: {}" .format(type(e), e.message))
        logger.info("LOG: AccountServices:account_does_exist: a different exception returned than expected for account {}".format(aaccountid))
        logger.info("Exception type: {} message: {}" .format(type(e), e.message))
        return True         # do not want it creating new account on Register

def account_validateamount(transamount):
    if transamount < 0:
        return False
    else:
        return True


### Database queries
def account_count(cls):
    return Account.objects().count()