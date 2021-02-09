import pdb
import sys
import os
import json
import pprint
from file_creator import Query_Execution_Summary, Task_Execution_Summary, Detailed_Metrics_per_task

def main():
    # Check and retrieve command-line arguments
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)  # Return a non-zero value to indicate abnormal termination
    filepath = sys.argv[1]

    # Verify source file
    if not os.path.isfile(filepath):
        print("error: {} does not exist".format(filepath))
        sys.exit(1)

    with open(filepath) as file_name:
        line = file_name.readline()
        while line != '':  # The EOF char is an empty string
            # 'Query Execution Summary' in line:
            if 'OPERATION' in line:
                query_execution = Query_Execution_Summary()
                query_execution.create_Query_Execution_Summary_text_file(file_name)
            # 'Task Execution Summary' in line:
            elif 'VERTICES' in line:
                task_execution = Task_Execution_Summary()
                task_execution.create_Task_Execution_Summary_text_file(line,file_name)
            elif 'org.apache.tez.common.counters.DAGCounter' in line:
                detailed_metrics = Detailed_Metrics_per_task()
                detailed_metrics.create_Detailed_Metrics_per_task_text_file(line,file_name)

            line = file_name.readline()

if __name__ == '__main__':
    main()