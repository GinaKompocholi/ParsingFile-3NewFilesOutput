import sys
import os
from InitiationFiles.file_creator import Query_Execution_Summary, Task_Execution_Summary, Detailed_Metrics_per_task
import logging
import pdb
from pathlib import Path

def _check_retrieve_command_line_args():

    # If user does not provide an input file, get the example input file from InitiationFiles folder
    if len(sys.argv) == 1:
        script_path = os.path.abspath(__file__)  # i.e. /path/to/dir/foobar.py
        script_dir = os.path.split(script_path)[0]  # i.e. /path/to/dir/
        file_name = "beeline_consent_query_stderr.txt"
        path = os.path.join(script_dir,  file_name)
        return path
    # If user stores an input file in root folder [Beeline] use this as an input file instead
    elif len(sys.argv) == 2:
        return sys.argv[1]
    # If user enters more arguments in command line, terminate
    else:
        logging.critical('Too many arguments were given.')
        sys.exit(1)  # Return a non-zero value to indicate abnormal termination


def _verify_existance_of_file(filepath):
    # Verify source file
    if not os.path.isfile(filepath):
        logging.critical("File {} does not exist".format(filepath))
        sys.exit(1)


def set_up_logger1():
    logging.root.handlers = []
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s' , level=logging.INFO, filename='loggings.log')

    # Setup Logging Object
    logger = logging.getLogger('LOG')
    logger.setLevel(logging.DEBUG)

    # Set log object to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)



    logging.getLogger("").addHandler(console)


def set_up_logger2():
    logging.root.handlers = []

    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='logging-info.log' ,filemode='w')
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG, filename='debugging.log' ,filemode='w')

    # Setup Logging Object
    logger = logging.getLogger('LOG')
    logger.setLevel(logging.DEBUG)

    # Set log object to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

def set_up_logger():

    logging.root.handlers = []
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline\InitiationFiles
    parent_of_script_dir = Path(script_dir).parent  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline
    folder_name = "Logs"
    file_name = "logging_info.log"
    file_path = os.path.join(parent_of_script_dir, folder_name, file_name)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO, filename=file_path ,filemode='a')
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG, filename=file_path ,filemode='a')


    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    #pdb.set_trace()

    f_handler = logging.FileHandler(file_path)

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.info('This is a warning')
    logger.error('This is an error')