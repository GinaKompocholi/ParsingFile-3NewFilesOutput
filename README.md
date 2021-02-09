# ParsingLogFile-3NewFilesOutput

### **Project Scope**

Main parses an input file (eg "beeline_consent_query_stderr.txt") and distinguishes the 3 main categories of the file (Query Execution Summary, Task Execution Summary, Detailed Metrics per task).
For each category, collects metrics and stores them in python Dictionaries preserving the values (eg 1200) and the names (eg REDUCE_INPUT_RECORDS), which the saves in a new txt file.

Build with Python 3.8.4 


### **In more Detail**

Each txt file contains only the metrics of one of the three main categories listed below:

1) Query Execution Summary 
Output file : 'Query_Execution_Summary.txt' -> Contains a python dictionary with keys the values under the Operations column and values the ones under the Duration column, in rows 80-91 of file "beeline_consent_query_stderr.txt". 

2) Task Execution Summary
Output file : 'Task_Execution_Summary.txt' -> Contains a python dictionary which in the top level contains as keys the 4 vertices ("Map 1","Map 3","Map 4","Reducer 2") and as value a nested dictionary.
The nested dictionary contains as keys the 5 metrics (DURATION(ms), CPU_TIME(ms), GC_TIME(ms), INPUT_RECORDS, OUTPUT_RECORDS) for each vertex and as values all the metrics under each column.
Metrics in rows 92-101. 

3) Detailed Metrics per task 
Output file : ''Detailed_Metrics_per_task.txt' -> Contains a python dictionary which in the top level contains as keys the 4 vertices
 Take advantage of the nesting and recreates a dictionary out of it that will contain all the metrics and the names respecting the 
grouping. Metrics in row 103-302.


