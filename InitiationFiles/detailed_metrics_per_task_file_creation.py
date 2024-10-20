import json
import os
from pathlib import Path
import logging

FOLDER_NAME = "output_files"
FILE_NAME = "detailed_metrics_per_task.txt"


class DetailedMetricsPerTask:

    def _get_file_location(self):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline\InitiationFiles
        parent_of_script_dir = Path(script_dir).parent  # i.e. C:\Users\KompocholiG\PycharmProjects\Beeline
        file_path = os.path.join(parent_of_script_dir, FOLDER_NAME, FILE_NAME)
        return file_path

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
        return line.replace("INFO  : ", "").replace(":", "").replace("\n", "")

    # check if there are still metrics for task by verifying line has spacing [:   ]
    def _not_end_of_metrics(self, line):
        return ":   " in line

    def create_detailed_metrics_per_task_text_file(self, line, input_file):
        file_path = self._get_file_location()

        # creation of output file detailed_metrics_per_task.txt
        with open(file_path, 'w') as detailed_metrics:
            key = self._get_dictionary_key(line)
            while 'Completed' not in key:
                line = self._read_next_line(input_file)
                detailed_metrics_dictionary = {}
                nested_dictionary = {}

                # as long as there are detailed metrics for each task (key) keep parsing lines
                while self._not_end_of_metrics(line):
                    vertex_name_and_metrics = self._get_vertex_name_and_metrics(line)
                    nested_dictionary_key, nested_dictionary_value = self._get_nested_dictionary_values(
                        vertex_name_and_metrics)
                    nested_dictionary = self._initialize_nested_dictionary(nested_dictionary, nested_dictionary_key,
                                                                           nested_dictionary_value)
                    detailed_metrics_dictionary[key] = nested_dictionary
                    line = self._read_next_line(input_file)
                json.dump(detailed_metrics_dictionary, detailed_metrics, indent=2)
                key = self._get_dictionary_key(line)
        detailed_metrics.close()
        logging.info("File detailed_metrics_per_task.txt was created successfully")
