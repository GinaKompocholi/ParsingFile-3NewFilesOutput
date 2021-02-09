import os, sys
import logging
from pathlib import Path
DEFAULT_FILE_NAME = 'beeline_consent_query_stderr.txt'

class Arguments:
    def _check_retrieve_command_line_args(self):
        # If user does not provide an input file, get the example input file from InitiationFiles folder
        if len(sys.argv) == 1:
            script_path = os.path.abspath(__file__)  # i.e. /path/to/dir/foobar.py
            script_dir = os.path.split(script_path)[0]  # i.e. /path/to/dir/
            folder = "../InputFile/"
            path = os.path.join(script_dir, folder, DEFAULT_FILE_NAME)
            return path
        # If user stores an input file in InitiationFiles folder, use this as an input file instead
        elif len(sys.argv) == 2:
            script_path = os.path.abspath(__file__)  # i.e. /path/to/dir/foobar.py
            script_dir = os.path.split(script_path)[0]  # i.e. /path/to/dir/
            folder = "../InputFile"
            folder_path = os.path.join(script_dir,  folder)
            path = os.path.join(folder_path,  sys.argv[1])
            return path
        # If user enters more arguments in command line, terminate
        else:
            logging.critical('Too many arguments were given.')
            sys.exit(1)  # Return a non-zero value to indicate abnormal termination


    def _verify_existance_of_file(self, filepath):
        # Verify source file
        if not os.path.isfile(filepath):
            logging.critical("File {} does not exist".format(filepath))
            sys.exit(1)

    def get_filepath(self):
        filepath = self._check_retrieve_command_line_args()
        self._verify_existance_of_file(filepath)
        logging.info("Arguments verification and filepath retrieval completed succesfully")
        return filepath

class Loggings:

    def _set_up_log_file(self):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline\InitiationFiles
        parent_of_script_dir = Path(script_dir).parent  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline
        folder_name = "Logs"
        file_name = "logging_info.log"
        file_path = os.path.join(parent_of_script_dir, folder_name, file_name)

        logging.basicConfig(filename=file_path,
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    def _set_up_console_logs(self):
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s,%(msecs)d - %(levelname)s - %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

    def set_up_logs(self):
        self._set_up_log_file()
        self._set_up_console_logs()
        logging.info("Setup of logs file and loggings on console completed succesfully")