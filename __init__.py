#Configure logging in the application
#Code re-utilized from:  http://www.patricksoftwareblog.com/python-logging-tutorial/

from os import path, remove
import logging
import logging.config

import mwallet
import services.AccountServices

#SET UP LOG FILE
name_logfile = 'mwallet.log'

# If applicable, delete the existing log file to generate a fresh log file during each execution
#if path.isfile(name_logfile):
#    remove(name_logfile)               #rather than remove, could rename!!

# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)          #set logger level

# Create the Handler for logging data to a file
logger_handler = logging.FileHandler(name_logfile)
logger_handler.setLevel(logging.DEBUG)  #set log handler level

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
logger.addHandler(logger_handler)
logger.info('Completed configuring logger()!')
