from os import path, remove
import logging
import logging.config
import json

# #set logging config
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)            #what level
#
# #create file handler
# handler = logging.FileHandler('logfile.log')
# #handler.setLevel(logging.INFO)
# handler.setLevel(logging.DEBUG)                     #what levels
#
# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
#
# # add the handlers to the logger
# logger.addHandler(handler)

#logger = logging.getLogger(__name__)

# # #LEARNING:  https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
# # 1. Write logging records everywhere with proper level
# #       info; debug; warn; error
# # 2. capture exceptions with traceback
# #         except Exception, e:
# #            logger.error('Failed to open file', exc_info=True)
# # 3. Do not get logger at the module level unless disable_existing_loggers is False
# #       set the init / config logger FIRST
# #       then create call the logger at leach


def setlogger():
    # If applicable, delete the existing log file to generate a fresh log file during each execution
    with open('applog/config_logging.json', 'r') as logging_configuration_file:
        config_dict = json.load(logging_configuration_file)
    logging.config.dictConfig(config_dict)
    # Log that the logger was configured
    logger = logging.getLogger(__name__)
    logger.info('Completed configuring logger()!')