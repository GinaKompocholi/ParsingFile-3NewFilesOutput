## Assignment for data engineer position

### Input

We need to parse file `beeline_consent_query_stderr.txt`.
The file contains the output from stdout of beeline (a command line utility that sends queries to Hive SQL Engine).
The logs are unstructured as you can see, and they contain detailed information for the query execution and in the end (
after row 80)
the metrics of the execution engine for this query.

### Output

We need to parse the file , collect these metrics and put them in python dictionaries preserving the values (eg `1200`)
and the names (eg `REDUCE_INPUT_RECORDS`).  
The output of the program will be 3 files. The files are expected to have the dictionaries directly persisted and
formatted as shown in the examples below, no need to create csv or any other format.  
Each file will contain only the metrics of one of the three main categories listed below:

1) **Query Execution Summary**  
   Metrics in rows 80-91 . The file is expected to contain a python dictionary with keys the values under the Operations
   column and values the ones under the Duration column ,
   essentially 6 key-value pairs

2) **Task Execution Summary**  
   Metrics in rows 92-101.  
   For each Vertex (4 vertices for this query) we need to persist:

   - `DURATION`(ms),
   - `CPU_TIME`(ms),
   - `GC_TIME`(ms),
   - `INPUT_RECORDS`,
   - `OUTPUT_RECORDS`.

So here we ask for a dictionary that in the top level will contain as keys the 4 vertices and each vertex will contain
as value another dictionary.
The nested dictionary will contain as keys the 5 metrics for each vertex. E.g.:

```
{
    "Map 1" : { "DURATION(ms)" : 65013.00, "CPU_TIME(ms)": 516890, "GC_TIME(ms)" : 7624, "INPUT_RECORDS" : 13119189, "OUTPUT_RECORDS" : 1200},
    "Map 3" : ...
    .
    .
}
```

3) **Detailed Metrics per task**   
   Metrics in row 103-302.   
   Take advantage of the nesting and recreate a dictionary out of it that will contain all the metrics and the names
   respecting the
   grouping.

```
{
    "org.apache.tez.common.counters.DAGCounter" : {"NUM_SUCCEEDED_TASKS": 58 , "TOTAL_LAUNCHED_TASKS" : 58 , ...} ,
    "File System Counters:" : { ... } ,
     .
     .
}
```

### Technical Specs:

1. Try to use only python 2 or python 3 standard library modules.
2. Ideally the results should be produced in a single file scan.
3. The row numbers here are indicative. Please do not just parse the file and read the specific row numbers since this
   file is a sample.
4. The program should be able to collect the same groups of rows from any similar file (that could potentially be any
   file), so please do not read the specific lines from a list.
5. You need to be able to identify the group of lines starting with the specified headers (defined above in points 1 , 2
   and 3) anywhere in a file.