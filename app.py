import bottle
from bottle import route, request, run, get, post, template, SimpleTemplate, static_file, url
#from model.Accounts import *
import services.AccountServices as AcServices
import json
import sys
import mongoengine as mongoengine
from twilio.twiml.messaging_response import MessagingResponse
import logging
from applog.loggingmodule import setlogger
import os

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    setupdbandlogger()
    return bottle.default_app()


@route('/static/<filename>', name='static')
def static(filename):
    return static_file(filename, root='static')

@get('/')
def home():
    #response="hello"
    output = template('views/home', get_url=url, encoding='utf8')
    return output

@get('/testmessage')
def testmessage():
    response="hello"
    output = template('views/mwallet_test', response=response, get_url=url, encoding='utf8')
    return output

@post('/testmessage')
def testmessage():
    #returns exercise data from newexercise.tpl in a DICT
    print( '=== POST came through with data====')
    logger = logging.getLogger(__name__)
    logger.info('=== POST came through with data====')
    messagedata = dict(request.params)
    logger.info('== message data: {}' .format(messagedata))
    print( messagedata)     #looks like DICT
    phonenumber = request.forms.get("account")
    smsmessage = request.forms.get("message")
    messagedata = smsmessage.split(" ", 2)  # maxsplit: 2 expect anything over 2 is wrong; validate 1 & 2
    ########### ### validate smsmessage - ensure complies with expectations
    #logger.info(type(messagedata))
    #print( type(messagedata))
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
    print( messagebody)
    logger.info(messagebody)
    phonenumber = request.forms.get('From', None)
    location_country = request.forms.get('FromCountry', None)
    location_city = request.forms.get('FromCity', None)
    print( "LOCATION country {} city {}" .format(location_country, location_city))
    logger.info("LOCATION country {} city {}" .format(location_country, location_city))
    ### IMPROVE CAPTURE OF THE MESSAGE BODY - what is there?
    # perhaps log message body here
    messagedata = messagebody.split(" ", 2)  # maxsplit: 2 expect anything over 2 is wrong; validate 1 & 2
    ########### ### validate smsmessage - ensure complies with expectations
    print( type(messagedata))
    if len(messagedata) == 2:
        actiontoperform = str(messagedata[0]).upper()        #ACTION TO BE PERFORMED: first
        action_value = str(messagedata[1])                  #expected text and value:  REGISTER: name; DEPOSIT/WITHDRAW: amount
    elif len(messagedata) ==1:
        actiontoperform = str(messagedata[0]).upper()  # ACTION TO BE PERFORMED: first
        action_value = ""
    print( "route-action: {}".format(actiontoperform))
    print( "value: {}".format(action_value))
    response = controller(phonenumber, actiontoperform, action_value)             #directs for appropriate action
    #################################
    # Start TwiML response
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)


def controller(accountid, routedirection, action_value):
    logger = logging.getLogger(__name__)
    logger.info('in controller: determining which route to follow based on routedirection param {}' .format(routedirection))
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
        response = "DO NOT UNDERSTAND DESIRED ACTION.  You can REGISTER, DEPOSIT, WITHDRAW, BALANCE and TRANSFER"
        #need exception handling?!!!
    #print( "response from controller: {}" .format(response))
    logger.info('response from controller: {}' .format(response))
    return response

####################################
#if __name__ == '__main__':
def setupdbandlogger():
    # To run the server, type-in $ python server.py
    setlogger()     #introduces logging configuration to be used with logging
    logger = logging.getLogger(__name__)
    logger.info('MAIN: trying to connect to database ')
    with open('config\dbconfig.json', 'r') as json_data_file:
        dbconfig = json.load(json_data_file)
    #dbconfig_environ = dbconfig['DEV']
    #dbconfig_environ = dbconfig['PROD']
    #dbconfig_environ = dbconfig['PRODAzure']
    dbconfig_environ = dbconfig['MEDA']
    try:
        #if dbconfig_environ['use_azure_appvariable'] == "True":
        #    env_azure = True    #use the environmental variables from Azure
        #else:
        #    env_azure = False   #use the dbconfig settings
        logger.info('DB CONNECT: environment vars: {}' .format(dbconfig_environ))
        #logger.info('State of env_azure: {}' .format(env_azure))
        #if env_azure == True:
        #    mongoengine.connect(db=os.getenv("DATABASE_NAME"), host=os.getenv("DATABASE_HOST"), port=os.getenv("DATABASE_PORT"))
        #    logger.info('attempting to connect to Azure Cosmos BD in Azure environment: env_azure== {}' .format(env_azure))
        #    logger.info('DB CONNECT: SUCCESS - Azure configuration variables')
        #else:
            ##mongoengine.connect(db=dbconfig_environ['dbname'], host=dbconfig_environ['host'], port=dbconfig_environ['port'])
        #try:
        mongoengine.connect(db=dbconfig_environ['dbname'], host=dbconfig_environ['host'], port=dbconfig_environ['port'])
        #except Exception as e:
        #    logger.error('Database connection error: %s', e.message, exc_info=e)
        #    raise e
        #logger.info('DB CONNECT: SUCCESS - dbconfig_environ variables')
    except Exception as e:
        logger.error('DB CONNECT: Failed to connect - check log for error mesage')
        logger.error( "DB Connection exception: Exception type: {} message: {}".format(type(e), e.message))
        print( '===== DB ERROR!  Start the MongoBD, silly guy!')
        sys.exit('MongoDB database connection requires MongoDB to be running.  Start the process')
    logger.info('DB CONNECT: SUCCESS - dbconfig_environ variables')
    #commented out to run in Azure environment


if __name__ == '__main__':
    wsgi_app()
    run(host='localhost', port=8080, reloader=True)
