from InitiationFiles.Query_execution_summary_File_creation import Query_Execution_Summary
from InitiationFiles.Task_execution_summary_File_creation import Task_Execution_Summary
from InitiationFiles.Detailed_metrics_per_task_File_creation import Detailed_Metrics_per_task
import logging


class ParseInputFile:
    def parse_file(self, filepath):

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
                    task_execution.create_Task_Execution_Summary_text_file(line, input_file)
                elif 'org.apache.tez.common.counters.DAGCounter' in line:
                    detailed_metrics = Detailed_Metrics_per_task()
                    detailed_metrics.create_Detailed_Metrics_per_task_text_file(line, input_file)

                line = input_file.readline()
        logging.info("Input file parsing completed succesfully")
