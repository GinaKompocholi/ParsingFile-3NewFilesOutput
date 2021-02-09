import json
import os
from pathlib import Path
import logging

FOLDER_NAME = "OutputFiles"
FILE_NAME = "Query_Execution_Summary.txt"

# Query_Execution_Summary category is defined within such lines. Bellow variable category_delimeter, is used to determine the start/end of the category.
category_delimeter = 'INFO  : ----------------------------------------------------------------------------------------------'

class Query_Execution_Summary:

    def __init__(self):
        self.seperator_indicator = 0
        # Creation of dictionary that will be passed in the output file
        self.Query_Execution_Summary_dictionary = {}

    def _get_file_location(self):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline\InitiationFiles
        parent_of_script_dir = Path(script_dir).parent  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline
        file_path = os.path.join(parent_of_script_dir, FOLDER_NAME, FILE_NAME)
        return file_path

    def _read_next_line(self, input_file):
        line = input_file.readline()
        return line

    # check if there are still metrics for Task_Execution_Summary by verifying lines are in between of separators [------] [------]
    def _not_end_of_metrics(self):
        if self.seperator_indicator < 2:
            return True
        else:
            return False

    # OPERATION DURATION metrics example -> ['Compile Query', '7.43s']
    def _get_key_and_value_from_metrics(self, line):
        # ignore "INFO :  " from line and store the rest metrics in a str to use as keys and values for dictionary
        metrics = line.replace("INFO  : ", "").split()
        key = ' '.join(metrics[0:len(metrics) - 1])
        value = metrics[-1]
        return key, value

    def _write_dictionary_to_file(self, Query_Execution_Summary_file):
        json.dump(self.Query_Execution_Summary_dictionary, Query_Execution_Summary_file, indent=2)

    def create_Query_Execution_Summary_text_file(self, input_file):

        file_path = self._get_file_location()
        #creation of output file Query_Execution_Summary.txt
        with open(file_path, 'w') as QES_file:
            # move to next line since 'INFO  : OPERATION    DURATION' line won't be used for creation of dictionary
            line = self._read_next_line(input_file)

            # as long as there are metrics in specific category (Query Execution Summary) keep parsing lines
            while self._not_end_of_metrics() is True:
                # If line is either the start or end of category logs, store it in the seperator_indicator indicator
                if category_delimeter in line:
                    self.seperator_indicator += 1
                else:
                    key, value = self._get_key_and_value_from_metrics(line)
                    self.Query_Execution_Summary_dictionary[key] = value
                line = self._read_next_line(input_file)
            self._write_dictionary_to_file(QES_file)
        QES_file.close()
        logging.info("File Query_Execution_Summary.txt created successfully")
