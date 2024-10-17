from InitiationFiles.query_execution_summary_file_creation import QueryExecutionSummary
from InitiationFiles.task_execution_summary_file_creation import TaskExecutionSummary
from InitiationFiles.detailed_metrics_per_task_file_creation import DetailedMetricsPerTask
import logging


class ParseInputFile:

    def parse_file(self, filepath):
        with open(filepath) as input_file:
            line = input_file.readline()
            while line != '':  # The EOF char is an empty string
                # 'Query Execution Summary' in line:
                if 'OPERATION' in line:
                    query_execution = QueryExecutionSummary()
                    query_execution.create_query_execution_summary_text_file(input_file)
                # 'Task Execution Summary' in line:
                elif 'VERTICES' in line:
                    task_execution = TaskExecutionSummary()
                    task_execution.create_task_execution_summary_text_file(line, input_file)
                elif 'org.apache.tez.common.counters.DAGCounter' in line:
                    detailed_metrics = DetailedMetricsPerTask()
                    detailed_metrics.create_detailed_metrics_per_task_text_file(line, input_file)

                line = input_file.readline()
        logging.info("Input file parsing completed successfully")
