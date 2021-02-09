import sys
import os
import pdb
from InitiationFiles.file_creator import Query_Execution_Summary, Task_Execution_Summary, Detailed_Metrics_per_task


def _check_retrieve_command_line_args():

    # If user does not provide an input file, get the example input file from InitiationFiles folder
    if len(sys.argv) == 1:
        #pdb.set_trace()
        script_path = os.path.abspath(__file__)  # i.e. /path/to/dir/foobar.py
        script_dir = os.path.split(script_path)[0]  # i.e. /path/to/dir/
        folder_name = "InitiationFiles"
        file_name = "beeline_consent_query_stderr.txt"
        path = os.path.join(script_dir, folder_name, file_name)
        return path
    # If user stores an input file in root folder [Beeline] use this as an input file instead
    elif len(sys.argv) == 2:
        return sys.argv[1]
    # If user enters more arguments in command line, terminate
    else:
        print(__doc__)
        print('Not correct arguments')
        sys.exit(1)  # Return a non-zero value to indicate abnormal termination

def _verify_existance_of_file(filepath):
    # Verify source file
    if not os.path.isfile(filepath):
        print("error: {} does not exist".format(filepath))
        sys.exit(1)

def main():

    filepath = _check_retrieve_command_line_args()
    _verify_existance_of_file(filepath)

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