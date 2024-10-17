import json
import os
from pathlib import Path
import logging

FOLDER_NAME = "output_files"
FILE_NAME = "task_execution_summary.txt"

# Task Execution Summary category is defined within such lines. Bellow variable category_delimiter, is used to determine the start/end of the category.
category_delimiter = 'INFO  : ----------------------------------------------------------------------------------------------'


class TaskExecutionSummary:

    def __init__(self):
        self.seperator_indicator = 0
        # Creation of dictionary that will be passed in the output file
        self.Task_Execution_Summary_dictionary = {}

    def _get_file_location(self):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline\InitiationFiles
        parent_of_script_dir = Path(script_dir).parent  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline
        file_path = os.path.join(parent_of_script_dir, FOLDER_NAME, FILE_NAME)
        return file_path

    # example of nested dictionary keys -> ['DURATION(ms)', 'CPU_TIME(ms)', 'GC_TIME(ms)', 'INPUT_RECORDS', 'OUTPUT_RECORDS']
    def _get_nested_dictionary_keys(self, line):
        # ignore "INFO :  " and "VERTICES" from line and store the rest metrics in a str to use as keys for the nested dictionary
        categories = line.replace("INFO  :   VERTICES      ", "")
        # store all elements from line in a list, except of "INFO  : "
        nested_dictionary_keys = categories.split()
        return nested_dictionary_keys

    def _read_next_line(self, input_file):
        line = input_file.readline()
        return line

    # check if there are still metrics for TaskExecutionSummary by verifying lines are in between of separators [------] [------]
    def _not_end_of_metrics(self):
        if self.seperator_indicator < 2:
            return True
        else:
            return False

    def _get_vertex_name_and_metrics(self, line):
        # Remove unnecessary log "INFO  : " and "," to match metrics format as displayed in the task description's example
        vertex_name_and_metrics = (line.replace("INFO  : ", "").replace(",", "")).split()
        return vertex_name_and_metrics

    # example of Key -> Map 1
    def _get_dictionary_key(self, vertex_name_and_metrics):
        key = ' '.join(vertex_name_and_metrics[0:2])
        return key

    # example of nested_dictionary_values ['65013.00', '516890', '7624', '13119,189', '1200']
    def _get_nested_dictionary_values(self, vertex_name_and_metrics):
        nested_values = ' '.join(vertex_name_and_metrics[2:len(vertex_name_and_metrics)])
        nested_dictionary_values = list(nested_values.split(" "))
        for index, value in enumerate(nested_dictionary_values):
            if "." not in value:
                nested_dictionary_values[index] = int(value)
        return nested_dictionary_values

    def _initialize_nested_dictionary(self, nested_dictionary, nested_dictionary_keys, nested_dictionary_values):
        for i in range(len(nested_dictionary_keys)):
            nested_dictionary[nested_dictionary_keys[i]] = nested_dictionary_values[i]
        return nested_dictionary

    def _write_dictionary_to_file(self, Task_Execution_Summary_file):
        json.dump(self.Task_Execution_Summary_dictionary, Task_Execution_Summary_file, indent=2)

    def create_task_execution_summary_text_file(self, line, input_file):
        file_path = self._get_file_location()

        # creation of output file task_execution_summary.txt
        with open(file_path, 'w') as TES_file:
            nested_dictionary_keys = self._get_nested_dictionary_keys(line)
            line = self._read_next_line(input_file)
            # as long as there are metrics in specific category (Task Execution Summary) keep parsing lines
            while self._not_end_of_metrics() is True:
                nested_dictionary = {}
                # If line is either the start or end of category logs, store it in the seperator_indicator indicator
                if category_delimiter in line:
                    self.seperator_indicator += 1
                else:
                    vertex_name_and_metrics = self._get_vertex_name_and_metrics(line)
                    dictionary_key = self._get_dictionary_key(vertex_name_and_metrics)
                    nested_dictionary_values = self._get_nested_dictionary_values(vertex_name_and_metrics)
                    nested_dictionary = self._initialize_nested_dictionary(nested_dictionary, nested_dictionary_keys,
                                                                           nested_dictionary_values)
                    self.Task_Execution_Summary_dictionary[dictionary_key] = nested_dictionary
                line = self._read_next_line(input_file)
            self._write_dictionary_to_file(TES_file)
        TES_file.close()
        logging.info("File task_execution_summary.txt was created successfully")
