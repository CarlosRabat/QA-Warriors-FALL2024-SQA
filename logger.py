import logging

def loggingObject():
    # Log format will be time, level, method, and message
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_name = 'QA-WARRIORS.log'

    # Logging setup
    logging.basicConfig(format=format_str, filename=file_name, level=logging.INFO)
    loggerObj = logging.getLogger('simple-logger')

    return loggerObj