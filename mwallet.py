from bottle import route, request, run, get, post, template, SimpleTemplate, static_file, url
#from model.Accounts import *
import services.AccountServices as AcServices
import json
import sys
#from bson import json_util
#import pymongo
import mongoengine as mongoengine
from twilio.twiml.messaging_response import MessagingResponse
import logging
from applog.loggingmodule import setlogger


@route('/static/<filename>', name='static')
def static(filename):
    return static_file(filename, root='static')

@get('/testmessage')
def testmessage():
    response="hello"
    output = template('views/mwallet_test', response=response, get_url=url, encoding='utf8')
    return output

@post('/testmessage')
def testmessage():
    #returns exercise data from newexercise.tpl in a DICT
    print '=== POST came through with data===='
    logger = logging.getLogger(__name__)
    logger.info('=== POST came through with data====')
    messagedata = dict(request.params)
    print messagedata     #looks like DICT
    phonenumber = request.forms.get("account")
    smsmessage = request.forms.get("message")
    messagedata = smsmessage.split(" ", 2)  # maxsplit: 2 expect anything over 2 is wrong; validate 1 & 2
    ########### ### validate smsmessage - ensure complies with expectations
    logger.info(type(messagedata))
    print type(messagedata)
    if len(messagedata) == 2:
        actiontoperform = str(messagedata[0]).upper()        #ACTION TO BE PERFORMED: first
        action_value = str(messagedata[1])                  #expected text and value:  REGISTER: name; DEPOSIT/WITHDRAW: amount
    elif len(messagedata) ==1:
        actiontoperform = str(messagedata[0]).upper()  # ACTION TO BE PERFORMED: first
        action_value = ""
    response = controller(phonenumber, actiontoperform, action_value)  # directs for appropriate action
    ##################
    output = template('views/mwallet_test', response=response, get_url=url, encoding='utf8')
    return output

@post('/sms')
def sms():
    ## Receive SMS message, process and return a dynamic reply based on BODY content
    ## responds to Twilio's TwiML messaging and parameters: https://www.twilio.com/docs/sms/twiml
    ## obtain key parameters [case sensitive]:
    #       MessageSid : unique message identifier
    #       From: phone number or channel address
    #       Body: message body
    #       Other interesting data: FromCity, FromState, FromCountry
    logger = logging.getLogger(__name__)
    messagebody = request.forms.get('Body', None)
    print messagebody
    logger.info(messagebody)
    phonenumber = request.forms.get('From', None)
    location_country = request.forms.get('FromCountry', None)
    location_city = request.forms.get('FromCity', None)
    print "LOCATION country {} city {}" .format(location_country, location_city)
    logger.info("LOCATION country {} city {}" .format(location_country, location_city))
    ### IMPROVE CAPTURE OF THE MESSAGE BODY - what is there?
    # perhaps log message body here
    messagedata = messagebody.split(" ", 2)  # maxsplit: 2 expect anything over 2 is wrong; validate 1 & 2
    ########### ### validate smsmessage - ensure complies with expectations
    print type(messagedata)
    if len(messagedata) == 2:
        actiontoperform = str(messagedata[0]).upper()        #ACTION TO BE PERFORMED: first
        action_value = str(messagedata[1])                  #expected text and value:  REGISTER: name; DEPOSIT/WITHDRAW: amount
    elif len(messagedata) ==1:
        actiontoperform = str(messagedata[0]).upper()  # ACTION TO BE PERFORMED: first
        action_value = ""
    print "route-action: {}".format(actiontoperform)
    print "value: {}".format(action_value)
    response = controller(phonenumber, actiontoperform, action_value)             #directs for appropriate action
    #################################
    # Start TwiML response
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)


def controller(accountid, routedirection, action_value):
    logger = logging.getLogger(__name__)
    logger.info('in controller determing with route to follow')
    # Manages the processing of the SMS?Form data to the appropriate action: REGISTER, DEPOSIT, WITHDRAW, TRANSFER
    # Potential to capture COUNTRY and adapt for multiple contracts/project
    # parameters: phonenumber==accountid, action to perform== routedirection, value associate with action == action_value
    if routedirection == "REGISTER":
        personname = str(action_value)
        ### VALIDATE THAT personname is a str
        response = AcServices.account_register(accountid, personname)
        #response = registeraccount(accountid, personname)
    elif routedirection == "DEPOSIT":
        valueamount = float(action_value)         ###VALIDATE NUMBER!! - greater than zero!
        #response = makedeposit(accountid, valueamount)
        response = AcServices.account_deposit(accountid, valueamount)
    elif routedirection == "WITHDRAW":
        valueamount = float(action_value)         ###VALIDATE NUMBER!! - greater than zero!
        response = AcServices.account_withdraw(accountid, valueamount)
        #response = makewithdrawal(accountid, valueamount)
    elif routedirection == "BALANCE":
        response = AcServices.account_getbalance(accountid)
    elif routedirection == "TRANSFER":
        #valueamount = float(action_value)         ###VALIDATE NUMBER!! - greater than zero!
        #response = makewithdrawal(accountid, valueamount)
        response = "We do not offer TRANSFERS at this time."
    else:
        response = "DO NOT UNDERSTAND DESIRED ACTION.  You can REGISTER, DEPOSIT and WITHDRAW"
        #need exception handling?!!!
    #print "response from controller: {}" .format(response)
    logger.info('response from controller: {}' .format(response))
    return response




if __name__ == '__main__':
    # To run the server, type-in $ python server.py
    setlogger()     #introduces logging configuration to be used with logging
    try:
        with open('config\dbconfig.json', 'r') as json_data_file:
            dbconfig = json.load(json_data_file)
        #dbconfig_environ = dbconfig['DEV']
        dbconfig_environ = dbconfig['PRODAzure']
        #db =
        mongoengine.connect(dbconfig_environ['dbname'], host=dbconfig_environ['host'], port=dbconfig_environ['port'])
    except:    #errors.ConnectionFailure:
        print '===== DB ERROR!  Start the MongoBD, silly guy!'
        sys.exit('MongoDB database connection requires MongoDB to be running.  Start the process')
    run(host='localhost', port=8080, reloader=True)
