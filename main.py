import sys
import os
from InitiationFiles.file_creator import Query_Execution_Summary, Task_Execution_Summary, Detailed_Metrics_per_task
import logging
from InitiationFiles import setup

def main():

    setup.set_up_logger()

    filepath = setup._check_retrieve_command_line_args()
    setup._verify_existance_of_file(filepath)

    with open(filepath) as input_file:
        line = input_file.readline()
        while line != '':  # The EOF char is an empty string
            # 'Query Execution Summary' in line:
            if 'OPERATION' in line:
                query_execution = Query_Execution_Summary()
                query_execution.create_Query_Execution_Summary_text_file(input_file)
            # 'Task Execution Summary' in line:
            elif 'VERTICES' in line:
                task_execution = Task_Execution_Summary()
                task_execution.create_Task_Execution_Summary_text_file(line,input_file)
            elif 'org.apache.tez.common.counters.DAGCounter' in line:
                detailed_metrics = Detailed_Metrics_per_task()
                detailed_metrics.create_Detailed_Metrics_per_task_text_file(line,input_file)

            line = input_file.readline()

if __name__ == '__main__':
    main()