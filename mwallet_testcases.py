## Test ACCOUNTS with mongoengine
#from model.Accounts import *
import mongoengine as mongoengine
import sys
import json


if __name__ == '__main__':
    ##  Test account - transaction relationship first
    # Mongoengine
    with open('config\dbconfig.json', 'r') as json_data_file:
        dbconfig = json.load(json_data_file)
    dbconfig_environ = dbconfig['DEV']
    mongoengine.connect(dbconfig_environ['dbname'], host=dbconfig_environ['host'], port=dbconfig_environ['port'])
    #testmaterial
    #Create test file with data:  store JSON file with test data: read in: create cases and run
    ##for case in testcasedata:
    nick = Account()
    #    result = nick.registeraccount(case['ac'], case['person'])
    result = nick.registeraccount('9061', 'becky')
    #print "print result - first word {}" .format(result[0:5])   # or do a splice by " ", 1
    if result[0:6] == "Cannot":
        print result
        sys.exit('account exists, so stopping')
    nick.deposit(1000)
    nick.deposit(1050)
    nick.getbalance()
    print nick.sendtojson()
    print "======"
    nick2 = Account.objects.get(accountid='9061')
    nick2.deposit(20000)
    print nick2.getbalance()
    print nick2.sendtojson()
    print "======"
    ##Scenario: one class - the data layer class
    becky = Account()
    result = becky.registeraccount('8281', 'charis')
    if result[0:6] == "Cannot":
        print result
        sys.exit('account exists, so stopping')
    print result
    becky.deposit(10000)
    becky.deposit(1200)
    becky.getbalance()
    becky.withdraw(1500)
    becky.getbalance()
    print becky.sendtojson()
