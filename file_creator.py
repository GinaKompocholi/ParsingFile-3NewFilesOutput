import json
import pdb
from decimal import Decimal

category_seperator = 'INFO  : ----------------------------------------------------------------------------------------------'
'''
INFO  : ----------------------------------------------------------------------------------------------
        Each of three categories Query_Execution_Summary, Task_Execution_Summary ,Detailed_Metrics_per_task
        are defined within such lines. Above variable category_seperator, is used to determine the start/end
        of each category.
INFO  : ----------------------------------------------------------------------------------------------
'''

class Query_Execution_Summary:

    def __init__(self):
        self.seperator_indicator = 0
        # Creation of dictionary that will be passed in the output file
        self.Query_Execution_Summary_dictionary = {}

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
        with open('Query_Execution_Summary.txt', 'w') as QES_file:
            # move to next line since 'INFO  : OPERATION    DURATION' line won't be used for creation of dictionary
            line = self._read_next_line(input_file)

            # as long as there are metrics in specific category (Query Execution Summary) keep parsing lines
            while self._not_end_of_metrics() is True:
                # If line is either the start or end of category logs, store it in the seperator_indicator indicator
                if category_seperator in line:
                    self.seperator_indicator += 1
                else:
                    key, value = self._get_key_and_value_from_metrics(line)
                    self.Query_Execution_Summary_dictionary[key] = value
                line = self._read_next_line(input_file)
            self._write_dictionary_to_file(QES_file)
        QES_file.close()

class Task_Execution_Summary:

    def __init__(self):
        self.seperator_indicator = 0
        # Creation of dictionary that will be passed in the output file
        self.Task_Execution_Summary_dictionary = {}

    # example of nested dictionary keys -> ['DURATION(ms)', 'CPU_TIME(ms)', 'GC_TIME(ms)', 'INPUT_RECORDS', 'OUTPUT_RECORDS']
    def _get_nested_dictionary_keys(self,line):
        # ignore "INFO :  " and "VERTICES" from line and store the rest metrics in a str to use as keys for the nested dictionary
        categories = line.replace("INFO  :   VERTICES      ", "")
        # store all elements from line in a list, except of "INFO  : "
        nested_dictionary_keys = categories.split()
        return nested_dictionary_keys

    def _read_next_line(self, input_file):
        line = input_file.readline()
        return line

    # check if there are still metrics for Task_Execution_Summary by verifying lines are in between of separators [------] [------]
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

    def create_Task_Execution_Summary_text_file(self, line, input_file):

        #creation of output file Task_Execution_Summary.txt
        with open('Task_Execution_Summary.txt', 'w') as TES_file:

            nested_dictionary_keys = self._get_nested_dictionary_keys(line)
            line = self._read_next_line(input_file)

            # as long as there are metrics in specific category (Task Execution Summary) keep parsing lines
            while self._not_end_of_metrics() is True:
                nested_dictionary = {}
                # If line is either the start or end of category logs, store it in the seperator_indicator indicator
                if category_seperator in line:
                    self.seperator_indicator += 1
                else:
                    vertex_name_and_metrics = self._get_vertex_name_and_metrics(line)
                    dictionary_key = self._get_dictionary_key(vertex_name_and_metrics)
                    nested_dictionary_values = self._get_nested_dictionary_values(vertex_name_and_metrics)
                    nested_dictionary = self._initialize_nested_dictionary(nested_dictionary, nested_dictionary_keys,nested_dictionary_values)
                    self.Task_Execution_Summary_dictionary[dictionary_key] = nested_dictionary
                line = self._read_next_line(input_file)
            self._write_dictionary_to_file(TES_file)
        TES_file.close()


class Detailed_Metrics_per_task:

    def _read_next_line(self, input_file):
        line = input_file.readline()
        return line

    def _get_vertex_name_and_metrics(self, line):
        # Remove unnecessary log "INFO  : " to match metrics format as displayed in the task description's example
        vertex_name_and_metrics = (line.replace("INFO  : ", "")).split()
        return vertex_name_and_metrics

    # example of nested_dictionary_values ['NUM_SUCCEEDED_TASKS:', '58']
    def _get_nested_dictionary_values(self, vertex_name_and_metrics):
        nested_dictionary_key = ' '.join(vertex_name_and_metrics[0:1])
        nested_dictionary_value = ' '.join(vertex_name_and_metrics[1:2])
        return nested_dictionary_key, nested_dictionary_value

    def _initialize_nested_dictionary(self, nested_dictionary, nested_dictionary_key, nested_dictionary_value):
        nested_dictionary[nested_dictionary_key] = int(nested_dictionary_value)
        return nested_dictionary

    # example of Keys -> org.apache.tez.common.counters.DAGCounter:, File System Counters:
    def _get_dictionary_key(self, line):
        key = line.replace("INFO  : ", "").replace(":", "").replace("\n", "")
        return key

    # check if there are still metrics for task by verifying line has spacing [:   ]
    def _not_end_of_metrics(self, line):
        if  ":   " in line:
            return True
        else:
            return False

    def create_Detailed_Metrics_per_task_text_file(self, line, input_file):

        #creation of output file Detailed_Metrics_per_task.txt
        with open('Detailed_Metrics_per_task.txt', 'w') as Detailed_Metrics:

            key = self._get_dictionary_key(line)
            while 'Completed' not in key:
                line = self._read_next_line(input_file)
                Detailed_Metrics_dictionary = {}
                nested_dictionary = {}

                # as long as there are detailed metrics for each task (key) keep parsing lines
                while self._not_end_of_metrics(line) is True:
                    vertex_name_and_metrics = self._get_vertex_name_and_metrics(line)
                    nested_dictionary_key, nested_dictionary_value = self._get_nested_dictionary_values(vertex_name_and_metrics)
                    nested_dictionary = self._initialize_nested_dictionary(nested_dictionary, nested_dictionary_key, nested_dictionary_value)
                    Detailed_Metrics_dictionary[key] = nested_dictionary
                    line = self._read_next_line(input_file)
                json.dump(Detailed_Metrics_dictionary, Detailed_Metrics, indent=2)
                key = self._get_dictionary_key(line)
        Detailed_Metrics.close()
